FROM node:14.18-alpine

RUN apk update && \
    apk upgrade

COPY dist/ /app

WORKDIR /app

RUN npm install --legacy-peer-deps && \
    npm rebuild node-sass

    #test1
    #test2


    
EXPOSE 3000

CMD npm start
