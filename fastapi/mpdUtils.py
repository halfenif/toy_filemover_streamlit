# Load .env
from env import Settings
config = Settings()

from mpd import MPDClient
from const import RESULT_FAIL
import inspect
from RequestResult import RequestResult
import json

def mpd_update_file():
    if config.IS_DEBUG:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] config.MPD_SERVER_LIST:', config.MPD_SERVER_LIST)

    try:
        servers = json.loads(config.MPD_SERVER_LIST)["servers"]
    except json.JSONDecodeError as e:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] Exception:', str(e))
        requestResult = RequestResult()
        requestResult.result = RESULT_FAIL
        requestResult.msg = f"MPD_SERVER_IP의 JSON문자열을 확인하시기 바랍니다. {str(e)}"
        requestResult.method = f'{inspect.stack()[0][3]}'
        return requestResult 
    
    for server in servers:
        if config.IS_DEBUG:
            print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] type of server:', type(server))
            print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] server:', server)

        update_status = mpd_update_by_server(server["IP"], server["PORT"])
        if update_status:
            return update_status


def mpd_update_by_server(serverIp: str, serverPort:int):
    client = MPDClient()

    try:
        client.connect(serverIp, serverPort)
        if config.IS_DEBUG:
            print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] mpd_version:', client.mpd_version)        
        if not client.mpd_version:
            requestResult = RequestResult()
            requestResult.result = RESULT_FAIL
            requestResult.msg = f"MPD에 연결 할 수 없습니다.[{serverIp}:{serverPort}]"
            requestResult.method = f'{inspect.stack()[0][3]}'
            return requestResult             
        client.update()
        client.disconnect()

    except Exception as e:
        print(f'[{inspect.getfile(inspect.currentframe())}][{inspect.stack()[0][3]}] Exception:', str(e))
        requestResult = RequestResult()
        requestResult.result = RESULT_FAIL
        requestResult.msg = f"{str(e)}, {serverIp}:{serverPort}"
        requestResult.method = f'{inspect.stack()[0][3]}'
        return requestResult 
    
    return None

