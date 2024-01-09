FROM node:14.21.3-alpine

RUN apk update && \
    apk upgrade

COPY . /app

WORKDIR /app

#test1

RUN npm install --legacy-peer-deps && \
    npm rebuild node-sass

EXPOSE 3000

CMD npm start
