# 
FROM python:3.8-slim

# 
WORKDIR /code

# 
COPY ./custom_makehuman/requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y \
    python3-pyqt5 \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    libgl1 \
    libglu1-mesa \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \
    libxcb-xinput0 \
    mesa-utils \
    x11-apps \
    xvfb && rm -rf /var/lib/apt/lists/*
# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt PyOpenGL_accelerate
# 
COPY ./custom_makehuman /code/makehuman
COPY ./makehumanMonitor.py /code/makehumanMonitor.py
COPY ./makehumanDocs/makehuman /root/makehuman


EXPOSE 12345

RUN touch log.txt
RUN which xvfb-run

CMD ["sh", "-c", "xvfb-run -a -n 0 python makehumanMonitor.py"]
