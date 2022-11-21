FROM node:alpine3.11 as build

WORKDIR /app

COPY ./ ./

RUN npm install

RUN npm run build

FROM nginx:latest

COPY --from=build /app/dist/agtern-client /usr/share/nginx/html

EXPOSE 80
