# Load .env
from env import Settings
config = Settings()

import os
import datetime
from genericpath import isdir
import inspect

from pathlib import Path

import const
from RequestResult import RequestResult
import fileUtils
from FileItem import FileItem
from FolderItem import FolderItem


# File Item for return
def addFile(fileItems, rootType, fullPath):
    # New FileItem Class
    fileItem = FileItem()
    fileItem.root_type = rootType
    fileItem.path_type = const.PATH_TYPE_FILE
    fileItem.file_path = fileUtils.getPathReplace(rootType, fullPath)
    fileItem.file_name = os.path.basename(fullPath)
    fileItem.file_name_display = fileUtils.getDisplayFileName(fileItem.file_name)
    fileItem.file_base_name, fileItem.file_ext_name = os.path.splitext(fileItem.file_name)    
    file_mday = datetime.datetime.fromtimestamp(
        os.path.getmtime(fullPath)).strftime(const.DATE_FORMAT)
    fileItem.file_mday = file_mday
    fileItem.file_size = fileUtils.getFileSizeFmt(
        os.path.getsize(fullPath))  # Calc FileInfo
    fileItem.path_encode = fileUtils.getPathEncode(fileItem.file_path)
    fileItem.path_link = "/file_info?file=" + fileItem.path_encode

    fileItem.file_path = ""
    fileItem.is_parent = False

    # Display Path
    fileItem.folder_current = fileItem.file_path

    fileItems.append(fileItem)  # Add to List
    return fileItems

# Folder Item for return
def addFolder(fileItems, rootType, fullPath):
    # New FileItem Class
    fileItem = FileItem()
    fileItem.root_type = rootType
    fileItem.path_type = const.PATH_TYPE_FOLDER
    fileItem.file_path = fileUtils.getPathReplace(rootType, fullPath)
    fileItem.file_name = os.path.basename(fullPath)
    fileItem.file_name_display = fileUtils.getDisplayFileName(fileItem.file_name)
    fileItem.file_base_name = ""
    fileItem.file_ext_name = ""
    file_mday = datetime.datetime.fromtimestamp(
        os.path.getmtime(fullPath)).strftime(const.DATE_FORMAT)
    fileItem.file_mday = file_mday
    fileItem.file_size = ""  # Calc FileInfo
    fileItem.path_encode = fileUtils.getPathEncode(fileItem.file_path)
    fileItem.path_link = ""

    fileItem.file_path = ""
    fileItem.is_parent = False

    # Display Path
    fileItem.folder_current = fileUtils.getPathReplace(rootType, fullPath)

    fileItems.append(fileItem)  # Add to List

    return fileItems

# Folder Item for Parent Folder
def addParentFolder(fileItems, pathCurrent, rootType):
    # 경로는 경우에 따라 혹은 OS에 따라 끝에 /가 붙을수도 등등 여러 경우가 있음으로..
    pathCurrentCheck = Path(pathCurrent).__str__()
    pathParent = Path(pathCurrent).parent.__str__()
    pathRoot = Path(fileUtils.getPathRoot(rootType)).__str__()

    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathCurrentCheck:', pathCurrentCheck)
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathParent:', pathParent)
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] rootType:', rootType)
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathRoot:', pathRoot)

    if pathCurrentCheck == pathRoot:
        return fileItems

    # New FileItem Class
    fileItem = FileItem()
    fileItem.root_type = rootType
    fileItem.path_type = const.PATH_TYPE_FOLDER
    fileItem.file_path = ""
    fileItem.file_name = ".."
    fileItem.file_name_display = fileUtils.getDisplayFileName(fileItem.file_name)
    fileItem.file_base_name = ""
    fileItem.file_ext_name = ""
    fileItem.file_mday = ""
    fileItem.file_mday = ""
    fileItem.file_size = ""  # Calc FileInfo

    if pathParent == pathRoot:
        fileItem.path_encode = fileUtils.getPathEncode("")
    else:
        fileItem.path_encode = fileUtils.getPathEncode(
            fileUtils.getPathReplace(rootType, pathParent))

    fileItem.file_path = ""
    fileItem.is_parent = True
    fileItems.insert(0, fileItem)  # Add to List
    return fileItems


# 통상적으로 지정된 Level1의 목록을 반환하는 함수
def list_folder_and_file_by_path(rootType: str, pathEncode: str):

    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] rootType:', rootType)
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathDecode:', pathEncode)

    stateCheck, pathFull, isRoot = fileUtils.getFullPath(rootType, pathEncode)
    if stateCheck:
        return stateCheck

    fileItems = []  # return list

    fileItems_files = []  # return list
    fileItems_folders = []  # return list




    for target_name in os.listdir(pathFull):
        if config.IS_DEBUG:
            print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] target_name:', target_name)

        # Make FilePath
        target_path = os.path.join(pathFull, target_name)

        # Check File or Folder
        if isdir(target_path):
            fileItems_folders = addFolder(fileItems_folders, rootType, target_path)
        else:
            if target_path.lower().endswith(".mp3"):
                fileItems_files = addFile(fileItems_files, rootType, target_path)

    # Sort List
    fileItems_folders.sort(key=lambda x: x.file_name, reverse=False)
    fileItems_files.sort(key=lambda x: x.file_name, reverse=False)

    # Add Parent
    if not isRoot:
        fileItems = addParentFolder(fileItems, pathFull, rootType)    

    for item in fileItems_files:
        fileItems.append(item)

    for item in fileItems_folders:
        fileItems.append(item)

    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] fileItems:', fileItems)    

    return fileItems


def folder_action(folderItem: FolderItem):
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] folderItem:', folderItem)
    
    requestResult = RequestResult()
    requestResult.result = const.RESULT_FAIL # 초기화
    requestResult.method = f'{inspect.stack()[0][3]}'    


    fullPathState, fullPathFrom, isRoot = fileUtils.getFullPath(folderItem.root_type, folderItem.path_encode)

    # Check
    if fullPathState:
        return fullPathState

    if folderItem.folder_command == const.FOLDER_ACTION_RENAME_CURRENT:
        # Check
        if isRoot:
            requestResult.msg = f"Root Folder에 대한 수정은 허용되지 않습니다.[{folderItem.new_folder_name}]"
            return requestResult
        
        # Get Base Folder
        baseFolder = os.path.basename(fullPathFrom)

        if folderItem.new_folder_name == baseFolder:
            requestResult.msg = f"기존 Folder명과 동일합니다.[{folderItem.new_folder_name}]"
            return requestResult

        # New Folder Check        
        if not fileUtils.is_valid_filename(folderItem.new_folder_name):
            requestResult.msg = f"유효하지 않은 Folder명입니다.[{folderItem.new_folder_name}]"
            return requestResult
        
        pathParent = Path(fullPathFrom).parent.__str__()
        fullPathTo = os.path.join(pathParent, folderItem.new_folder_name)

        requestResult = fileUtils.mvFolder(fullPathFrom, fullPathTo)
        if requestResult:
            return requestResult
        
        folderItem.path_encode = fileUtils.getPathEncode(fileUtils.getPathReplace(folderItem.root_type, fullPathTo))
        folderItem.new_folder_name = fileUtils.getDisplayFileName(folderItem.new_folder_name)

        if config.IS_DEBUG:
            print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] folderItem Return:', folderItem)            
        return folderItem



        
    elif folderItem.folder_command == const.FOLDER_ACTION_ADD_SUB_FOLDER:
        return ""
    elif folderItem.folder_command == const.FOLDER_ACTION_DELETE_CURRENT:
        return ""
    else:
        requestResult.msg = f"정의되지 않은 명령어 유형입니다. [{folderItem.folder_command}]"
        return requestResult

    requestResult.result = const.RESULT_FAIL # 초기화
    return ""