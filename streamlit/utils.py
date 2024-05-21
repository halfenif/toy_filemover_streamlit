import base64
import const
import streamlit as st



# 기본------------------
def getPathEncode(path):
    if path == "":
        return None, ""
    
    try:
        return None, base64.urlsafe_b64encode(bytes(path, const.ENC_TYPE)).decode(const.ENC_TYPE)
    except Exception as e:
        st.write(f"Exception @ Streamlit > utils.py > getPathEncode{str(e)}")
        return "Error", None

