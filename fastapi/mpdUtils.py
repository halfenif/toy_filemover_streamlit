from mpd import MPDClient
from const import RESULT_FAIL
from config import IS_DEBUG, MPD_SERVER_IP, MPD_SERVER_PORT
import inspect
from RequestResult import RequestResult

def mpd_update_file():
    client = MPDClient()

    try:
        client.connect(MPD_SERVER_IP, MPD_SERVER_PORT)
        if IS_DEBUG:
            print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] mpd_version:', client.mpd_version)        

            # filelist = client.lsinfo()
            # if filelist:
            #     print("파일 목록:")
            #     for item in filelist:
            #         if 'file' in item:
            #             print(f"  파일: {item['file']}")
            #         elif 'directory' in item:
            #             print(f"  디렉토리: {item['directory']}")

        # client.timeout(MPD_SERVER_TIMEOUT)
        client.update()

    except Exception as e:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] Exception:', str(e))
        requestResult = RequestResult()
        requestResult.result = RESULT_FAIL
        requestResult.msg = str(e)
        requestResult.method = f'{inspect.stack()[0][3]}'
        return requestResult         
    
    return None

