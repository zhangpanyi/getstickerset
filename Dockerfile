FROM python:3.7.2-alpine3.8

COPY getstickerset.py /getstickerset.py

RUN apk add build-base
RUN apk add libffi-dev zlib-dev jpeg-dev openssl-dev

RUN pip3 install webp
RUN pip3 install Pillow
RUN pip3 install progress
RUN pip3 install python-telegram-bot

RUN apk del build-base
RUN rm -rf /tmp/*
RUN rm -rf /root/.cache/*

ENTRYPOINT [ "python3", "getstickerset.py" ]
