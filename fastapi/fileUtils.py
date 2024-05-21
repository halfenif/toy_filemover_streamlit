# Load .env
from env import Settings
config = Settings()

# Import
from fastapi import HTTPException
import hashlib
import base64
from operator import truediv
import os
import shutil

import inspect

import const
import fileUtils
from pathlib import Path
import shutil

from requestApp import internalError

from RequestResult import RequestResult
import re
from unicodedata import east_asian_width


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
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathType:', pathType)
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] path:', path)
    
    pathRoot = pathJoin(fileUtils.getPathRoot(pathType),"")
    pathFrom = pathJoin(path,"")

    replaceResult = pathFrom.replace(pathRoot, "")
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] replaceResult:', replaceResult)

    return replaceResult


def getPathRoot(pathType):
    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathType:', pathType)

    if pathType == const.PATH_LOCATION_SOURCE:
        path_root = const.FOLDER_CONFIG[const.PATH_LOCATION_SOURCE]
    elif pathType == const.PATH_LOCATION_TARGET:
        path_root = const.FOLDER_CONFIG[const.PATH_LOCATION_TARGET]
    else:

        msg = "getPathRoot, pathType parameter not SOURCE or TARGET"
        raise HTTPException(status_code=500, detail=msg)

    # Debug
    # Debug
    if config.IS_DEBUG:
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
        pathFull = pathJoin(fileUtils.getPathRoot(locationType), pathDecode)
        
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

def getDisplayFileName(inputFileName):
    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] inputFileName:', inputFileName)    

    if not config.UI_OPTION_SHORT_FILE_NAME:
        return inputFileName
    
    outputFileName = ""

    list_double = ['W', 'F', 'W']

    # ChatGPT - ask python east_asian_width
    # Fullwidth (F): 주로 동아시아 문자로서 전체 너비를 차지합니다. 한자, 한글, 일어 등이 이에 해당합니다.
    # Halfwidth (H): 전체 너비의 반만 차지하는 문자들입니다. 주로 영어, 숫자, 일부 기호들이 여기에 해당합니다.
    # Neutral (N): East Asian Width가 적용되지 않는 문자들로, 대부분의 공백 문자나 제어 문자가 여기에 속합니다.
    # Wide (W): 전체 너비의 2배를 차지하는 문자들로, 전체 너비와 반대 개념입니다. 대부분의 기호 및 일부 특수 문자들이 여기에 속합니다.
    # Narrow (Na): Halfwidth의 너비보다 더 작은 문자들을 나타냅니다.
    # Ambiguous (A): East Asian Width 속성이 어떤 너비에 해당하는지 명확하지 않은 문자들입니다.

    fileNameLen = 0
    
    for item in inputFileName:
        unicode_result = east_asian_width(item)

        if unicode_result in list_double:
            fileNameLen+=2
        else:
            fileNameLen+=1
        
        if fileNameLen > config.UI_OPTION_SHORT_FILE_LENGTH:
            return outputFileName + "..."

        outputFileName = outputFileName + item

    return outputFileName

# 추가------------------


def pathJoin(pathPre, pathSur):

    # Debug
    if config.IS_DEBUG:        
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathPre:', pathPre)    
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathSur:', pathSur)    

    pathResultWithSlash = os.path.join("/", *pathPre.split("/"), *pathSur.split("/"))
    pathResult = os.path.normpath(pathResultWithSlash)
    if config.IS_DEBUG:        
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathResult:', pathResult)    
    return pathResult

def existFileAndFolder(pathType, path):
    decodePath = pathJoin(getPathRoot(pathType), getPathDecode(path))

    if os.path.exists(decodePath):
        return decodePath
    else:
        return None


def addFolder(pathTarget):
    try:
        os.makedirs(pathTarget)
        # 8진수로 파이썬3는 앞에 0o를 붙어야한다.
        os.chmod(pathTarget, 0o777)

        return None
    except Exception as e:
        return str(e)

def mvFile(fullPathFrom, fullPathTo):
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

def mvFolder(fullPathFrom, fullPathTo):
    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] fullPathFrom:', fullPathFrom)
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] fullPathTo:', fullPathTo)    

    try:
        # shutil.copy(fullPathFrom, fullPathTo)
        # os.remove(fullPathFrom)
        os.rename(fullPathFrom, fullPathTo)
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


def deleteFolderAndFile(pathTarget):

    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathTarget:', pathTarget)

    try:
        
        if not (pathTarget.startswith(getPathRoot(const.PATH_LOCATION_SOURCE)) or pathTarget.startswith(getPathRoot(const.PATH_LOCATION_TARGET))):
            requestResult = RequestResult()
            requestResult.result = const.RESULT_FAIL
            requestResult.msg = "삭제요청된 경로가 SOURCE, TARGET 하위경로가 아닙니다."
            requestResult.method = f'{inspect.stack()[0][3]}'
            return requestResult
        
        if pathTarget == getPathRoot(const.PATH_LOCATION_SOURCE) or pathTarget == getPathRoot(const.PATH_LOCATION_TARGET):
            requestResult = RequestResult()
            requestResult.result = const.RESULT_FAIL
            requestResult.msg = f"Root경로는 삭제 할 수 없습니다.[{pathTarget}]"
            requestResult.method = f'{inspect.stack()[0][3]}'
            return requestResult
                
        if os.path.isdir(pathTarget):
            shutil.rmtree(pathTarget, True)

        if os.path.isfile(pathTarget):
            os.remove(pathTarget)

    except Exception as e:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] os exception:', str(e))
        requestResult = RequestResult()
        requestResult.result = const.RESULT_FAIL
        requestResult.msg = str(e)
        requestResult.method = f'{inspect.stack()[0][3]}'
        return requestResult

    return None
    
def is_valid_filename(filename):
    # 허용되지 않는 문자를 포함하는지 검사
    invalid_chars = r'<>:"/\|?*{}'

    result = True

    # 빈 문자열 검사
    if not filename:
        result = False
    elif filename.startswith("."):
        result = False
    elif filename.endswith("."):
        result = False
    elif any(char in invalid_chars for char in filename):
        result = False

    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] filename:', filename)
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] result:', result)

    return result

def write_file(fileByte, filePath):

    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] filePath:', filePath)

    if os.path.exists(filePath):
        requestResult = RequestResult()
        requestResult.result = const.RESULT_FAIL
        requestResult.msg = f"존재하는 파일경로 입니다.[{filePath}]"
        requestResult.method = f'{inspect.stack()[0][3]}'
        return requestResult
    
    try:
        with open(filePath, "wb") as file:
            file.write(fileByte)
    except Exception as e:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] exception:', str(e))
        requestResult = RequestResult()
        requestResult.result = const.RESULT_FAIL
        requestResult.msg = str(e)
        requestResult.method = f'{inspect.stack()[0][3]}'
        return requestResult
    
    return None