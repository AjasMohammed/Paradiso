FROM node:20.8-bullseye-slim

WORKDIR /Paradiso/frontend

COPY package*.json ./

RUN npm install

COPY . .

CMD [ "npm", "start" ]