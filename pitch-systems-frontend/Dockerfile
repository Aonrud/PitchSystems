FROM node:22 as build

ENV NODE_ENV=production

WORKDIR /app

COPY package.json ./
COPY pnpm-lock.yaml ./

# pnpm must be installed as it doesn't come with the default image
RUN npm i -g pnpm
RUN pnpm i
COPY . ./

RUN pnpm build

FROM node:22

WORKDIR /app
COPY --from=build /app .

EXPOSE 4173

CMD ["node","build"]
