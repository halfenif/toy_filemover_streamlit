from pydantic import BaseModel, Field

class TagItem(BaseModel):
    root_type:       str = Field("", alias='rootType')
    file_name:       str = Field("", alias='fileName')
    file_base_name:  str = Field("", alias='fileBaseName')
    file_ext_name:   str = Field("", alias='fileExtName')
    path_encode:     str = Field("", alias="pathEncode")
    tag_album:       str = Field("", alias='tagAlbum')
    tag_title:       str = Field("", alias='tagTitle')
    tag_artist:      str = Field("", alias='tagArtist')
    tag_albumartist: str = Field("", alias='tagAlbumartist')
    tag_date:        str = Field("", alias='tagDate')
    tag_tracknumber: str = Field("", alias='tagTracknumber')
    path_to_move_encode:     str = Field("", alias="pathToMoveEncode")
    doWhip:         bool = Field(False, alias='doWhip')
    doMove:         bool = Field(False, alias='doMove')
    doDeleteFile:   bool = Field(False, alias='doDeleteFile')
    doMpdUpdate:    bool = Field(False, alias='doMpdUpdate')