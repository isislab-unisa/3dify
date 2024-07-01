# 
FROM python:3.10

# 
WORKDIR /code

# 
COPY ./BuildWebGL /code/

EXPOSE 8000
# 
CMD ["python", "-m", "http.server"]