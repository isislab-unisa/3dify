# 3Dify Cloud-native

Cloud-native 3Dify web application.

## Architecture

The architecture comprises a web application, a file store, and a NoSQL database.

1. The `web application` is built with the **Next.js** framework, which allows us to develop both the front-end and back-end using **TypeScript**.
   The front-end is designed as a Single-Page Application (SPA) and written in **React**, also taking advantage of the abstractions offered by Next.js.
   Another benefit of Next.js is the possibility to use **Next.js API Routes** to create a serverless back-end to optimize resource utilization.
2. **MinIO** is used as `file store` for persisting uploaded photos, generated avatars, etc.
3. For the `database`, the application leverages **MongoDB** capabilities for storing users' information and more.

![Architecture](assets/3dify_architecture.png 'Architecture')

## Getting Started

The easiest way to start the application is to run the development server:

```bash
npm run dev
```

Alternatively, run using Docker:

```bash
# build the image
docker build -t 3dify .

# run the container
docker run -d -p 3000:3000 --name 3dify 3dify
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
