FROM tiangolo/uvicorn-gunicorn

RUN mkdir /fastapi

# COPY requirements.txt /fastapi


WORKDIR /fastapi

# 통상적인 방법
# RUN pip install -r requirements.txt

# SSL Error로 신뢰할수 있는 사이트를 강제로 지정하는 방법. 대충 사용한것만 기술
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org fastapi
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org pydantic
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org mutagen
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org pathlib
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org python-mpd2
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org pydantic_settings


COPY . /fastapi

EXPOSE 9001

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9001"]