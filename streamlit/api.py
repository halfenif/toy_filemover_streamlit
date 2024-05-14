import requests
import streamlit as st
import const
import inspect
from config import URL_BACKEND

# interact with FastAPI endpoint
backend = URL_BACKEND


## Utils ----------------
def result_check(response: any):
    if response.status_code == 200:

        #Result Check
        try:
            result_state_str = response.json()["Result"]
            if(result_state_str == const.RESULT_FAIL):
                message = response.json()["Message"] + ' @ ' + response.json()["Method"]
                st.error(message, icon="🚨")
                return "", 500
            
            # 정상응답인경우
            return response.status_code, response.json()
        except:
            # Arrry에는 Result가 없다.
            return response.status_code, response.json()

    else:
        # Server에서 오류응답인경우
        message = "호출오류: Http Status Code is " + str(response.status_code)
        st.error(message, icon="🔥")        
        return response.status_code, ""
    
def request_exception(e: any, client_method: str):
    message = "호출오류:" + str(e) + ' @ ' + client_method
    st.error(message, icon="🔥")

## Method ----------------
def api_test():
    try:
        response = requests.get(backend + inspect.stack()[0][3], params={})
        return result_check(response)
    except requests.exceptions.RequestException as e:
        request_exception(e, inspect.stack()[0][3])

def list_folder_and_file_by_path(rootType: str, pathEncode: str):
    try:
        response = requests.get(backend + inspect.stack()[0][3], params={'rootType':rootType, 'pathEncode':pathEncode})
        return result_check(response)
    except requests.exceptions.RequestException as e:
        request_exception(e, inspect.stack()[0][3])

    
def file_read_taginfo_by_path(fileitem: any):
    try:
        response = requests.get(backend + inspect.stack()[0][3], params=fileitem)
        return result_check(response)
    except requests.exceptions.RequestException as e:
        request_exception(e, inspect.stack()[0][3])

def file_write_taginfo_by_path(tagitem: any):
    try:
        response = requests.get(backend + inspect.stack()[0][3], params=tagitem)
        return result_check(response)
    except requests.exceptions.RequestException as e:
        request_exception(e, inspect.stack()[0][3])