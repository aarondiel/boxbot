FROM openjdk:17-slim AS JAVA_FORMATTER
WORKDIR /root/JavaFormatter
RUN apt update && apt install make

COPY JavaFormatter .
RUN make all

FROM python:3.11-slim
WORKDIR /srv/http/boxbot
RUN mkdir -p /data/memes
RUN mkdir -p /data/elotrix
RUN touch /data/offensive_memes.txt
VOLUME [ "/data/memes", "/data/elotrix", "/data/offensive_memes.txt" ]
ENV TOKEN=""
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY --from=JAVA_FORMATTER /root/JavaFormatter/bin JavaFormatter/bin
RUN apt update && apt install -y openjdk-17-jre-headless ffmpeg

COPY commands commands
COPY main.py utils.py ./
CMD [ "python", "main.py" ]
