docker images prune

docker pull python:3.9-slim
docker pull tiangolo/uvicorn-gunicorn

docker-compose build
docker-compose up
