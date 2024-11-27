FROM python:3.12-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y git openjdk-11-jdk libgdal-dev

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

COPY requirements.txt requirements.txt

RUN pip install uv
RUN uv pip install --no-cache-dir -r requirements.txt --system

COPY scripts/ .

ENTRYPOINT ["python", "teehr_ngen.py"]