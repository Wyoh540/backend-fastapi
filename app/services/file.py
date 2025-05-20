import shutil
import uuid
from collections.abc import Generator

from sqlmodel import Session, select
from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app import models


class FileService:
    """文件管理"""

    @classmethod
    def save_file(cls, db: Session, file: UploadFile) -> models.UploadedFile:
        """保存文件"""
        upload_file = models.UploadedFile(filename=file.filename, file_size=file.size, content_type=file.content_type)

        file_path = settings.UPLOAD_DIR / upload_file.filepath / str(upload_file.id)

        # 安全验证：确保路径在指定的目录内
        if not file_path.resolve().parent.samefile(settings.UPLOAD_DIR):
            raise HTTPException(status_code=403, detail="Invalid upload directory")

        with file_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)
        db.add(upload_file)
        db.commit()
        db.refresh(upload_file)

        return upload_file

    @classmethod
    def download_file(cls, db: Session, file_id: uuid.UUID) -> StreamingResponse:
        """下载文件"""
        query = select(models.UploadedFile).where(models.UploadedFile.id == file_id)
        upload_file = db.exec(query).first()
        if not upload_file:
            raise HTTPException(status_code=404, detail="文件不存在")
        file_path = settings.UPLOAD_DIR / upload_file.filepath / str(upload_file.id)

        if not file_path.exists():
            db.delete(upload_file)
            db.commit()
            raise HTTPException(status_code=404, detail="文件不存在或已删除")

        def iterfile() -> Generator[bytes]:
            with file_path.open("rb") as f:
                yield from f

        return StreamingResponse(iterfile(), media_type=upload_file.content_type)

    @classmethod
    def delete_file(cls, db: Session, file_id: uuid.UUID) -> None:
        """删除上传的文件"""
        query = select(models.UploadedFile).where(models.UploadedFile.id == file_id)
        upload_file = db.exec(query).first()
        if not upload_file:
            raise HTTPException(status_code=404, detail="文件不存在")

        file_path = settings.UPLOAD_DIR / upload_file.filepath / str(upload_file.id)
        if file_path.exists():
            file_path.unlink()

        db.delete(upload_file)
        db.commit()
