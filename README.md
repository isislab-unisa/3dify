## Table of Content
1. [Introduction](#introduction)
2. [Application Front End](#application-front-end)
3. [Architecture](#architecture)
4. [Application Deployement](#application-deployment)
5. [Run the Application Locally](#run-the-application-locally)
   1. [Prerequisites](#prerequisites)
      1. [Windows](#windows)
      2. [Linux](#linux)
      3. [MacOS](#macos)
   2. [Launch](#launch)
6. [Getting Started with Development](#getting-started-with-development)
     1. [Prerequisites](#prerequisites-1)
     2. [Launch](#launch-1)
8. [Where to apply changes](#where-to-apply-changes)
9. [3Dify Test Suite](#3dify-test-suite)

# Introduction
The 3Dify project aims to enable avatar creation using advanced AI and a modular software architecture. Such a modular architecture allows for flexible and scalable development, ensuring easy updates and improvements.

3dify allows users to create fully-animated 3D avatars by uploading a single picture of a face. Using AI, 3dify scans the face from the input photo, extracts its features and uses the [MakeHuman](http://www.makehumancommunity.org/) avatar generation suite to create 3D animated avatars based on the facial features extracted from the 3dify software modules.

3dify consists of 2 web applications.
1. a single page web application which allows authenticated users to browse previously generated avatars, upload new pictures and modify them. Once the picture is set, a "customize" button runs the Web GL application for preview and customization.

![Web Application](assets/WebAppScreen.png 'Web Application')

2. a Web GL application, built with Unity, that creates the avatar and renders the fully-animated 3d model result for preview. The application provides user interface controls to customize the output avatar by changing facial features.

![Web GL Application](assets/WebGLScreen.png 'Web GL Application')

Example of a generated avatar:

![Example](assets/AvatarComparison2.png 'Example')

# Application front end

The front end provides users with a gallery of pictures they have uploaded to generate their avatars. The gallery is proposed as a grid of photos to make it look familiar to users accustomed to picture galleries installed on their smartphones. Alongside the gallery, users are provided with a box to upload their pictures through drag-and-drop and selection from their computer.

Consider that a user uploads a picture either way; the platform shows users the update's progress to keep them informed about what is happening to avoid refreshes or other actions that could only worsen the user experience, even though loading a picture does not take much time. When the loading is complete, users can access the picture from the gallery, and by clicking on it, they can preview the picture and gain access to several features. Below the preview, they have an action bar with options such as zoom-in, zoom-out, flip horizontally and vertically, rotate in both directions and the most important one–the customization option, which is dedicated to avatar customization and rendering using the Unity-based front end.

The application does not support logging in yet, but it is already designed with the capabilities to do so, and this is why users can already see buttons for logging in and out. This functionality will be enabled in future versions using the MongoDB database.

The WebGL front-end, developed using the Unity game engine, allows users to preview an initial version of their avatar based on the image uploaded to the web application described above.

After initial facial feature inference and avatar generation, the application displays a high-fidelity rendering of the fully animated avatar. This avatar includes a mesh with attached materials and textures, as well as a skeleton for use in applications such as XR and video games.

If the user is not satisfied with the initial results, the application offers extensive customization of facial features, including the head, eyes, nose, hair, and other details, using the panel on the left.

Customization is done by adjusting position and size values using sliders or by selecting from graphical options (eyes, hair, etc.).

By pressing the Build button in the lower left corner, the user initiates the avatar generation pipeline. This process, which takes more than 10 seconds, sends the new face parameters to the backend services to generate a modified version of the avatar.

# Architecture

The application front end architecture comprises a web application, a file store, and a NoSQL database.

1. The `web application` is built with the **Next.js** framework, which allows us to develop both the front-end and back-end using **TypeScript**.
   The front-end is designed as a Single-Page Application (SPA) and written in **React**, also taking advantage of the abstractions offered by Next.js.
   Another benefit of Next.js is the possibility to use **Next.js API Routes** to create a serverless back-end to optimize resource utilization.
2. **MinIO** is used as `file store` for persisting uploaded photos, generated avatars, etc.
3. Part of the back-end is implemented in the **Python** language, which handles the facial feature extraction and communication with the Makehuman daemon
4. For the `database`, the application leverages **MongoDB** capabilities for storing users' information and more.
5. The `WebGL application` is built with the **Unity** game engine and the **C#** language and lets users customize and preview the avatar and download its 3D model.
6. The `avatar generation` is handled by a **Makehuman** process running in background. 

![Architecture](assets/3dify_architecture_release_2.png 'Architecture')

# Application deployment

The application consists of five docker containers:
- [3dify-makehuman](https://hub.docker.com/repository/docker/isislab/3dify-makehuman/general): The container that executes a customized version of MakeHuman that permits to elaborate the sliders value extracted from a photo into a rendered 3D avatar.
- [3dify-unity](https://hub.docker.com/repository/docker/isislab/3dify-unity/general): The container which starts a simple python HTTP web server which hosts the WebGL application for the avatar preview
- [3dify-python](https://hub.docker.com/repository/docker/isislab/3dify-python/general): Container containing the logic behind the conversion between facial landmarks and MakeHuman ’s parameters, as well as the logic connecting the application to MakeHuman for sending new sliders value and for exporting and downloading the final 3D model .FBX file.
- [filestore](https://hub.docker.com/r/minio/minio): Container including MinIO, an object storage application compatible with the Amazon S3 API
- [3dify-next](https://hub.docker.com/repository/docker/isislab/3dify-next/general): Containers based on this image start the web application for the avatar management front-end.

The deployment of these containers is coordinated by the [Docker Compose](https://github.com/isislab-unisa/3dify/blob/main/docker-compose.yml) configuration file.

# Run the Application Locally

## Prerequisites
#### Windows
For executing on Windows Systems it is necessary to install beforehand an X11 Server, we advise **VcXsrv Windows X Server** that can be found at the following [link](https://sourceforge.net/projects/vcxsrv/), as well as **Docker Desktop** at the following [link](https://www.docker.com/products/docker-desktop/).

The following are the preliminary steps for executing only for Windows Systems.

1. After having installed VcXsrv proceed to open with **XLaunch** 
2. Select **Multiple Windows** and specify 1 as **Display number**
3. Select **Start no client**
4. Ensure that **Disable access control** is checked
5. Click **Finish**
6. Open **Docker Desktop**
7. Proceed with the instruction for the launch with Docker Compose specified below.

#### Linux
For executing on Linux Systems it is just necessary to install **Docker Engine** by following the guide for your distro at the following [link](https://docs.docker.com/engine/). (**ATTENTION** Currently this version only work by using Docker Engine with sudo command and is not compatible with Docker Desktop for linux systems.)

The following are the preliminary steps for executing only for Linux Systems after having installed Docker Engine.

1. Open the terminal (Restart it if is the same terminal from which you have just installed Docker engine) and type:.
```bash
xhost +local:docker
```
2. Proceed with the instruction for the launch with Docker Compose specified below.
   
#### MacOs
For executing on MacOs Systems is necessary to install both an X11 server, we advise **XQuartz** downloadable from the following [link](https://www.xquartz.org/) and **Docker Desktop**, downloadable from the following [link](https://www.docker.com/products/docker-desktop/).

(**DISCLAIMER**: Currently on Apple Silicon Processors the software may present some slow down due to the translation layer from x64 to ARM.)

1. After having installed **XQuartz** proceed to open it.
2. Open a terminal and type:
```bash
      xhost +local:docker
      xhost + 127.0.0.1
```
3. Open the **docker-compose.yml** and comment the following line:
```bash
      - DISPLAY=${DISPLAY:-host.docker.internal:1}
```
4. And remove the comment from the following line:
```bash
      # - DISPLAY=host.docker.internal:0
```
5. Proceed with the instruction for the launch with Docker Compose specified below.

## Launch
Download the Docker Compose file at [https://github.com/isislab-unisa/3dify/blob/main/docker-compose.yml](https://github.com/isislab-unisa/3dify/blob/main/docker-compose.yml).

Launch all the containers required to run the application:

```bash
docker compose up -d
```

Stop all the containers of the application:

```bash
docker compose down
```

If the application is correctly deployed, it can be run by default at the link [http://localhost:3000/](http://localhost:3000/).

# Getting Started with Development

## Prerequisites
Follow the same instruction as specified above.

## Launch

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

If the application is correctly deployed, it can be run by default at the link [http://localhost:3000/](http://localhost:3000/).

## Where to Apply Changes?

- [/app/api](https://github.com/isislab-unisa/3dify/tree/main/app/api): in this folder you will find the code for the serverless APIs that power the application back end.
   - *genderAge*: which estimates the gender and the age of a person given a picture of the face.
   - *photos, uploadPhotos*: that lets the application read and write image files on the MinIO storage.

- [/app/components](https://github.com/isislab-unisa/3dify/tree/main/app/components): in this folder you will find the code for the UI elements of the application front end, such as the photos gallery.

- [/app/pythonServices](https://github.com/isislab-unisa/3dify/tree/main/app/pythonServices): in this folder you will find the code for the python-based back end.
   - *scanFace*: extracts the 478 landmarks that map the face of the input face portrayed in the image
   - *extractFeatures*: the outputs of genderAge and scanFace are processed to calculate facial parameters in terms of sizes and distances of all parts of the face (head, eyes, nose, mouth,...). Such parameters are numerical normalized in the [-1, 1] interval or a choice in an enumeration
   - *applyAndDownload*: communicates with the makehuman daemon which will in turn generate an avatar based on a series of facial parameters given in input

# 3Dify Test Suite
## Prerequisites
In order to proceed with the execution of the tests suite, it is necessary to:
1. Install miniforge at the following [link](https://github.com/conda-forge/miniforge)
2. Create a new environment named "makehuman" and activate it by typing
```bash
conda create -n makehuman && conda activate makehuman
```
3. Install in the environment all the packages inside "tests/requirements.txt" by using
```bash
pip install -r requirements.txt
```
4. Execute the test.bat or test.bash script
