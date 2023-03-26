FROM node:alpine3.11 as build

WORKDIR /app/frontend

COPY frontend ./

RUN npm install

CMD npm start

FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# install all requirements
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY backend /app/backend
COPY data /app/data

COPY --from=build /app/frontend/dist/agtern-client /app/frontend/dist/agtern-client

CMD [ "python3", "-m", "backend", "--dev", "--no-scrape" ]

EXPOSE 8000
