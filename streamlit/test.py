import streamlit as st
from api import api_test

st.title('Streamlit-FastAPI Call Test')

if st.button('버튼을 클릭하세요'):
    st.write('버튼이 클릭되었습니다!')

    status_code, result = api_test()
    if status_code == 200:
        st.write('요청이 성공적으로 보내졌습니다.')
        st.write(result)
    else:
        st.write('요청을 보내는 중 문제가 발생했습니다. 상태 코드:', status_code)
