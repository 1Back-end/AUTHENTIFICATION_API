#
#
# from pydantic import BaseModel, Field, ConfigDict
# from typing import Any, Optional
#
# class FileUpload(BaseModel):
#     file_name: Optional[str] = None
#     base_64: Optional[Any] = None
#
# class FileResize(BaseModel):
#     file_name: Optional[str] = None
#     url: Optional[str] = None
#
# class File(BaseModel):
#     file_name: str
#     url: str
#     mimetype: Optional[int] = None
#     width: Optional[int] = None
#     height: Optional[int] = None
#     size: Optional[int] = None
#     thumbnail: Optional[FileResize] = None
#     medium: Optional[FileResize] = None
#
#     class Config:
#        model_config = ConfigDict(from_attributes=True)
