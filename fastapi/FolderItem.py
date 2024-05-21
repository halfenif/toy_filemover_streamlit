from pydantic import BaseModel, Field

class FolderItem(BaseModel):
    folder_command:    str = Field("", alias='folderCommand')
    root_type:         str = Field("", alias='rootType')
    path_encode:       str = Field("", alias="pathEncode")
    new_folder_name:   str = Field("", alias="newFolderName")
