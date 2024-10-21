from fastapi import FastAPI, HTTPException
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
    
class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: int):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

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
    try:
        imageBase64 = request.imageBase64
        #imageBase64 = imageBase64.split(",")[1]
        landmarks, normalizedLandmarks = extractLandmarks(imageBase64)
        return Response(landmarks=landmarks, normalizedLandmarks=normalizedLandmarks)
    except Exception as e:
        raise CustomHTTPException(status_code=202, detail="Error extracting Landmarks from image", error_code=1001)

@app.post("/extractFeatures")
async def generateSliders(request: Request) -> Response:
    try:
        imageBase64 = request.imageBase64
        #imageBase64 = imageBase64.split(",")[1]
        sliders = process(imageBase64, request.gender, request.age)
        return Response(sliders=sliders)
    except Exception as e:
        raise CustomHTTPException(status_code=202, detail="Error extracting features from image", error_code=1002)

@app.get("/downloadFbxZip")
async def downloadFbxZip() -> Response:
    try:
        data = sendCommand("exportFbx")
        return Response(zipFile64=data)
    except Exception as e:
        raise CustomHTTPException(status_code=202, detail="Error downloading FBX zip", error_code=1003)
    
@app.post("/applyAndDownload")
async def applyAndDownload(request: BuildRequest) -> Response:
    try:
        sliders = request.sliders
        sendCommandParameters("applyModifiers", sliders)
        data = sendCommand("exportFbx")
        return Response(zipFile64=data)
    except Exception as e:
        raise CustomHTTPException(status_code=202, detail="Error applying modifiers and downloading FBX zip", error_code=1004)
    
@app.post("/getCustomSkin")
async def getCustomSkin(request: Request) -> Response:
    try:
        imageBase64 = request.imageBase64
        image = open_base64_image(imageBase64)
        data = createCustomSkin(skinColor=request.skinColor, gender=request.gender, age=request.age, image=image)
        return Response(textureFile64=data)
    except Exception as e:
        raise CustomHTTPException(status_code=202, detail="Error creating custom skin", error_code=1005)
