FROM node:alpine3.11 as frontend-image
WORKDIR /agtern/frontend
COPY ./frontend .
RUN npm install
RUN npm run build

FROM python:3.11 as backend-image
ENV PYTHONUNBUFFERED 1
WORKDIR /agtern
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader popular
COPY ./backend ./backend
COPY ./data ./data
COPY ./envs ./envs
COPY --from=frontend-image /agtern/frontend/dist/agtern-client /agtern/frontend/dist/agtern-client
ENTRYPOINT [ "python3", "-m", "backend" ]
CMD [ "python3", "-m", "backend", "--dev", "--no-scrape" ]
HEALTHCHECK CMD curl -f http://localhost:8000/ || exit 1
EXPOSE 8000
