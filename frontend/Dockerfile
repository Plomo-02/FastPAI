FROM node:20-slim

WORKDIR /app

COPY package.json ./

RUN yarn install --peers

EXPOSE 5173

CMD ["yarn", "dev"] 