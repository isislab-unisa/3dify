# 
FROM python:3.10-slim

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y libglib2.0-0 libgl1

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./3Dify-sliderModule /code/3Dify-sliderModule
COPY ./3Dify-sliderModule/models/.u2net /root/.u2net

EXPOSE 80
# 
CMD ["fastapi", "run", "3Dify-sliderModule/main.py", "--port", "80"]