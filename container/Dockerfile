FROM python:3.7-alpine
MAINTAINER Mark Jennings <jenningsm42@gmail.com>

COPY ./requirements.txt /server/
COPY ./setup.py /server/
COPY ./server /server/server
WORKDIR /server

RUN apk --update add git gcc musl-dev libffi-dev openssl-dev protobuf
RUN git clone https://github.com/jenningsm42/mini-mmo-client.git
RUN cp -r /server/mini-mmo-client/proto /server
RUN mkdir -p /server/server/proto
RUN protoc -I=./proto --python_out=./server/proto ./proto/*

RUN pip install -e . -r requirements.txt
EXPOSE 1337

ENTRYPOINT ["game-server"]
