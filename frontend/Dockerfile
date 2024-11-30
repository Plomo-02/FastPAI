FROM node:20-slim

WORKDIR /app

COPY package*.json /app/

RUN npm install
RUN npm install -g serve

COPY . /app/

RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "start"]
