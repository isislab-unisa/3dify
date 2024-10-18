from const import limits

normalizedDistanceDictionary = {}

def midpoint(point1x, point1y, point2x, point2y):
    return {"x": (point1x + point2x) / 2, "y": (point1y + point2y) / 2}

def normalize(value, min, max):
    return (value - min) / (max - min);

def reset_normalizedDistanceDictionary():
    global normalizedDistanceDictionary
    normalizedDistanceDictionary = {}


def normalizeminus11(value, min, max):
    return 2 * ((value - min) / (max - min)) - 1;


def reverse_normalizeminus11(value, min_value, max_value):
    return (2 * ((value - min_value) / (max_value - min_value)) - 1) * -1

def normalizeCustomLimits(value, min_value, max_value, new_min, new_max):
    normalized_value = (value - min_value) / (max_value - min_value) * (new_max - new_min) + new_min
    return normalized_value


def calculate_forehead(faceShapeCoord, noseCoord, distanceDictionary, gender):
    distanceForehead = abs(faceShapeCoord[1]["y"] - noseCoord[1]["y"])
    distanceDictionary["distanceForehead"] = distanceForehead


def calculateChin(normalizedLandmarks, distanceDictionary, faceShapeCoord, lipsCoord, chinCoord, gender):
    chinSX = normalizedLandmarks[149]
    chinDX = normalizedLandmarks[378]

    distanceChin = abs(chinSX["x"] - chinDX["x"])
    distanceDictionary["distanceChin"] = distanceChin
    normalizedDistanceDictionary["chin/chin-width-decr|incr"] = normalizeminus11(distanceChin, limits[gender]["distanceChin"][0], limits[gender]["distanceChin"][1]);

    distanceChinLips = abs(faceShapeCoord[0]["y"] - lipsCoord[0]["y"])
    distanceDictionary["distanceChinLips"] = distanceChinLips
    
    chinDepth = abs(chinCoord[0]["z"] + chinCoord[1]["z"] + chinCoord[2]["z"] + chinCoord[3]["z"])/4
    distanceDictionary["chinDepth"] = chinDepth
    print("Chin Depth: ", chinDepth)
    if gender == "female":
        normalizedDistanceDictionary["chin/chin-prominent-decr|incr"] = normalizeminus11(chinDepth, limits[gender]["chinDepth"][0], limits[gender]["chinDepth"][1])
        if normalizedDistanceDictionary["chin/chin-prominent-decr|incr"] > 0.35:
            normalizedDistanceDictionary["chin/chin-prominent-decr|incr"] = 0.25
    else:
        normalizedDistanceDictionary["chin/chin-prominent-decr|incr"] = 0.25

def calculateFaceShape(faceShapeCoord, distanceDictionary, gender):
    distanceUpperFace = abs(faceShapeCoord[2]["x"] - faceShapeCoord[3]["x"])
    distanceDictionary["distanceUpperFace"] = distanceUpperFace

    distanceLeftLowerFace = abs(faceShapeCoord[2]["x"] - faceShapeCoord[4]["x"])
    distanceRightLowerFace = abs(faceShapeCoord[3]["x"] - faceShapeCoord[5]["x"])
    meanDistanceLowerFace = (distanceLeftLowerFace + distanceRightLowerFace) * 0.5
    distanceDictionary["meanDistanceLowerFace"] = meanDistanceLowerFace
    normalizedDistanceDictionary["head/head-fat-decr|incr"] = normalizeminus11(meanDistanceLowerFace, limits[gender]["meanDistanceLowerFace"][0], limits[gender]["meanDistanceLowerFace"][1])

    distanceUpDownFace = abs(faceShapeCoord[0]["y"] - faceShapeCoord[1]["y"])
    distanceDictionary["distanceUpDownFace"] = distanceUpDownFace


def calculateNose(noseCoord, noseCurveCoord, faceShapeCoord, distanceDictionary, normalizedLandmarks, gender):
    distanceLowNoseChin = abs(noseCoord[0]["y"] - faceShapeCoord[0]["y"])
    distanceDictionary["distanceLowNoseChin"] = distanceLowNoseChin
    normalizedDistanceDictionary["nose/nose-trans-down|up"] = normalizeminus11(distanceLowNoseChin, limits[gender]["distanceLowNoseChin"][0], limits[gender]["distanceLowNoseChin"][1])


    distanceLowHighNose = abs(noseCoord[1]["y"] - noseCoord[0]["y"])
    distanceDictionary["distanceLowHighNose"] = distanceLowHighNose
    normalizedDistanceDictionary["nose/nose-scale-vert-decr|incr"] = normalizeminus11(distanceLowHighNose, limits[gender]["distanceLowHighNose"][0], limits[gender]["distanceLowHighNose"][1])


    distanceNostrilNose = abs(noseCoord[2]["x"] - noseCoord[3]["x"])
    distanceDictionary["distanceNostrilNose"] = distanceNostrilNose
    normalizedDistanceDictionary["nose/nose-scale-horiz-decr|incr"] = normalizeminus11(distanceNostrilNose, limits[gender]["distanceNostrilNose"][0], limits[gender]["distanceNostrilNose"][1]) 
    normalizedDistanceDictionary["nose/nose-width3-decr|incr"] = normalizeminus11(distanceNostrilNose, limits[gender]["distanceNostrilNose"][0], limits[gender]["distanceNostrilNose"][1])


    nostril1SX = normalizedLandmarks[59]
    nostril1DX = normalizedLandmarks[238]

    nostril2SX = normalizedLandmarks[458]
    nostril2DX = normalizedLandmarks[289]

    distanceNostril1 = abs(nostril1SX["x"] - nostril1DX["x"])
    distanceNostril2 = abs(nostril2SX["x"] - nostril2DX["x"])

    meanDistanceNostril = (distanceNostril1 + distanceNostril2) * 0.5
    distanceDictionary["meanDistanceNostril"] = meanDistanceNostril
    normalizedDistanceDictionary["nose/nose-flaring-decr|incr"] = normalizeminus11(meanDistanceNostril, limits[gender]["meanDistanceNostril"][0], limits[gender]["meanDistanceNostril"][1]);
    normalizedDistanceDictionary["nose/nose-nostrils-width-decr|incr"] = - normalizedDistanceDictionary["nose/nose-flaring-decr|incr"]

    noseCenter = normalizedLandmarks[5]

    distanceNostrilUpDownSX = abs(nostril1SX["y"] - noseCenter["y"])
    distanceNostrilUpDownDX = abs(nostril2SX["y"] - noseCenter["y"])

    meanDistanceNostrilUpDown = (
        distanceNostrilUpDownSX + distanceNostrilUpDownDX
    ) * 0.5
    distanceDictionary["meanDistanceNostrilUpDown"] = meanDistanceNostrilUpDown

    noseMediumDX = normalizedLandmarks[174]
    noseMediumSX = normalizedLandmarks[399]

    distanceNoseMedium = abs(noseMediumSX["x"] - noseMediumDX["x"])
    distanceDictionary["distanceNoseMedium"] = distanceNoseMedium
    normalizedDistanceDictionary["nose/nose-width2-decr|incr"] = normalizeminus11(distanceNoseMedium, limits[gender]["distanceNoseMedium"][0], limits[gender]["distanceNoseMedium"][1]);


    noseHighDX = normalizedLandmarks[193]
    noseHighSX = normalizedLandmarks[417]

    distanceNoseHigh = abs(noseHighSX["x"] - noseHighDX["x"])
    distanceDictionary["distanceNoseHigh"] = distanceNoseHigh
    normalizedDistanceDictionary["nose/nose-width1-decr|incr"] = normalizeminus11(distanceNoseHigh, limits[gender]["distanceNoseHigh"][0], limits[gender]["distanceNoseHigh"][1])
    
    noseCompression = abs(noseCurveCoord[4]["z"] + noseCurveCoord[5]["z"])/2
    distanceDictionary["noseCompression"] = noseCompression
    normalizedDistanceDictionary["nose/nose-compression-compress|uncompress"] = normalizeminus11(noseCompression, limits[gender]["noseCompression"][0], limits[gender]["noseCompression"][1]);
    print("Nose COmpression: ", noseCompression)
    
    noseCurve = abs(noseCurveCoord[0]["z"] + noseCurveCoord[1]["z"] + noseCurveCoord[2]["z"] + noseCurveCoord[3]["z"])/4
    distanceDictionary["noseCurve"] = noseCurve
    normalizedDistanceDictionary["nose/nose-curve-concave|convex"] = normalizeminus11(noseCurve, limits[gender]["noseCurve"][0], limits[gender]["noseCurve"][1]);
    print("Nose Curve: ", noseCurve)
    
    noseDepth = abs(noseCurveCoord[0]["z"] + noseCurveCoord[1]["z"] + noseCurveCoord[2]["z"] + noseCurveCoord[3]["z"] + noseCurveCoord[4]["z"] + noseCurveCoord[5]["z"])/6
    distanceDictionary["noseDepth"] = noseDepth
    normalizedDistanceDictionary["nose/nose-scale-depth-decr|incr"] = normalizeminus11(noseDepth, limits[gender]["noseDepth"][0], limits[gender]["noseDepth"][1]);
    print("Nose Depth: ", noseDepth)
    
    noseGreek = abs(noseCurveCoord[0]["z"] + noseCurveCoord[1]["z"])/2
    distanceDictionary["noseGreek"] = noseGreek
    normalizedDistanceDictionary["nose/nose-greek-decr|incr"] = normalizeminus11(noseGreek, limits[gender]["noseGreek"][0], limits[gender]["noseGreek"][1]);
    print("Nose Greek: ", noseGreek)

def calculateEyes(
    rightEyeCoord,
    distanceDictionary,
    normalizedLandmarks,
    noseCoord,
    faceShapeCoord,
    leftEyeCoord,
    gender
):
    distanceXRightEye = abs(rightEyeCoord[2]["x"] - rightEyeCoord[3]["x"])
    distanceDictionary["distanceXRightEye"] = distanceXRightEye

    distanceYRightEye = abs(rightEyeCoord[0]["y"] - rightEyeCoord[1]["y"])
    distanceDictionary["distanceYRightEye"] = distanceYRightEye
    scaledDistanceYRightEye = distanceYRightEye / distanceXRightEye
    distanceDictionary["scaledDistanceYRightEye"] = scaledDistanceYRightEye
    normalizedDistanceDictionary["eyes/r-eye-height2-decr|incr"] = normalizeminus11(distanceYRightEye, limits[gender]["distanceYRightEye"][0], limits[gender]["distanceYRightEye"][1]);
    normalizedDistanceDictionary["eyes/r-eye-scale-decr|incr"] = normalizeminus11(scaledDistanceYRightEye, limits[gender]["scaledDistanceYRightEye"][0], limits[gender]["scaledDistanceYRightEye"][1]);


    upRightEyeSX = normalizedLandmarks[56]
    downRightEyeSX = normalizedLandmarks[26]

    distanceYRightEyeSX = abs(upRightEyeSX["y"] - downRightEyeSX["y"])
    distanceDictionary["distanceYRightEyeSX"] = distanceYRightEyeSX
    normalizedDistanceDictionary["eyes/r-eye-height1-decr|incr"] = normalizeminus11(distanceYRightEyeSX, limits[gender]["distanceYRightEyeSX"][0], limits[gender]["distanceYRightEyeSX"][1])


    upRightEyeDX = normalizedLandmarks[30]
    downRightEyeDX = normalizedLandmarks[110]

    distanceYRightEyeDX = abs(upRightEyeDX["y"] - downRightEyeDX["y"])
    distanceDictionary["distanceYRightEyeDX"] = distanceYRightEyeDX
    normalizedDistanceDictionary["eyes/r-eye-height3-decr|incr"] = normalizeminus11(distanceYRightEyeDX, limits[gender]["distanceYRightEyeDX"][0], limits[gender]["distanceYRightEyeDX"][1])


    centerPointRightEye = {
        "centerX": (rightEyeCoord[0]["x"] + rightEyeCoord[1]["x"]) * 0.5,
        "centerY": (rightEyeCoord[0]["y"] + rightEyeCoord[1]["y"]) * 0.5,
    }

    distanceRightEyeCenterNose = abs(centerPointRightEye["centerX"] - noseCoord[1]["x"])
    distanceDictionary["distanceRightEyeCenterNose"] = distanceRightEyeCenterNose

    distanceRightEyeNose = abs(centerPointRightEye["centerX"] - noseCoord[1]["x"])
    distanceDictionary["distanceRightEyeNose"] = distanceRightEyeNose
    normalizedDistanceDictionary["eyes/r-eye-trans-in|out"] = normalizeminus11(distanceRightEyeNose, limits[gender]["distanceRightEyeNose"][0], limits[gender]["distanceRightEyeNose"][1])


    distanceRightEyeCenterChin = abs(
        centerPointRightEye["centerY"] - faceShapeCoord[0]["y"]
    )
    distanceDictionary["distanceRightEyeCenterChin"] = distanceRightEyeCenterChin
    normalizedDistanceDictionary["eyes/r-eye-trans-down|up"] = normalizeminus11(distanceRightEyeCenterChin, limits[gender]["distanceRightEyeCenterChin"][0], limits[gender]["distanceRightEyeCenterChin"][1])


    distanceXLeftEye = abs(leftEyeCoord[2]["x"] - leftEyeCoord[3]["x"])
    distanceDictionary["distanceXLeftEye"] = distanceXLeftEye

    distanceYLeftEye = abs(leftEyeCoord[0]["y"] - leftEyeCoord[1]["y"])
    distanceDictionary["distanceYLeftEye"] = distanceYLeftEye

    scaledDistanceYLeftEye = distanceYLeftEye / distanceXLeftEye
    distanceDictionary["scaledDistanceYLeftEye"] = scaledDistanceYLeftEye
    normalizedDistanceDictionary["eyes/l-eye-height2-decr|incr"] = normalizeminus11(distanceYLeftEye, limits[gender]["distanceYLeftEye"][0], limits[gender]["distanceYLeftEye"][1])
    normalizedDistanceDictionary["eyes/l-eye-scale-decr|incr"] = normalizeminus11(scaledDistanceYLeftEye, limits[gender]["scaledDistanceYLeftEye"][0], limits[gender]["scaledDistanceYLeftEye"][1])


    upLeftEyeSX = normalizedLandmarks[286]
    downLeftEyeSX = normalizedLandmarks[256]

    distanceYLeftEyeSX = abs(upLeftEyeSX["y"] - downLeftEyeSX["y"])
    distanceDictionary["distanceYLeftEyeSX"] = distanceYLeftEyeSX
    normalizedDistanceDictionary["eyes/l-eye-height1-decr|incr"] = normalizeminus11(distanceYLeftEyeSX, limits[gender]["distanceYLeftEyeSX"][0], limits[gender]["distanceYLeftEyeSX"][1]);


    upLeftEyeDX = normalizedLandmarks[260]
    downLeftEyeDX = normalizedLandmarks[339]

    distanceYLeftEyeDX = abs(upLeftEyeDX["y"] - downLeftEyeDX["y"])
    distanceDictionary["distanceYLeftEyeDX"] = distanceYLeftEyeDX
    normalizedDistanceDictionary["eyes/l-eye-height3-decr|incr"] = normalizeminus11(distanceYLeftEyeDX, limits[gender]["distanceYLeftEyeDX"][0], limits[gender]["distanceYLeftEyeDX"][1]);


    centerPointLeftEye = {
        "centerX": (leftEyeCoord[0]["x"] + leftEyeCoord[1]["x"]) * 0.5,
        "centerY": (leftEyeCoord[0]["y"] + leftEyeCoord[1]["y"]) * 0.5,
    }

    distanceLeftEyeCenterNose = abs(centerPointLeftEye["centerX"] - noseCoord[1]["x"])
    distanceDictionary["distanceLeftEyeCenterNose"] = distanceLeftEyeCenterNose

    distanceLeftEyeNose = abs(centerPointLeftEye["centerX"] - noseCoord[1]["x"])
    distanceDictionary["distanceLeftEyeNose"] = distanceLeftEyeNose
    normalizedDistanceDictionary["eyes/l-eye-trans-in|out"] = normalizeminus11(distanceLeftEyeNose, limits[gender]["distanceLeftEyeNose"][0], limits[gender]["distanceLeftEyeNose"][1]);


    distanceLeftEyeCenterChin = abs(
        centerPointLeftEye["centerY"] - faceShapeCoord[0]["y"]
    )
    distanceDictionary["distanceLeftEyeCenterChin"] = distanceLeftEyeCenterChin
    normalizedDistanceDictionary["eyes/l-eye-trans-down|up"] = normalizeminus11(distanceLeftEyeCenterChin, limits[gender]["distanceLeftEyeCenterChin"][0], limits[gender]["distanceLeftEyeCenterChin"][1]);



def calculateEyebrows(
    rightEyeBrowCoord, distanceDictionary, rightEyeCoord, leftEyeBrowCoord, leftEyeCoord, gender
):
    # EYEBROW DX
    rightPointSX = midpoint(
        rightEyeBrowCoord[0]["x"],
        rightEyeBrowCoord[0]["y"],
        rightEyeBrowCoord[4]["x"],
        rightEyeBrowCoord[4]["y"],
    )
    rightPointMidSX = midpoint(
        rightEyeBrowCoord[2]["x"],
        rightEyeBrowCoord[2]["y"],
        rightEyeBrowCoord[6]["x"],
        rightEyeBrowCoord[6]["y"],
    )
    rightPointMidDX = midpoint(
        rightEyeBrowCoord[3]["x"],
        rightEyeBrowCoord[3]["y"],
        rightEyeBrowCoord[7]["x"],
        rightEyeBrowCoord[7]["y"],
    )
    rightPointDX = midpoint(
        rightEyeBrowCoord[1]["x"],
        rightEyeBrowCoord[1]["y"],
        rightEyeBrowCoord[5]["x"],
        rightEyeBrowCoord[5]["y"],
    )
    distanceYEyeBrowDX = abs(rightPointSX["y"] - rightPointDX["y"])
    distanceDictionary["distanceYEyeBrowDX"] = distanceYEyeBrowDX

    meanEyeBrowRightExtY = (rightPointSX["y"] + rightPointDX["y"]) * 0.5
    meanEyeBrowRightIntY = (rightPointMidSX["y"] + rightPointMidDX["y"]) * 0.5
    distanceEyeBrowRightY = abs(meanEyeBrowRightExtY - meanEyeBrowRightIntY)
    distanceDictionary["distanceEyeBrowRightY"] = distanceEyeBrowRightY

    distanceEyeEyeBrowRight = abs(rightEyeCoord[1]["y"] - rightPointMidSX["y"])
    distanceDictionary["distanceEyeEyeBrowRight"] = distanceEyeEyeBrowRight

    # EYEBROW SX
    leftPointSX = midpoint(
        leftEyeBrowCoord[0]["x"],
        leftEyeBrowCoord[0]["y"],
        leftEyeBrowCoord[4]["x"],
        leftEyeBrowCoord[4]["y"],
    )
    leftPointMidSX = midpoint(
        leftEyeBrowCoord[2]["x"],
        leftEyeBrowCoord[2]["y"],
        leftEyeBrowCoord[6]["x"],
        leftEyeBrowCoord[6]["y"],
    )
    leftPointMidDX = midpoint(
        leftEyeBrowCoord[3]["x"],
        leftEyeBrowCoord[3]["y"],
        leftEyeBrowCoord[7]["x"],
        leftEyeBrowCoord[7]["y"],
    )
    leftPointDX = midpoint(
        leftEyeBrowCoord[1]["x"],
        leftEyeBrowCoord[1]["y"],
        leftEyeBrowCoord[5]["x"],
        leftEyeBrowCoord[5]["y"],
    )

    # Differenza delle y dei punti esterni
    distanceYEyeBrowSX = abs(leftPointSX["y"] - leftPointDX["y"])
    distanceDictionary["distanceYEyeBrowSX"] = distanceYEyeBrowSX

    # Differenza delle y dei punti centrali rispetto agli esterni
    meanEyeBrowLeftExtY = (leftPointSX["y"] + leftPointDX["y"]) * 0.5
    meanEyeBrowLeftIntY = (leftPointMidSX["y"] + leftPointMidDX["y"]) * 0.5
    distanceEyeBrowLeftY = abs(meanEyeBrowLeftExtY - meanEyeBrowLeftIntY)
    distanceDictionary["distanceEyeBrowLeftY"] = distanceEyeBrowLeftY

    distanceEyeEyeBrowLeft = abs(leftEyeCoord[1]["y"] - leftPointMidSX["y"])
    distanceDictionary["distanceEyeEyeBrowLeft"] = distanceEyeEyeBrowLeft

    meanDistanceYEyeBrow = (distanceYEyeBrowDX + distanceYEyeBrowSX) * 0.5
    distanceDictionary["meanDistanceYEyeBrow"] = meanDistanceYEyeBrow
    meanDistanceEyeBrowY = (distanceEyeBrowRightY + distanceEyeBrowLeftY) * 0.5
    distanceDictionary["meanDistanceEyeBrowY"] = meanDistanceEyeBrowY
    meanDistanceEyeEyeBrow = (distanceEyeEyeBrowRight + distanceEyeEyeBrowLeft) * 0.5
    distanceDictionary["meanDistanceEyeEyeBrow"] = meanDistanceEyeEyeBrow
    normalizedDistanceDictionary["eyebrows/eyebrows-trans-down|up"] = normalizeminus11(meanDistanceEyeEyeBrow, limits[gender]["meanDistanceEyeEyeBrow"][0], limits[gender]["meanDistanceEyeEyeBrow"][1])
    normalizedDistanceDictionary["eyebrows/eyebrows-angle-down|up"] = normalizeCustomLimits(meanDistanceYEyeBrow, limits[gender]["meanDistanceYEyeBrow"][0], limits[gender]["meanDistanceYEyeBrow"][1], -0.2, 0.2)



def calculateLips(normalizedLandmarks, lipsCoord, distanceDictionary, gender):
    upOpenMouth = normalizedLandmarks[13]
    downOpenMouth = normalizedLandmarks[14]
    distanceOpenMouth = abs(upOpenMouth["y"] - downOpenMouth["y"])

    distance_x_lips = abs(lipsCoord[2]["x"] - lipsCoord[3]["x"])
    distanceDictionary["distanceXLips"] = distance_x_lips
    normalizedDistanceDictionary["mouth/mouth-scale-horiz-decr|incr"] = (
        normalizeminus11(distance_x_lips, limits[gender]["distanceXLips"][0], limits[gender]["distanceXLips"][1])
    )


    distance_y_lips = abs(lipsCoord[1]["y"] - lipsCoord[0]["y"]) - distanceOpenMouth
    distanceDictionary["distanceYLips"] = distance_y_lips

    distanceLipsWidthDown = abs(downOpenMouth["y"] - lipsCoord[0]["y"])
    distanceDictionary["distanceLipsWidthDown"] = distanceLipsWidthDown
    normalizedDistanceDictionary["mouth/mouth-lowerlip-height-decr|incr"] = normalizeminus11(distanceLipsWidthDown, limits[gender]["distanceLipsWidthDown"][0], limits[gender]["distanceLipsWidthDown"][1])


    distanceLipsWidthUp = abs(upOpenMouth["y"] - lipsCoord[1]["y"])
    distanceDictionary["distanceLipsWidthUp"] = distanceLipsWidthUp
    normalizedDistanceDictionary["mouth/mouth-upperlip-height-decr|incr"] = normalizeminus11(distanceLipsWidthUp, limits[gender]["distanceLipsWidthUp"][0], limits[gender]["distanceLipsWidthUp"][1])


    cupidBowSx = normalizedLandmarks[37]
    cupidBowDx = normalizedLandmarks[267]

    distanceCupidBow = abs(cupidBowSx["x"] - cupidBowDx["x"])
    distanceDictionary["distanceCupidBow"] = distanceCupidBow
    normalizedDistanceDictionary["mouth/mouth-cupidsbow-width-decr|incr"] = normalizeminus11(distanceCupidBow, limits[gender]["distanceCupidBow"][0], limits[gender]["distanceCupidBow"][1])


    distanceCupidBowY = (
        abs(cupidBowSx["y"] - lipsCoord[1]["y"])
        + abs(cupidBowDx["y"] - lipsCoord[1]["y"])
    ) / 2
    distanceDictionary["distanceCupidBowY"] = distanceCupidBowY
    normalizedDistanceDictionary["mouth/mouth-cupidsbow-decr|incr"] = normalizeminus11(distanceCupidBowY, limits[gender]["distanceCupidBowY"][0], limits[gender]["distanceCupidBowY"][1]);


def calculateFaceShape2(normalizedLandmarks, jawCoord, templeCoord, cheeksCoord, foreheadCoord, distanceDictionary, gender):
    distanceTemple = abs(templeCoord[0]["x"] - templeCoord[1]["x"])
    distanceForeheadChin = abs(normalizedLandmarks[168]["y"] - normalizedLandmarks[152]["y"])
    distanceJawLine = abs(jawCoord[0]["x"] - jawCoord[1]["x"])
    widthToLengthRatio = distanceTemple / distanceForeheadChin
    cheekWidthToJawWidthRatio = abs(cheeksCoord[0]["x"] - cheeksCoord[1]["x"]) / distanceJawLine
    distanceCheeks = abs(cheeksCoord[0]["x"] - cheeksCoord[1]["x"])
    distanceForehead = abs(foreheadCoord[0]["x"] - foreheadCoord[1]["x"])
    
    distanceDictionary["distanceTemple"] = distanceTemple
    distanceDictionary["distanceForeheadChin"] = distanceForeheadChin
    distanceDictionary["distanceJawLine"] = distanceJawLine
    distanceDictionary["widthToLengthRatio"] = widthToLengthRatio
    distanceDictionary["cheekWidthToJawWidthRatio"] = cheekWidthToJawWidthRatio
    
    #Forehead Temple
    normalizedDistanceDictionary["forehead/forehead-temple-decr|incr"] = normalizeminus11(distanceTemple, limits[gender]["distanceTemple"][0], limits[gender]["distanceTemple"][1])
    
    invTriang = False
    
    #Triangular vs Inverted Triangular
    if distanceTemple > distanceJawLine:
        invTriang = True
        normalizedDistanceDictionary["head/head-invertedtriangular"] = normalize(
            distanceTemple / distanceJawLine,
            limits[gender]["distanceTemple/distanceJawLine"][0],
            limits[gender]["distanceTemple/distanceJawLine"][1],
        )
    else:
        normalizedDistanceDictionary["head/head-triangular"] = normalize(
            distanceTemple / distanceJawLine,
            limits[gender]["distanceTemple/distanceJawLine"][0],
            limits[gender]["distanceTemple/distanceJawLine"][1],
        )
     
    #rectangular, vs round vs square   
    if distanceTemple > distanceForeheadChin:
        normalizedDistanceDictionary["head/head-rectangular"] = normalize(
            distanceTemple / distanceForeheadChin,
            limits[gender]["distanceTemple/distanceForeheadChin"][0],
            limits[gender]["distanceTemple/distanceForeheadChin"][1],
        )
        if invTriang and gender=="female":
            normalizedDistanceDictionary["head/head-rectangular"] = normalizedDistanceDictionary["head/head-rectangular"] - 0.2
    elif abs(distanceTemple - distanceForeheadChin) < 0.05:
        if cheekWidthToJawWidthRatio > 0.5:
            normalizedDistanceDictionary["head/head-round"] = normalize(
                cheekWidthToJawWidthRatio,
                limits[gender]["cheekWidthToJawWidthRatio"][0],
                limits[gender]["cheekWidthToJawWidthRatio"][1],
            )
        else:
            normalizedDistanceDictionary["head/head-square"] = normalize(
                cheekWidthToJawWidthRatio,
                limits[gender]["cheekWidthToJawWidthRatio"][0],
                limits[gender]["cheekWidthToJawWidthRatio"][1],
            )
    
    #Diamond 
    if distanceCheeks > distanceForehead:
        if distanceForehead > distanceJawLine:
            normalizedDistanceDictionary["head/head-diamond"] = normalize(
                distanceCheeks / distanceJawLine,
                limits[gender]["distanceCheeks/distanceJawLine"][0],
                limits[gender]["distanceCheeks/distanceJawLine"][1],
            )
        
    #Head Vertical Scaling
    lengthToWidthRatio = distanceForeheadChin / distanceTemple
    distanceDictionary["lengthToWidthRatio"] = lengthToWidthRatio
    # if gender == "female":
    #     normalizedDistanceDictionary["head/head-scale-vert-decr|incr"] = 0.15
    # normalizedDistanceDictionary["head/head-scale-vert-decr|incr"] = 0.4


def calculateFaceFeatureDistances(normalizedLandmarks, distance_dictionary, faceShapeCoord, noseCoord, lipsCoord, rightEyeCoord, leftEyeCoord,
                                  rightEyeBrowCoord, leftEyeBrowCoord, jawCoord, templeCoord, cheeksCoord, foreheadCoord, noseCurveCoord, chinCoord, gender):
    
    calculate_forehead(faceShapeCoord, noseCoord, distance_dictionary, gender)
    calculateChin(normalizedLandmarks, distance_dictionary, faceShapeCoord, lipsCoord, chinCoord, gender)
    calculateFaceShape(faceShapeCoord, distance_dictionary, gender)
    calculateNose(noseCoord, noseCurveCoord, faceShapeCoord, distance_dictionary, normalizedLandmarks, gender)
    calculateEyes(
        rightEyeCoord,
        distance_dictionary,
        normalizedLandmarks,
        noseCoord,
        faceShapeCoord,
        leftEyeCoord,
        gender
    )
    calculateEyebrows(
        rightEyeBrowCoord,
        distance_dictionary,
        rightEyeCoord,
        leftEyeBrowCoord,
        leftEyeCoord,
        gender
    )
    calculateLips(normalizedLandmarks, lipsCoord, distance_dictionary, gender)
    calculateFaceShape2(normalizedLandmarks, jawCoord, templeCoord, cheeksCoord, foreheadCoord, distance_dictionary, gender)
    
    return normalizedDistanceDictionary


