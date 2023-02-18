FROM python:3.10-bullseye

WORKDIR /srv/http/BoxBot

VOLUME [ "/data/memes", "/data/elotrix" ]

ENV TOKEN=""
ENV COMMAND_PREFIX="box::"

RUN apt update && apt install -y openjdk-17-jdk

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY JavaFormatter ./JavaFormatter/
RUN cd JavaFormatter && make all

COPY commands ./commands/
COPY main.py utils.py offensive_memes.txt ./


CMD [ "python", "main.py" ]
