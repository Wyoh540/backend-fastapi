import uuid
from typing import Any

from fastapi import APIRouter, File, Form, UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import select

from app.models import UploadedFile
from app.api.deps import SessionDep
from app.services.file import FileService
from app import schemas

router = APIRouter()


@router.post("/files/", tags=["File"], response_model=schemas.File)
async def create_file(file: bytes = File()) -> Any:
    """使用File()上传文件,适用于小型文件"""
    return {"file_size": len(file)}


@router.post("/upload-file/", tags=["File"], response_model=schemas.UploadFile)
async def create_upload_file(session: SessionDep, file: UploadFile) -> Any:
    """使用UploadFile()上传文件, 适用于图像、视频、二进制文件等大型文件, 可获取上传文件的元数据"""

    upload_file = FileService.save_file(session, file=file)

    return upload_file


@router.get("/upload-file/", tags=["File"], response_model=Page[schemas.UploadFile])
def get_upload_files(session: SessionDep) -> Any:
    query = select(UploadedFile)

    return paginate(session, query)


@router.get("/upload-file/{file_id}", tags=["File"])
def download_file(file_id: uuid.UUID, session: SessionDep) -> Any:
    return FileService.download_file(session, file_id=file_id)


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


@router.delete("/upload-file/{file_id}", tags=["File"])
def delete_file(file_id: uuid.UUID, session: SessionDep) -> Any:
    """删除上传的文件"""
    FileService.delete_file(session, file_id=file_id)

    return {"detail": "文件已成功删除"}
