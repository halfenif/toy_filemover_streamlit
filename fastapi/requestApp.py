import const
from RequestResult import RequestResult

def internalError(msg: str, method: str):
    requestResult = RequestResult()
    requestResult.result = const.RESULT_FAIL
    requestResult.msg = msg
    requestResult.method = method
    return requestResult