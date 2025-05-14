import uuid
from typing import Any
import shutil

from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import select

from app.models import UploadedFile
from app.api.deps import SessionDep
from app.core.config import settings
from app import schemas

router = APIRouter()


@router.post("/files/", tags=["File"], response_model=schemas.File)
async def create_file(file: bytes = File()) -> Any:
    """使用File()上传文件,适用于小型文件"""
    return {"file_size": len(file)}


@router.post("/upload-file/", tags=["File"], response_model=schemas.UploadFile)
async def create_upload_file(session: SessionDep, file: UploadFile) -> Any:
    """使用UploadFile()上传文件, 适用于图像、视频、二进制文件等大型文件, 可获取上传文件的元数据"""

    upload_file = UploadedFile(filename=file.filename, file_size=file.size, content_type=file.content_type)
    file_path = settings.UPLOAD_DIR / upload_file.filepath / str(upload_file.id)

    # 安全验证：确保路径在指定的目录内
    if not file_path.resolve().parent.samefile(settings.UPLOAD_DIR):
        raise HTTPException(status_code=403, detail="Invalid upload directory")

    with file_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    session.add(upload_file)
    session.commit()
    session.refresh(upload_file)

    return upload_file


@router.get("/upload-file/", tags=["File"], response_model=list[schemas.UploadFile])
def get_upload_files(session: SessionDep) -> Any:
    query = select(UploadedFile)
    return session.exec(query).all()


@router.get("/upload-file/{file_id}", tags=["File"])
def download_file(file_id: uuid.UUID, session: SessionDep) -> Any:
    query = select(UploadedFile).where(UploadedFile.id == file_id)
    upload_file = session.exec(query).one()
    file_path = settings.UPLOAD_DIR / upload_file.filepath / str(upload_file.id)

    if not file_path.exists():
        session.delete(upload_file)
        session.commit()
        raise HTTPException(status_code=404, detail="文件不存在或已删除")

    return FileResponse(path=file_path, filename=upload_file.filename, media_type=upload_file.content_type)


@router.post("/upload-file-form/", tags=["File"], response_model=schemas.FileForm)
async def create_file_with_form(
    file: bytes = File(), fileb: UploadFile | None = File(default=None), token: str = Form()
) -> Any:
    """表单文件上传"""
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type if fileb else None,
    }
