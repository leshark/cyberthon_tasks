FROM python:3.7-slim-buster

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y socat

COPY server.py .

CMD socat -dd -T 60 TCP-LISTEN:5003,reuseaddr,fork EXEC:'python server.py'