#To execute (from 3dify-sliderModule folder): python -m pytest -v

import pytest
from fastapi.testclient import TestClient
from main import app, Request, BuildRequest, Response
import base64
import os
import zipfile

client = TestClient(app)

correctContent = ""
wrongContent = ""
noFace = ""
lowRes = ""

with open(r"./test_file/correctImage.txt", "r") as file:
    correctContent = file.read()
    
with open(r"./test_file/wrongImage.txt", "r") as file:
    wrongContent = file.read()
    
with open(r"./test_file/noFace.txt", "r") as file:
    noFace = file.read()
    
with open(r"./test_file/lowRes.txt", "r") as file:
    lowRes = file.read()

    
def test_scanFace_noImage():
    request_data = {
        "imageBase64" : wrongContent,
        "gender" : "male",
        "age" : 20,
        "skinColor" : 1
    }
    with pytest.raises(ValueError, match="Invalid imageBase64"):
        response = client.post("/scanFace", json=request_data)
        
def test_scanFace_correctImage():
    request_data = {
        "imageBase64" : correctContent,
        "gender" : "male",
        "age" : 20,
        "skinColor" : 1
    }
    response = client.post("/scanFace", json=request_data)
    assert response.status_code == 200
    assert "landmarks" in response.json()
    assert "normalizedLandmarks" in response.json()
    assert len(response.json()["landmarks"]) > 0
    assert len(response.json()["normalizedLandmarks"]) > 0
    
def test_scanFace_noFace():
    request_data = {
        "imageBase64" : noFace,
        "gender" : "male",
        "age" : 20,
        "skinColor" : 1
    }
    with pytest.raises(ValueError, match="No face detected"):
        response = client.post("/scanFace", json=request_data)

def test_extractFeatures_noImage():
    request_data = {
        "imageBase64" : wrongContent,
        "gender" : "male",
        "age" : 20,
        "skinColor" : 1
    }
    with pytest.raises(ValueError, match="Invalid imageBase64"):
        response = client.post("/extractFeatures", json=request_data)
        
def test_extractFeatures_correctImage():
    request_data = {
        "imageBase64" : correctContent,
        "gender" : "male",
        "age" : 20,
        "skinColor" : 1
    }
    response = client.post("/extractFeatures", json=request_data)
    assert response.status_code == 200
    assert "sliders" in response.json()
    assert len(response.json()["sliders"]) > 0
    
def test_extractFeatures_noFace():
    request_data = {
        "imageBase64" : noFace,
        "gender" : "male",
        "age" : 20,
        "skinColor" : 1
    }
    with pytest.raises(ValueError, match="No face detected"):
        response = client.post("/extractFeatures", json=request_data)
        
def test_extractFeatures_lowRes():
    request_data = {
        "imageBase64" : lowRes,
        "gender" : "male",
        "age" : 20,
        "skinColor" : 1
    }
    response = client.post("/extractFeatures", json=request_data)
    assert response.status_code == 200
    assert "sliders" in response.json()
    assert len(response.json()["sliders"]) > 0
    
def test_customSkin_noImage():
    request_data = {
        "imageBase64" : wrongContent,
        "gender" : "male",
        "age" : 20,
        "skinColor" : 1
    }
    with pytest.raises(ValueError, match="Invalid imageBase64"):
        response = client.post("/getCustomSkin", json=request_data)
        
def test_applyAndDownload(tmp_path):
    request_data = {
        "sliders": {
            "modifier head/head-age-decr|incr": "-0.4",
        }
    }
    response = client.post("/applyAndDownload", json=request_data)
    assert response.status_code == 200
    assert "zipFile64" in response.json()
    assert len(response.json()["zipFile64"]) > 0
    zipFile64 = response.json()["zipFile64"] 
    zipData = base64.b64decode(zipFile64)
    print(tmp_path)
    os.makedirs(os.path.join(tmp_path, "zipContent"), exist_ok=True)
    with open(os.path.join(tmp_path, "3Dify.zip"), "wb") as file:
        file.write(zipData)
    with zipfile.ZipFile(os.path.join(tmp_path, "3Dify.zip"), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(tmp_path, "zipContent"))
    zipContentDir = os.path.join(os.path.join(tmp_path, "zipContent"), "myHuman")
    assert os.path.exists(os.path.join(zipContentDir, "myHuman.fbx"))
    assert os.path.exists(os.path.join(zipContentDir, "textures"))
    
# def test_applyAndDownload_noMakehuman():
#     request_data = {
#         "sliders": {
#             "modifier head/head-age-decr|incr": "-0.4",
#         }
#     }
#     with pytest.raises(RuntimeError, match="Could not connect to Makehuman Daemon"):
#         response = client.post("/applyAndDownload", json=request_data)    


# def test_failedMediapipeInitialization():
#     request_data = {
#         "imageBase64" : correctContent,
#         "gender" : "male",
#         "age" : 20,
#         "skinColor" : 1
#     }
#     with pytest.raises(RuntimeError, match="Failed to initialize MediaPipe:"):
#         response = client.post("/extractFeatures", json=request_data)
