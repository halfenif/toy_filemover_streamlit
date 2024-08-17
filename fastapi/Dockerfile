FROM python

RUN mkdir /fastapi

COPY requirements.txt /fastapi


WORKDIR /fastapi

# 통상적인 방법
RUN pip install -r requirements.txt


COPY . /fastapi

EXPOSE 9001

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9001"]
