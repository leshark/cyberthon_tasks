FROM python:3.7-slim-buster

WORKDIR /server

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY server.py .

COPY wsgi.py .

CMD ["gunicorn", "-w", "2", "--bind", "0.0.0.0:5002", "wsgi:app"]