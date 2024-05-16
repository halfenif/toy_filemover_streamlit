from pydantic import BaseModel, Field

class FileItem(BaseModel):
    root_type:         str = Field("", alias='rootType')
    file_path:         str = Field("", alias='filePath')
    file_name:         str = Field("", alias='fileName')
    file_name_display: str = Field("", alias='fileNameDisplay')
    file_base_name:    str = Field("", alias='fileBaseName')
    file_ext_name:     str = Field("", alias='fileExtName')
    file_mday:         str = Field("", alias='fileMday')
    file_size:         str = Field("", alias='fileSize')
    path_type:         str = Field("", alias='pathType')
    path_encode:       str = Field("", alias="pathEncode")
    path_link:         str = Field("", alias="pathLink")
    folder_current:    str = Field("", alias="folderCurrent")
    is_parent:        bool = Field("", alias="isParent")