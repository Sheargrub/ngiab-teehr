FROM python:3.10-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y git openjdk-11-jdk

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY scripts/ .

ENTRYPOINT ["python", "teehr_ngen.py"]