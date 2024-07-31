from fastapi import FastAPI
from pydantic import BaseModel
from imageProcess import process, extractLandmarks, open_base64_image
from textureManipulation import createCustomSkin
from cli.mh.genericCommandPy import sendCommand, sendCommandParameters
from fastapi.middleware.cors import CORSMiddleware

class Request(BaseModel):
    imageBase64: str | None = None
    gender : str | None = None
    age : float | None = None
    skinColor : int | None = None
    
class BuildRequest(BaseModel):
    sliders: dict | None = None

class Response(BaseModel):
    sliders: dict | None = None
    landmarks: list | None = None
    normalizedLandmarks: list | None = None
    zipFile64: str | None = None
    textureFile64: str | None = None

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/scanFace")
async def getLandmarks(request: Request) -> Response:
    imageBase64 = request.imageBase64
    #imageBase64 = imageBase64.split(",")[1]
    landmarks, normalizedLandmarks = extractLandmarks(imageBase64)
    return Response(landmarks=landmarks, normalizedLandmarks=normalizedLandmarks)

@app.post("/extractFeatures")
async def generateSliders(request: Request) -> Response:
    imageBase64 = request.imageBase64
    #imageBase64 = imageBase64.split(",")[1]
    sliders = process(imageBase64, request.gender, request.age)
    return Response(sliders=sliders)

@app.get("/downloadFbxZip")
async def downloadFbxZip() -> Response:
    data = sendCommand("exportFbx")
    return Response(zipFile64=data)
    
@app.post("/applyAndDownload")
async def applyAndDownload(request: BuildRequest) -> Response:
    sliders = request.sliders
    sendCommandParameters("applyModifiers", sliders)
    data = sendCommand("exportFbx")
    return Response(zipFile64=data)
    
@app.post("/getCustomSkin")
async def getCustomSkin(request: Request) -> Response:
    imageBase64 = request.imageBase64
    image = open_base64_image(imageBase64)
    data = createCustomSkin(skinColor=request.skinColor, gender=request.gender, age=request.age, image=image)
    return Response(textureFile64=data)
