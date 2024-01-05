FROM node:14.18-alpine

RUN apk update && \
    apk upgrade

COPY . /app

WORKDIR /app

RUN npm install --legacy-peer-deps && \
    npm rebuild node-sass

EXPOSE 3000
#test1
#test2
#test3
#test4
#test5
#test6
#test7

CMD npm start
