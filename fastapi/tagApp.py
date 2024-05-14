import os
from genericpath import isdir
import inspect

from const import PATH_LOCATION_SOURCE, PATH_LOCATION_TARGET, RESULT_FAIL
import config
import fileUtils
from TagItem import TagItem
from RequestResult import RequestResult

import tagUtils

from FileItem import FileItem

from pathlib import Path

from mpdUtils import mpd_update_file

# 파일의 mp3 tag를 Read하는 함수
def file_read_taginfo_by_path(fileItem: FileItem):

    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] fileItem:', fileItem)

    stateCheck, pathFull, isRoot = fileUtils.getFullPath(fileItem.root_type, fileItem.path_encode)
    if stateCheck:
        return stateCheck
    
    stateCheck, tagItem = tagUtils.get_tag(pathFull, fileItem)
    if stateCheck:
        return stateCheck    

    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] tagItem:', tagItem)

    return tagItem

# 파일의 mp3 tag를 Write하는 함수
def file_write_taginfo_by_path(tagItem: TagItem):

    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] fileItem:', tagItem)

    stateCheck, pathFullLeft, isRoot = fileUtils.getFullPath(tagItem.root_type, tagItem.path_encode)
    if stateCheck:
        return stateCheck
    
    stateCheck, tagItem = tagUtils.set_tag(pathFullLeft, tagItem)
    if stateCheck:
        return stateCheck    

    #------------------------------
    # File rename or mv
    doMv = False
    # Origin Parent Path
    pathParent = Path(pathFullLeft).parent.__str__()
    # Base File Name Compare:
    check_left_file_name = os.path.basename(pathFullLeft)
    check_right_file_name = tagItem.file_base_name + tagItem.file_ext_name

    if not fileUtils.is_valid_filename(check_right_file_name):
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] check_right_file_name:', check_right_file_name)
        requestResult = RequestResult()
        requestResult.result = RESULT_FAIL
        requestResult.msg = "Not Valid File Name"
        requestResult.method = f'{inspect.stack()[0][3]}'
        return requestResult        

    if not check_left_file_name == check_right_file_name:
        doMv = True
    if tagItem.doMove:
        if tagItem.root_type == PATH_LOCATION_SOURCE:
            pathParent = fileUtils.getPathRoot(PATH_LOCATION_TARGET) + fileUtils.getPathDecode(tagItem.path_to_move_encode)
        elif tagItem.root_type == PATH_LOCATION_TARGET:
            pathParent = fileUtils.getPathRoot(PATH_LOCATION_SOURCE) + fileUtils.getPathDecode(tagItem.path_to_move_encode)

        doMv = True
    
    if doMv:
        pathFullRight = os.path.join("/", *pathParent.split("/"), *check_right_file_name.split("/"))
        mvResult = fileUtils.mvFolderAndFile(pathFullLeft, pathFullRight)
        if mvResult:
            return mvResult
    
    if tagItem.doMpdUpdate:
        mpd_status = mpd_update_file()
        if mpd_status:
            return mpd_status

    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] tagItem:', tagItem)

    return tagItem