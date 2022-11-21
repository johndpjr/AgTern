FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY data ./

COPY backend ./

CMD [ "python3", "-m", "/app/backend", "--dev", "--no-scrape" ]

EXPOSE 8080
