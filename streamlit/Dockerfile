FROM python:3.9-slim

RUN mkdir /streamlit

#COPY requirements.txt /streamlit

WORKDIR /streamlit

# 통상적인 방법
#RUN pip install -r requirements.txt

# SSL Error로 신뢰할수 있는 사이트를 강제로 지정하는 방법. 대충 사용한것만 기술
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org streamlit
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org requests
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org requests-toolbelt
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org uuid

COPY . /streamlit

EXPOSE 9000

CMD ["streamlit", "run", "app.py", "--server.port","9000"]