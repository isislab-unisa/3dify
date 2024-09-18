from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pandas as pd
from const import (nosePoints, faceShapePoints, rightEyePoints, rightEyeBrowPoints,
                   leftEyePoints, leftEyeBrowPoints, lipsPoints, points, max_width, jawPoints, foreheadPoints, templePoints, cheeksPoints, noseCurvePoints, chinPoints)
from faceFeatures import calculateFaceFeatureDistances, normalizeminus11, reset_normalizedDistanceDictionary
import base64
# from faceShapeFeatures import inferFaceShapeSliders
import traceback
import os



def imshow(img):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(img)
    return ax


def draw_landmarks_on_image(rgb_image, detection_result):
    face_landmarks_list = detection_result.face_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected faces to visualize.
    for idx in range(len(face_landmarks_list)):
        face_landmarks = face_landmarks_list[idx]

        # Draw the face landmarks.
        face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        face_landmarks_proto.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x, y=landmark.y, z=landmark.z
                )
                for landmark in face_landmarks
            ]
        )

        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style(),
        )
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style(),
        )
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_iris_connections_style(),
        )

    return annotated_image


def plot_face_blendshapes_bar_graph(face_blendshapes):
    # Extract the face blendshapes category names and scores.
    face_blendshapes_names = [
        face_blendshapes_category.category_name
        for face_blendshapes_category in face_blendshapes
    ]
    face_blendshapes_scores = [
        face_blendshapes_category.score
        for face_blendshapes_category in face_blendshapes
    ]
    # The blendshapes are ordered in decreasing score value.
    face_blendshapes_ranks = range(len(face_blendshapes_names))

    fig, ax = plt.subplots(figsize=(12, 12))
    bar = ax.barh(
        face_blendshapes_ranks,
        face_blendshapes_scores,
        label=[str(x) for x in face_blendshapes_ranks],
    )
    ax.set_yticks(face_blendshapes_ranks, face_blendshapes_names)
    ax.invert_yaxis()

    # Label each bar with values
    for score, patch in zip(face_blendshapes_scores, bar.patches):
        plt.text(
            patch.get_x() + patch.get_width(), patch.get_y(), f"{score:.4f}", va="top"
        )

    ax.set_xlabel("Score")
    ax.set_title("Face Blendshapes")
    plt.tight_layout()
    plt.show()
    
def initializeMediaPipe():
    parent_dir = os.path.join(os.getcwd(), "..")
    up_dir = os.listdir(parent_dir)
    model_path = ""
    if ".dockerenv" in up_dir:
        print("Running in Docker")
        model_path = r"3Dify-sliderModule/mediapipe_models/face_landmarker_v2_with_blendshapes.task"
    else:
        print("Running locally")
        model_path = r"./mediapipe_models/face_landmarker_v2_with_blendshapes.task"

    try:
        base_options = python.BaseOptions(
            # model_asset_path=r"3Dify-sliderModule/mediapipe_models/face_landmarker_v2_with_blendshapes.task"
            # model_asset_path=r"./mediapipe_models/face_landmarker_v2_with_blendshapes.task"
            model_asset_path = model_path
        )
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces = 1,
            min_face_presence_confidence = 0.5,
        )
        detector = vision.FaceLandmarker.create_from_options(options)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize MediaPipe: {e}")
    return detector


def calculate_limits(landmarks):
    min_x, min_y, max_x, max_y = (
        float("inf"),
        float("inf"),
        float("-inf"),
        float("-inf"),
    )
    for landmark in landmarks:
        if landmark.x < min_x:
            min_x = landmark.x
        if landmark.y < min_y:
            min_y = landmark.y
        if landmark.x > max_x:
            max_x = landmark.x
        if landmark.y > max_y:
            max_y = landmark.y

    return {"minX": min_x, "minY": min_y, "maxX": max_x, "maxY": max_y}

def open_base64_image(imageBase64):
    try:
        img_bytes = base64.b64decode(imageBase64)
        img_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid imageBase64")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
    except cv2.error as e:
        raise RuntimeError(f"Invalid imageBase64 : {e}")

def extractLandmarks(imgBase64):
    detector = initializeMediaPipe()
    img = open_base64_image(imgBase64)
    # img = cv2.imread(imgPath)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # imshow(img)
    global skipped
    try:
        original_height, original_width = img.shape[:2]
    except Exception as e:
        print("Failed Loading Image Shape")
        traceback.print_exc()
        return
    if original_width > max_width:
        scale = max_width / float(original_width)
        new_height = int(original_height * scale)
        img = cv2.resize(img, (max_width, new_height))
    # img = cv2.imread("Senza titolo.png")
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

    # STEP 4: Detect face landmarks from the input image.
    detection_result = detector.detect(image)

    # STEP 5: Process the detection result. In this case, visualize it.
    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)

    image_height, image_width, channels = annotated_image.shape

    try:
        landmarks = detection_result.face_landmarks[0]
    except Exception as e:
        # print("SKIPPED NO LANDMARKS")
        raise ValueError("No face detected")

    limits = calculate_limits(landmarks)

    width = (limits["maxX"] - limits["minX"]) * image_width
    height = (limits["maxY"] - limits["minY"]) * image_height

    square_size = max(width, height)

    # Angolo in alto a sinistra del quadrato di riferimento
    start_x_up_sx = limits["minX"] * image_width + (width - square_size) / 2
    start_y_up_sx = limits["minY"] * image_height + (height - square_size) / 2

    # Angolo in basso a sinistra del quadrato di riferimento
    # start_x_down_sx = limits["minX"] * image_width
    # start_y_down_sx = limits["maxY"] * image_height - square_size

    start_x_down_sx = start_x_up_sx
    start_y_down_sx = start_y_up_sx + square_size

    cv2.rectangle(
        annotated_image,
        (int(start_x_up_sx), int(start_y_up_sx)),
        (int(start_x_up_sx + square_size), int(start_y_up_sx + square_size)),
        (0, 255, 0),
        1,
    )
    cv2.circle(
        annotated_image,
        (int(start_x_down_sx), int(start_y_down_sx)),
        radius=5,
        color=(0, 0, 255),
        thickness=1,
    )

    normalizedLandmarks = []
    for lm in landmarks:
        normalizedLandmarks.append(
            {
                "x": (lm.x - start_x_down_sx / image_width)
                / (square_size / image_width),
                "y": (lm.y - start_y_down_sx / image_height)
                / (square_size / image_height),
                "z": lm.z - (start_x_down_sx / image_width),
            }
        )
    
    return landmarks, normalizedLandmarks


def process(imgBase64, gender, age):
    reset_normalizedDistanceDictionary()    
    landmarks, normalizedLandmarks = extractLandmarks(imgBase64)

    noseCoord = []
    faceShapeCoord = []
    rightEyeCoord = []
    rightEyeBrowCoord = []
    leftEyeCoord = []
    leftEyeBrowCoord = []
    lipsCoord = []
    cheeksCoord = []
    foreheadCoord = []
    jawCoord = []
    templeCoord = []
    noseCurveCoord = []
    chinCoord = []
    
    coord = {
        "noseCoord": noseCoord,
        "faceShapeCoord": faceShapeCoord,
        "rightEyeCoord": rightEyeCoord,
        "rightEyeBrowCoord": rightEyeBrowCoord,
        "leftEyeCoord": leftEyeCoord,
        "leftEyeBrowCoord": leftEyeBrowCoord,
        "lipsCoord": lipsCoord,
        "cheeksCoord": cheeksCoord,
        "foreheadCoord": foreheadCoord,
        "jawCoord": jawCoord,
        "templeCoord": templeCoord,
        "noseCurveCoord": noseCurveCoord,
        "chinCoord": chinCoord,  
    }

    for p in points:
        for i in range(len(p)):
            lm1 = normalizedLandmarks[p[i]]
            color = (0, 0, 0)

            if p is nosePoints:
                color = (255, 0, 0)
                noseCoord.append(lm1)
            elif p is faceShapePoints:
                color = (0, 255, 0)
                faceShapeCoord.append(lm1)
            elif p is rightEyePoints:
                color = (0, 0, 255)
                rightEyeCoord.append(lm1)
            elif p is rightEyeBrowPoints:
                color = (0, 255, 255)
                rightEyeBrowCoord.append(lm1)
            elif p is leftEyePoints:
                color = (0, 0, 255)
                leftEyeCoord.append(lm1)
            elif p is leftEyeBrowPoints:
                color = (0, 255, 255)
                leftEyeBrowCoord.append(lm1)
            elif p is lipsPoints:
                color = (255, 255, 255)
                lipsCoord.append(lm1)
            elif p is jawPoints:
                color = (255, 255, 0)
                jawCoord.append(lm1)
            elif p is templePoints:
                color = (255, 0, 255)
                templeCoord.append(lm1)
            elif p is cheeksPoints:
                color = (255, 0, 255)
                cheeksCoord.append(lm1)
            elif p is foreheadPoints:
                color = (255, 0, 255)
                foreheadCoord.append(lm1)
            elif p is noseCurvePoints:
                color = (255, 0, 255)
                noseCurveCoord.append(lm1)
            elif p is chinPoints:
                color = (255, 0, 255)
                chinCoord.append(lm1)
                
            # x1 = int(lm1["x"] * square_size + start_x_down_sx)
            # y1 = int(lm1["y"] * square_size + start_y_down_sx)

            # cv2.rectangle(annotated_image, (x1, y1), (x1 + 2, y1 + 2), color, -1)

    # cv2_imshow(cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
    # imshow(annotated_image)

    distance_dictionary = {}
    normalized_distance_dictionary = calculateFaceFeatureDistances(normalizedLandmarks, distance_dictionary, faceShapeCoord, noseCoord, lipsCoord, rightEyeCoord, leftEyeCoord,
                                  rightEyeBrowCoord, leftEyeBrowCoord, jawCoord, templeCoord, cheeksCoord, foreheadCoord, noseCurveCoord, chinCoord, gender)
    
    makeHumanParameters = {}
    
    genderValue = 0.0 if gender == "female" else 1.0
    
    makeHumanParameters["modifier head/head-age-decr|incr"] = str(normalizeminus11(age, 0.0, 100.0))
    makeHumanParameters["modifier macrodetails/Gender"] = str(genderValue)
    # makeHumanParameters["modifier forehead/forehead-scale-vert-decr|incr"] = "-0.25"
    
    skins = {
        "male": {
            "young": "skins/middleage_caucasian_male/middleage_caucasian_male.mhmat",
            "middleAge": "skins/middleage_caucasian_male/middleage_caucasian_male.mhmat",
            "old": "skins/old_caucasian_male/old_caucasian_male.mhmat",
        },
        "female": {
            "young": "skins/middleage_caucasian_female/middleage_caucasian_female.mhmat",
            "middleAge": "skins/middleage_caucasian_female/middleage_caucasian_female.mhmat",
            "old": "skins/old_caucasian_female/old_caucasian_female.mhmat",
        },
    }
    
    makeHumanParameters["skinMaterial"] = skins[gender]["young" if age < 28 else "middleAge" if age < 60 else "old"]
    
    for key in normalized_distance_dictionary.keys():
        makeHumanParameters["modifier " + key] = str(normalized_distance_dictionary[key])
        print("modifier " + key + " " + str(normalized_distance_dictionary[key]))
        
    # faceShapeSliders = inferFaceShapeSliders(imgBase64, gender)
    # for key in faceShapeSliders.keys():
    #     makeHumanParameters["modifier " + key] = str(faceShapeSliders[key])

    makeHumanParameters["skeleton"] = "default_no_toes.mhskel";
    makeHumanParameters["eyelashes"] = "Eyelashes01 d533836f-13ad-4836-8b65-051108253cd2";
    makeHumanParameters["eyebrows"] = "eyebrow001 9c81ec3a-faa5-4c94-9cdb-992300ba3084";
    makeHumanParameters["eyes"] = "HighPolyEyes 2c12f43b-1303-432c-b7ce-d78346baf2e6";
    makeHumanParameters["material HighPolyEyes"] = "2c12f43b-1303-432c-b7ce-d78346baf2e6 eyes/materials/brownlight.mhmat";
    makeHumanParameters["material eyebrow001"] = "9c81ec3a-faa5-4c94-9cdb-992300ba3084 eyebrow001.mhmat";
    makeHumanParameters["material Eyelashes01"] = "d533836f-13ad-4836-8b65-051108253cd2 eyelashes01.mhmat";
        
    return makeHumanParameters

