FROM node:14.18-alpine

RUN apk update && \
    apk upgrade

COPY . /app

WORKDIR /app

RUN npm install --legacy-peer-deps && \
    npm rebuild node-sass 
    #test9
    #test10
    #test11
EXPOSE 3000

CMD npm start
