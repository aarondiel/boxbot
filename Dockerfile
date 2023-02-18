FROM python:3.10-bullseye

WORKDIR /srv/http/BoxBot

VOLUME [ "/data/memes", "/data/elotrix" ]

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY commands ./commands/
COPY JavaFormatter ./JavaFormatter/
COPY main.py utils.py settings.json offensive_memes.txt ./

ENV TOKEN=""
ENV COMMAND_PREFIX="box::"

CMD [ "python", "main.py" ]
