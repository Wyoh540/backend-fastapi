import uuid

from sqlmodel import SQLModel, Field


class FileBase(SQLModel):
    filename: str = Field(max_length=255, description="文件名称")
    filepath: str = Field(max_length=255, description="文件路径", default="")
    file_size: int = Field(description="文件大小，单位为字节")
    content_type: str = Field(max_length=100, description="文件内容类型")


class UploadedFile(FileBase, table=True):
    """文件上传模型"""

    __tablename__ = "uploaded_files"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
