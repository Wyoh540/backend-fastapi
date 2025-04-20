from sqlmodel import SQLModel


class File(SQLModel):
    """File响应模型"""

    file_size: int


class UploadFile(SQLModel):
    """UploadFile响应模型"""

    file_name: str | None
    file_size: int | None
    content_type: str | None


class FileForm(SQLModel):
    """File表单上传响应模型"""

    file_size: int
    token: str
    fileb_content_type: str | None
