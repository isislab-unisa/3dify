from fastapi import FastAPI
from pydantic import BaseModel
from imageProcess import process, extractLandmarks


class Request(BaseModel):
    imageBase64: str | None = None
    gender : float | None = None
    age : float | None = None

class Response(BaseModel):
    sliders: dict | None = None
    landmarks: list | None = None
    normalizedLandmarks: list | None = None

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/extractLandmarks")
async def getLandmarks(request: Request) -> Response:
    imageBase64 = request.imageBase64
    imageBase64 = imageBase64.split(",")[1]
    landmarks, normalizedLandmarks = extractLandmarks(imageBase64)
    return Response(landmarks=landmarks, normalizedLandmarks=normalizedLandmarks)

@app.post("/generateSliders")
async def generateSliders(request: Request) -> Response:
    imageBase64 = request.imageBase64
    imageBase64 = imageBase64.split(",")[1]
    sliders = process(imageBase64, request.gender, request.age)
    return Response(sliders=sliders)