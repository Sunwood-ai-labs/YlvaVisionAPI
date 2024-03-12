FROM python:3.11

WORKDIR /app

RUN apt -y update && apt -y upgrade
RUN apt -y install libopencv-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
