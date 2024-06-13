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

# install python 
RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-full
RUN apt-get upgrade -y
RUN pip --version
RUN python3 -m pip install --break-system-packages --no-cache-dir --upgrade numpy python-dotenv
RUN python3 --version

ENV NODE_ENV production

COPY --from=builder /app ./
EXPOSE 3000
CMD ["npm", "run", "start"]