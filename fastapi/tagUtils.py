# Load .env
from env import Settings
config = Settings()

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import EasyMP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis

import inspect
from TagItem import TagItem
from FileItem import FileItem

from requestApp import internalError

from RequestResult import RequestResult
import const

# Get ----------------------------------
def get_tag(pathFull: str, fileItem: FileItem):
    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathFull:', pathFull)


    tagItem = TagItem()
    tagItem.root_type = fileItem.root_type
    tagItem.file_name = fileItem.file_name
    tagItem.file_base_name = fileItem.file_base_name
    tagItem.file_ext_name = fileItem.file_ext_name
    tagItem.path_encode = fileItem.path_encode
    

    try:
        if pathFull.lower().endswith(".mp3"):
            tag = EasyID3(pathFull)
        elif pathFull.lower().endswith(".flac"):
            tag = FLAC(pathFull)
        elif pathFull.lower().endswith(".ogg"):
            tag = OggVorbis(pathFull)
        else:
            requestResult = RequestResult()
            requestResult.result = const.RESULT_FAIL # 초기화
            requestResult.method = f'{inspect.stack()[0][3]}'
            requestResult.msg = "지원하지 않는 확장자 입니다."       
            return requestResult, tagItem

        # Debug
        if config.IS_DEBUG:
            print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] tag:', tag)
            print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] Type of tag:', type(tag))

        if tag.get('title'):
            tagItem.tag_title = ','.join(tag.get('title'))
        
        if tag.get('artist'):
            tagItem.tag_artist = ','.join(tag.get('artist'))

        if tag.get('album'):
            tagItem.tag_album = ','.join(tag.get('album'))

        if tag.get('albumartist'):
            tagItem.tag_albumartist = ','.join(tag.get('albumartist'))

        if tag.get('date'):
            tagItem.tag_date = ','.join(tag.get('date'))

        if tag.get('tracknumber'):
            tagItem.tag_tracknumber = ','.join(tag.get('tracknumber'))

    except Exception as e:
        # Debug
        if config.IS_DEBUG:        
            print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] Exception:', e)        

        return internalError(f"MP3 Tag Read Error.[{pathFull}][{str(e)}]", inspect.stack()[0][3]), None

    return None, tagItem

# Set ----------------------------------
def set_tag(pathFull: str, tagItem: TagItem):
    # Debug
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] pathFull:', pathFull)
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] tagItem:', tagItem)
        

    try:
        if pathFull.lower().endswith(".mp3"):
            tag = EasyID3(pathFull)
        elif pathFull.lower().endswith(".flac"):
            tag = FLAC(pathFull)
        elif pathFull.lower().endswith(".ogg"):
            tag = OggVorbis(pathFull)
        else:
            requestResult = RequestResult()
            requestResult.result = const.RESULT_FAIL # 초기화
            requestResult.method = f'{inspect.stack()[0][3]}'
            requestResult.msg = "지원하지 않는 확장자 입니다."       
            return requestResult, tagItem

        # Debug
        if config.IS_DEBUG:
            print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] tag:', tag)
            print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] Type of tag:', type(tag))
        
        if tagItem.doWhip:
            tag.delete()

        if tagItem.tag_title:
            tag['title'] =tagItem.tag_title

        if tagItem.tag_artist:
            tag['artist'] =tagItem.tag_artist

        if tagItem.tag_album:
            tag['album'] =tagItem.tag_album

        if tagItem.tag_albumartist:
            tag['albumartist'] =tagItem.tag_albumartist

        if tagItem.tag_date:
            tag['date'] =tagItem.tag_date

        if tagItem.tag_tracknumber:
            tag['tracknumber'] =tagItem.tag_tracknumber
            
        tag.save()

    except Exception as e:
        # Debug
        if config.IS_DEBUG:        
            print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] Exception:', e)        

        return internalError(f"MP3 Tag Write Error.[{pathFull}][{str(e)}]", inspect.stack()[0][3]), None
    
    
    return None, tagItem