FROM python:3.10-bullseye

WORKDIR /srv/http/boxbot

VOLUME [ "/data/memes", "/data/elotrix", "/data/offensive_memes.txt" ]

ENV TOKEN=""
ENV COMMAND_PREFIX="box::"

RUN apt update && apt install -y openjdk-17-jdk

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY JavaFormatter ./JavaFormatter/
RUN cd JavaFormatter && make all

COPY commands ./commands/
COPY main.py utils.py ./

CMD [ "python", "main.py" ]
