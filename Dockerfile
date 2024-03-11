# install dependencies, only when needed
FROM node:20 AS deps
RUN mkdir -p /app
WORKDIR /app
COPY package*.json ./
RUN npm install

# rebuild the source code, only when needed
FROM node:20 AS builder
RUN mkdir -p /app
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# build image
FROM node:20 AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app ./
EXPOSE 3000
CMD ["npm", "run", "start"]