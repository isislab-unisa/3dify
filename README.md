The 3Dify project aims to permit avatar creation using advanced AI and a modular software architecture. Such modular architecture allowed a flexible and scalable development, ensuring easy updates and improvement.

## Application front end

The front end provides users with a gallery of pictures they have uploaded to generate their avatars. The gallery is proposed as a grid of photos to make it look familiar to users accustomed to picture galleries installed on their smartphones. Alongside the gallery, users are provided with a box to upload their pictures through drag-and-drop and selection from their computer.

Consider that a user uploads a picture either way; the platform shows users the update's progress to keep them informed about what is happening to avoid refreshes or other actions that could only worsen the user experience, even though loading a picture does not take much time. When the loading is complete, users can access the picture from the gallery, and by clicking on it, they can preview the picture and gain access to several features. Below the preview, they have an action bar with options such as zoom-in, zoom-out, flip horizontally and vertically, rotate in both directions and the most important one–the customization option, which is dedicated to avatar customization and rendering using the Unity-based front end.

The application does not support logging in yet, but it is already designed with the capabilities to do so, and this is why users can already see buttons for logging in and out. This functionality will be enabled in future versions.

### Architecture

The application front end architecture comprises a web application, a file store, and a NoSQL database.

1. The `web application` is built with the **Next.js** framework, which allows us to develop both the front-end and back-end using **TypeScript**.
   The front-end is designed as a Single-Page Application (SPA) and written in **React**, also taking advantage of the abstractions offered by Next.js.
   Another benefit of Next.js is the possibility to use **Next.js API Routes** to create a serverless back-end to optimize resource utilization.
2. **MinIO** is used as `file store` for persisting uploaded photos, generated avatars, etc.
3. For the `database`, the application leverages **MongoDB** capabilities for storing users' information and more.

![Architecture](assets/3dify_architecture.png 'Architecture')

## Avatar customization and rendering WebGL web front-end

## Run the Application Locally

Download the Docker Compose file at [https://github.com/isislab-unisa/3dify/blob/main/docker-compose.yml](https://github.com/isislab-unisa/3dify/blob/main/docker-compose.yml).

Launch all the containers required to run the application:

```bash
docker compose up -d
```

Stop all the containers of the application:

```bash
docker compose down
```

## Getting Started with Development

Get the code at the repo [https://github.com/isislab-unisa/3dify/tree/main](https://github.com/isislab-unisa/3dify/tree/main).

Launch all the containers required to run the application in **development mode**:

```bash
docker compose -f dev.docker-compose.yml up -d
```

Monitor the application while developing to see your changes reflecting automatically:

```bash
docker compose -f dev.docker-compose.yml watch
```

Stop all the containers of the application:

```bash
docker compose -f dev.docker-compose.yml down
```

### Where to Apply Changes?