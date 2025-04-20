from typing import Any

from fastapi import APIRouter, File, Form, UploadFile

from app import schemas

router = APIRouter()


@router.post("/files/", tags=["File"], response_model=schemas.File)
async def create_file(file: bytes = File()) -> Any:
    """使用File()上传文件,适用于小型文件"""
    return {"file_size": len(file)}


@router.post("/upload-file/", tags=["File"], response_model=schemas.UploadFile)
async def create_upload_file(file: UploadFile) -> Any:
    """使用UploadFile()上传文件, 适用于图像、视频、二进制文件等大型文件, 可获取上传文件的元数据"""
    return {
        "file_name": file.filename,
        "file_size": file.size,
        "file_content_type": file.content_type,
    }


@router.post("/upload-file-form/", tags=["File"], response_model=schemas.FileForm)
async def create_file_with_form(
    file: bytes = File(), fileb: UploadFile | None = None, token: str = Form()
) -> Any:
    """表单文件上传"""
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type if fileb else None,
    }
