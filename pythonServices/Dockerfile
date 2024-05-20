# 
FROM python:3.10

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install libgl1 -y

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./3Dify-sliderModule /code/3Dify-sliderModule

EXPOSE 80
# 
CMD ["fastapi", "run", "3Dify-sliderModule/main.py", "--port", "80"]