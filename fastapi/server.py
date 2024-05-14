from fastapi import FastAPI, Depends
import inspect

import folderApp
import tagApp

from FileItem import FileItem
from TagItem import TagItem

import config

app = FastAPI(
    title="FastAPI for FileMover",
    description="""Wow""",
    version="0.1.0",
)

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