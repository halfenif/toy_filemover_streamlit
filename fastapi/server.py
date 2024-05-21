# Load .env
from env import Settings
config = Settings()

print(f'config.ENV_TYPE:{config.ENV_TYPE}')

from fastapi import FastAPI, Depends, File, Request
import inspect

import folderApp
import tagApp

from FileItem import FileItem
from TagItem import TagItem
from FolderItem import FolderItem
import const
from RequestResult import RequestResult


# --------------------------------------------------------------
# Application
app = FastAPI(
    title="FastAPI for FileMover",
    description="""Wow""",
    version="0.1.0",
)


# --------------------------------------------------------------
# Router

# API Test
@app.get("/api_test")
def api_test():
    print(f'test:')
    return {"name":"Name is Name"}

# Folder And File List
@app.get("/list_folder_and_file_by_path")
def list_folder_and_file_by_path(rootType: str, pathEncode: str):
    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] rootType:', rootType)
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathDecode:', pathEncode)    
    return folderApp.list_folder_and_file_by_path(rootType, pathEncode)

# Read Tag Info
@app.get("/file_read_taginfo_by_path")
def file_read_taginfo_by_path(fileItem: FileItem = Depends()):
    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] fileItem:', fileItem)

    return tagApp.file_read_taginfo_by_path(fileItem)

# Write Tag Info
@app.get("/file_write_taginfo_by_path")
def file_write_taginfo_by_path(tagItem: TagItem = Depends()):
    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] tagItem:', tagItem)

    return tagApp.file_write_taginfo_by_path(tagItem)


# Folder Action
@app.get("/folder_action")
def folder_action(folderItem: FolderItem = Depends()):
    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] folderItem:', folderItem)

    return folderApp.folder_action(folderItem)

# Upload File
@app.post("/upload_file")
def upload_file(request: Request, file: bytes = File(...)):


    headers = dict(request.headers)
    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] headers:', headers)

    # Check
    if not "root-type" in headers:
        requestResult = RequestResult()
        requestResult.result = const.RESULT_FAIL
        requestResult.msg = f"Request Header에 root-type이 없습니다."
        requestResult.method = f'{inspect.stack()[0][3]}'
        return requestResult
    
    if not "path-encode" in headers:
        requestResult = RequestResult()
        requestResult.result = const.RESULT_FAIL
        requestResult.msg = f"Request Header에 path-encode가 없습니다."
        requestResult.method = f'{inspect.stack()[0][3]}'
        return requestResult
    
    if not "file-name" in headers:
        requestResult = RequestResult()
        requestResult.result = const.RESULT_FAIL
        requestResult.msg = f"Request Header에 file-name이 없습니다."
        requestResult.method = f'{inspect.stack()[0][3]}'
        return requestResult

    fileItem = FileItem()
    fileItem.root_type = headers["root-type"]
    fileItem.path_encode = headers["path-encode"]
    fileItem.file_name = headers["file-name"]

    return folderApp.upload_file(file,fileItem)