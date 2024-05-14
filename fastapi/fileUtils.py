from fastapi import HTTPException
import hashlib
import base64
from operator import truediv
import os
import shutil

import inspect

import config
import const
import fileUtils
from pathlib import Path
import shutil

from requestApp import internalError

from RequestResult import RequestResult
import re


def getFileSizeFmt(num, suffix="B"):
    for unit in [" ", " K", " M", " G", " T", " P", " E", " Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def getFileHash(file_path):
    f = open(file_path, 'rb')
    data = f.read()
    hash = hashlib.md5(data).hexdigest()
    return hash


def getPathHash(path):
    return hashlib.md5(path.encode(const.ENC_TYPE)).hexdigest()

# 기본------------------
def getPathEncode(path):
    try:
        return base64.urlsafe_b64encode(bytes(path, const.ENC_TYPE)).decode(const.ENC_TYPE)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def getPathDecode(path):
    try:
        return base64.urlsafe_b64decode(bytes(path, const.ENC_TYPE)).decode(const.ENC_TYPE)
    except Exception as e:
        return '/'
#        raise HTTPException(status_code=500, detail=str(e))


def getPathReplace(pathType, path):
    return path.replace(fileUtils.getPathRoot(pathType), "")


def getPathRoot(pathType):
    # Debug
    print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathType:', pathType)

    if pathType == const.PATH_LOCATION_SOURCE:
        path_root = config.FOLDER_CONFIG[const.PATH_LOCATION_SOURCE]
    elif pathType == const.PATH_LOCATION_TARGET:
        path_root = config.FOLDER_CONFIG[const.PATH_LOCATION_TARGET]
    else:

        msg = "getPathRoot, pathType parameter not SOURCE or TARGET"
        print(msg)
        raise HTTPException(status_code=500, detail=msg)

    # Debug
    print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] path_root:', path_root)
    return path_root

def getFullPath(locationType: str, pathEncode: str):

    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] locationType:', locationType)
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathEncode:', pathEncode)    

    # Path Param is Encoded
    pathDecode = fileUtils.getPathDecode(pathEncode)

    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathDecode:', pathDecode)    

    # Make Path (source or target path + subpath)
    if pathDecode == '/':
        isRoot = True
        pathFull = fileUtils.getPathRoot(locationType)
    else:
        if config.IS_DEBUG:
            print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] Before Join:')    

        isRoot = False
        pathFull = os.path.join(
            fileUtils.getPathRoot(locationType), pathDecode)
        
    # Debug
    if config.IS_DEBUG:        
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathFull:', pathFull)    

    # Exist Check
    if not os.path.exists(pathFull):
        return internalError(f"Request Path Not Exist.[{pathFull}]", inspect.stack()[0][3]), None, None
        
    # Check Read or Write Permission
    read_write = os.access(pathFull, os.W_OK) and os.access(pathFull, os.R_OK)
    if not read_write:
        return internalError("Folder Permission denied", inspect.stack()[0][3]), None, None
            
    return None, pathFull, isRoot

# 추가------------------


def existFileAndFolder(pathType, path):
    decodePath = os.path.join(getPathRoot(pathType), getPathDecode(path))

    if os.path.exists(decodePath):
        return decodePath
    else:
        return None


def addFolder(pathType, path, folderName):
    try:
        pathTarget = os.path.join(getPathRoot(pathType), path, folderName)
        print(f'pathTarget:', pathTarget)
        os.makedirs(pathTarget)
        # 8진수로 파이썬3는 앞에 0o를 붙어야한다.
        os.chmod(pathTarget, 0o777)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def mvFolderAndFile(fullPathFrom, fullPathTo):
    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] fullPathFrom:', fullPathFrom)
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] fullPathTo:', fullPathTo)    

    try:
        shutil.copy(fullPathFrom, fullPathTo)
        os.remove(fullPathFrom)
        # os.rename(fullPathFrom, fullPathTo)
        # os.makedirs(pathTarget)
        # 8진수로 파이썬3는 앞에 0o를 붙어야한다.
        os.chmod(fullPathTo, 0o777)
    except Exception as e:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] os exception:', str(e))
        requestResult = RequestResult()
        requestResult.result = const.RESULT_FAIL
        requestResult.msg = str(e)
        requestResult.method = f'{inspect.stack()[0][3]}'
        return requestResult
    
    return None


def deleteFolderAndFile(pathType, path):
    try:
        pathTarget = os.path.join(getPathRoot(pathType), path)
        print(f'[fileUtils.py][deleteFolderAndFile pathTarget:', pathTarget)

        if os.path.isdir(pathTarget):
            shutil.rmtree(pathTarget, True)

        if os.path.isfile(pathTarget):
            os.remove(pathTarget)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def is_valid_filename(filename):
    # 파일명에 허용되지 않는 문자 패턴
    invalid_chars_pattern = r'[\\/:\*\?"<>\|]'  # 슬래시, 역슬래시, 콜론, 별표, 물음표, 큰따옴표, 부등호, 세미콜론, 수직바

    # 파일명에 허용되지 않는 문자 확인
    if re.search(invalid_chars_pattern, filename):
        return False
    else:
        return True