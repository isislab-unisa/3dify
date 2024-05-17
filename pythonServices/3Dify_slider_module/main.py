from fastapi import FastAPI
from pydantic import BaseModel
from imageProcess import process


class Request(BaseModel):
    imageBase64: str | None = None


class Response(BaseModel):
    sliders: dict | None = None


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/generateSliders")
async def generateSliders(request: Request) -> Response:
    imageBase64 = request.imageBase64
    imageBase64 = imageBase64.split(",")[1]
    sliders = process(imageBase64)
    return Response(sliders=sliders)
