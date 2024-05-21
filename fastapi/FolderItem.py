from pydantic import BaseModel, Field

class FolderItem(BaseModel):
    folder_command:           str = Field("", alias='folderCommand')
    root_type:                str = Field("", alias='rootType')
    path_encode:              str = Field("", alias="pathEncode")
    new_folder_name_encode:   str = Field("", alias="newFolderNameEncode")
    new_folder_name_display:  str = Field("", alias="newFolderNameDisplay")
