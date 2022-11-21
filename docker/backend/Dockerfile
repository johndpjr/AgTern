FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR ./app

# install all requirements
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY data ./data

COPY backend ./backend

CMD [ "python3", "-m", "backend", "--dev", "--no-scrape" ]

EXPOSE 8000
