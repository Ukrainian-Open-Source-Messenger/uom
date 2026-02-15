# real-time-service/Dockerfile
FROM node:20

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE $APP_PORT

CMD ["sh", "-c", "npm run build && node dist/index.js"]
