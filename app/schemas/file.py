import uuid

from sqlmodel import SQLModel

from app.models.file import FileBase


class File(SQLModel):
    """File响应模型"""

    file_size: int


class UploadFile(FileBase):
    """UploadFile响应模型"""

    id: uuid.UUID


class FileForm(SQLModel):
    """File表单上传响应模型"""

    file_size: int
    token: str
    fileb_content_type: str | None
