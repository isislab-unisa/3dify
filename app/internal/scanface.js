//import vision from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3";
import {FaceLandmarker, FilesetResolver} from '@mediapipe/tasks-vision';
import * as faceapi from 'face-api.js';
import * as canvas from 'canvas';
import { changeFaceDetector, isFaceDetectionModelLoaded } from './faceDetectionControls';

const SSD_MOBILENETV1 = 'ssd_mobilenetv1'

// patch nodejs environment, we need to provide an implementation of
// HTMLCanvasElement and HTMLImageElement
const { Canvas, Image, ImageData } = canvas
faceapi.env.monkeyPatch({ Canvas, Image, ImageData })


function almost(a, b, delta = 0.000001){
    return Math.abs(a - b) < delta
}

function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
}

function clamp01(value) {
    return clamp(value, 0, 1);
}

function lerp(a, b, t) {
    return (1-t)*a + t*b
}

function inverseLerp(a, b, x){
    return clamp((x-a) / (b-a), 0, 1)
}

function map01tominus11(x){
    return x*2-1
}

//Calcola i limiti del quadrato di riferimento per l'estrazione delle feature
function calculateLimits(landmarks) {
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (let landmarkCategory of landmarks) {
        for (let landmark of landmarkCategory) {
            if (landmark.x < minX) minX = landmark.x;
            if (landmark.y < minY) minY = landmark.y;
            if (landmark.x > maxX) maxX = landmark.x;
            if (landmark.y > maxY) maxY = landmark.y;
        }
    }

    return { minX, minY, maxX, maxY };
}

function GetHtmlImageElement(imgBase64, width)
{
    let img = "<img id=\"image\" src=\"" + imgBase64 + "\" style=\"max-width: " + width + "px;\">";
    let image = new Image();
    image.src = imgBase64;
    return image;
}

/*
const vision = await FilesetResolver.forVisionTasks(
    // path/to/wasm/root
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
  );
  */

// const {FaceLandmarker, FilesetResolver, DrawingUtils} = vision;

let vision;
let faceLandmarker;

//Carica il modello e la libreria di mediaPipe ed imposta i parametri per la rilevazione dei landmark del volto
async function createFaceLandmarker(){

    const filesetResolver = await FilesetResolver.forVisionTasks(
        "@mediapipe/tasks-vision/wasm"
    );

    faceLandmarker = await FaceLandmarker.createFromOptions(filesetResolver, {
        baseOptions:{
            modelAssetPath: "/MediaPipe_Models/face_landmarker.task",
            delegate: "GPU"
        },
        outputFaceBlendshapes: true,
        runningMode: "IMAGE",
        numFaces: 1,
    });
}
//await createFaceLandmarker();

// inputImg = html <img> element containing input image with width and height
export async function GetLandmarksFromPhoto(base64img, widthImg)
{
    vision = (await import("@mediapipe/tasks-vision"));
    await createFaceLandmarker();

    const inputImg = GetHtmlImageElement(base64img, widthImg)
    await changeFaceDetector(SSD_MOBILENETV1)
    await faceapi.loadFaceLandmarkModel('http://localhost:3000/weights/')
    await faceapi.nets.ageGenderNet.load('http://localhost:3000/weights/')
    //const inputImgEl = $('#inputImg').get(0)

    //FaceAPI for gender and age
    if (!isFaceDetectionModelLoaded()) {
        console.log("Face detection model not loaded")
        return
    }

    const options = faceapi.SsdMobilenetv1Options(0.5)

    const faceAPIResults = await faceapi.detectAllFaces(inputImg, options).withFaceLandmarks()
        .withAgeAndGender()


    let gender = faceAPIResults[0].gender
    let genderValue = 0.0
    if (gender.toLowerCase() == "male") {
        genderValue = 1.0
    }
    //makeHumanParameters["modifier macrodetails/Gender"] = genderValue.toString()

    let age = faceAPIResults[0].age
    let ageValue
    if (age <= 25.0) {
        ageValue = inverseLerp(0, 25, age) * 0.5
    }
    else {
        ageValue = inverseLerp(25, 99, age) * 0.5 + 0.5
    }
    //makeHumanParameters["modifier macrodetails/Age"] = "0.500000";


    console.log("GENDER : " + gender)
    console.log("AGE : " + age)


    if(!vision){
        console.log("faceLandmarker not ready");
        return;
    }

    //Rilevazione misure della testa
    // const { spawn} = require('child_process');
    // const python = spawn("python", )

    //Se presente rimuove un canvas con le mesh generate precedentemente
    /*const oldCanvas = document.getElementById("overlay");
    if(oldCanvas){
        oldCanvas.parentNode.removeChild(oldCanvas);
    }*/

    //Rileva i landmark del volto e li disegna su un canvas creato appositamente
    console.log(faceLandmarker)
    const faceLandmarkerResult = faceLandmarker.detect(inputImg);
    /*const canvas = document.createElement("canvas");
    canvas.setAttribute("class", "canvas");
    canvas.setAttribute("id", "overlay");
    canvas.setAttribute("width", inputImg.width + "px");
    canvas.setAttribute("height", inputImg.height + "px");
    canvas.style.left = "0px";
    canvas.style.top = "0px";
    canvas.style.width = "${inputImg.width}px";
    canvas.style.height = "${inputImg.height}px";*/

    //const ctx = drawMediaPipeLandmarks(inputImg, canvas, faceLandmarkerResult);
    

    console.log(faceLandmarkerResult.faceLandmarks);
    let limits = calculateLimits(faceLandmarkerResult.faceLandmarks);
    
    //Disegna un quadrato di riferimento intorno alla mesh creata    
    let width = (limits.maxX - limits.minX) * inputImg.width;
    let height = (limits.maxY - limits.minY) * inputImg.height;

    let squareSize = Math.max(width, height);

    //Angolo in alto a sinistra del quadrato di riferimento
    let startXUpSX = limits.minX * inputImg.width + (width - squareSize) / 2;
    let startYUpSX = limits.minY * inputImg.height + (height - squareSize) / 2;

    //Angolo in basso a sinistra del quadrato di riferimento
    let startX = startXUpSX;
    let startY = startYUpSX + squareSize;

    /*
    ctx.beginPath();
    ctx.rect(startXUpSX, startYUpSX, squareSize, squareSize);
    ctx.rect(startX, startY, 4, 4)
    ctx.strokeStyle = "red";
    ctx.stroke();*/

    //Normalizza i valori dei landmark all'interno del quadrato di riferimento
    let normalizedLandmarks = [];
    for (const landmarks of faceLandmarkerResult.faceLandmarks){
        normalizedLandmarks.push([]);
        for (const landmark of landmarks){
            normalizedLandmarks[normalizedLandmarks.length - 1].push({
                x: (landmark.x - startX / canvas.width) / (squareSize / canvas.width),
                y: (landmark.y - startY / canvas.height) / (squareSize / canvas.height),
                z: landmark.z - (startX / canvas.width)
            });
        }
    }

    return {landmarks: faceLandmarkerResult.faceLandmarks, normalizedLandmarks: normalizedLandmarks, age: 0.5, gender: genderValue};
}