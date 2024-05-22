normalizedDistanceDictionary = {}

def midpoint(point1x, point1y, point2x, point2y):
    return {"x": (point1x + point2x) / 2, "y": (point1y + point2y) / 2}

def normalize(value, min, max):
    return (value - min) / (max - min);


def normalizeminus11(value, min, max):
    return 2 * ((value - min) / (max - min)) - 1;


def reverse_normalizeminus11(value, min_value, max_value):
    return (2 * ((value - min_value) / (max_value - min_value)) - 1) * -1



def calculate_forehead(faceShapeCoord, noseCoord, distanceDictionary):
    distanceForehead = abs(faceShapeCoord[1]["y"] - noseCoord[1]["y"])
    distanceDictionary["distanceForehead"] = distanceForehead


def calculateChin(normalizedLandmarks, distanceDictionary, faceShapeCoord, lipsCoord):
    chinSX = normalizedLandmarks[176]
    chinDX = normalizedLandmarks[400]

    distanceChin = abs(chinSX["x"] - chinDX["x"])
    distanceDictionary["distanceChin"] = distanceChin
    normalizedDistanceDictionary["chin/chin-width-decr|incr"] = normalizeminus11(distanceChin, 0.11, 0.40);

    distanceChinLips = abs(faceShapeCoord[0]["y"] - lipsCoord[0]["y"])
    distanceDictionary["distanceChinLips"] = distanceChinLips


def calculateFaceShape(faceShapeCoord, distanceDictionary):
    distanceUpperFace = abs(faceShapeCoord[2]["x"] - faceShapeCoord[3]["x"])
    distanceDictionary["distanceUpperFace"] = distanceUpperFace
    # normalizedDistanceDictionary["head/head-round"] = normalize(distanceUpperFace, 0.871, 1.742);


    distanceLeftLowerFace = abs(faceShapeCoord[2]["x"] - faceShapeCoord[4]["x"])
    distanceRightLowerFace = abs(faceShapeCoord[3]["x"] - faceShapeCoord[5]["x"])
    meanDistanceLowerFace = (distanceLeftLowerFace + distanceRightLowerFace) * 0.5
    distanceDictionary["meanDistanceLowerFace"] = meanDistanceLowerFace
    normalizedDistanceDictionary["head/head-fat-decr|incr"] = normalizeminus11(meanDistanceLowerFace, 0.043, 0.196)

    # normalizedDistanceDictionary["head/head-rectangular"] = normalizeminus11(meanDistanceLowerFace, 0.087, 0.196);


    distanceUpDownFace = abs(faceShapeCoord[0]["y"] - faceShapeCoord[1]["y"])
    distanceDictionary["distanceUpDownFace"] = distanceUpDownFace


def calculateNose(noseCoord, faceShapeCoord, distanceDictionary, normalizedLandmarks):
    distanceLowNoseChin = abs(noseCoord[0]["y"] - faceShapeCoord[0]["y"])
    distanceDictionary["distanceLowNoseChin"] = distanceLowNoseChin
    normalizedDistanceDictionary["nose/nose-trans-down|up"] = normalizeminus11(distanceLowNoseChin, 0.269, 0.606)


    distanceLowHighNose = abs(noseCoord[1]["y"] - noseCoord[0]["y"])
    distanceDictionary["distanceLowHighNose"] = distanceLowHighNose
    normalizedDistanceDictionary["nose/nose-scale-vert-decr|incr"] = normalizeminus11(distanceLowHighNose, 0.263, 0.55)


    distanceNostrilNose = abs(noseCoord[2]["x"] - noseCoord[3]["x"])
    distanceDictionary["distanceNostrilNose"] = distanceNostrilNose
    normalizedDistanceDictionary["nose/nose-scale-horiz-decr|incr"] = normalizeminus11(distanceNostrilNose, 0.149, 0.3)
    normalizedDistanceDictionary["nose/nose-width3-decr|incr"] = normalizeminus11(distanceNostrilNose, 0.149, 0.3)


    nostril1SX = normalizedLandmarks[59]
    nostril1DX = normalizedLandmarks[238]

    nostril2SX = normalizedLandmarks[458]
    nostril2DX = normalizedLandmarks[289]

    distanceNostril1 = abs(nostril1SX["x"] - nostril1DX["x"])
    distanceNostril2 = abs(nostril2SX["x"] - nostril2DX["x"])

    meanDistanceNostril = (distanceNostril1 + distanceNostril2) * 0.5
    distanceDictionary["meanDistanceNostril"] = meanDistanceNostril
    normalizedDistanceDictionary["nose/nose-flaring-decr|incr"] = normalizeminus11(meanDistanceNostril, 0.03, 0.067);


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
    normalizedDistanceDictionary["nose/nose-width2-decr|incr"] = normalizeminus11(distanceNoseMedium, 0.075, 0.168);


    noseHighDX = normalizedLandmarks[193]
    noseHighSX = normalizedLandmarks[417]

    distanceNoseHigh = abs(noseHighSX["x"] - noseHighDX["x"])
    distanceDictionary["distanceNoseHigh"] = distanceNoseHigh
    normalizedDistanceDictionary["nose/nose-width1-decr|incr"] = normalizeminus11(distanceNoseHigh, 0.052, 0.117);



def calculateEyes(
    rightEyeCoord,
    distanceDictionary,
    normalizedLandmarks,
    noseCoord,
    faceShapeCoord,
    leftEyeCoord,
):
    distanceXRightEye = abs(rightEyeCoord[2]["x"] - rightEyeCoord[3]["x"])
    distanceDictionary["distanceXRightEye"] = distanceXRightEye

    distanceYRightEye = abs(rightEyeCoord[0]["y"] - rightEyeCoord[1]["y"])
    distanceDictionary["distanceYRightEye"] = distanceYRightEye
    scaledDistanceYRightEye = distanceYRightEye / distanceXRightEye
    distanceDictionary["scaledDistanceYRightEye"] = scaledDistanceYRightEye
    normalizedDistanceDictionary["eyes/r-eye-height2-decr|incr"] = normalizeminus11(scaledDistanceYRightEye, 0.2, 0.7);
    normalizedDistanceDictionary["eyes/r-eye-scale-decr|incr"] = normalizeminus11(scaledDistanceYRightEye, 0.2, 0.7);


    upRightEyeSX = normalizedLandmarks[56]
    downRightEyeSX = normalizedLandmarks[26]

    distanceYRightEyeSX = abs(upRightEyeSX["y"] - downRightEyeSX["y"])
    distanceDictionary["distanceYRightEyeSX"] = distanceYRightEyeSX
    normalizedDistanceDictionary["eyes/r-eye-height1-decr|incr"] = normalizeminus11(distanceYRightEyeSX, 0.052, 0.117)


    upRightEyeDX = normalizedLandmarks[30]
    downRightEyeDX = normalizedLandmarks[110]

    distanceYRightEyeDX = abs(upRightEyeDX["y"] - downRightEyeDX["y"])
    distanceDictionary["distanceYRightEyeDX"] = distanceYRightEyeDX
    normalizedDistanceDictionary["eyes/r-eye-height3-decr|incr"] = normalizeminus11(distanceYRightEyeDX, 0.053, 0.12)


    centerPointRightEye = {
        "centerX": (rightEyeCoord[0]["x"] + rightEyeCoord[1]["x"]) * 0.5,
        "centerY": (rightEyeCoord[0]["y"] + rightEyeCoord[1]["y"]) * 0.5,
    }

    distanceRightEyeCenterNose = abs(centerPointRightEye["centerX"] - noseCoord[1]["x"])
    distanceDictionary["distanceRightEyeCenterNose"] = distanceRightEyeCenterNose

    distanceRightEyeNose = abs(centerPointRightEye["centerX"] - noseCoord[1]["y"])
    distanceDictionary["distanceRightEyeNose"] = distanceRightEyeNose
    normalizedDistanceDictionary["eyes/r-eye-trans-in|out"] = normalizeminus11(distanceRightEyeNose, 0.090, 0.245)


    distanceRightEyeCenterChin = abs(
        centerPointRightEye["centerY"] - faceShapeCoord[0]["y"]
    )
    distanceDictionary["distanceRightEyeCenterChin"] = distanceRightEyeCenterChin
    normalizedDistanceDictionary["eyes/r-eye-trans-down|up"] = normalizeminus11(distanceRightEyeCenterChin, 0.47, 1.05)


    distanceXLeftEye = abs(leftEyeCoord[2]["x"] - leftEyeCoord[3]["x"])
    distanceDictionary["distanceXLeftEye"] = distanceXLeftEye

    distanceYLeftEye = abs(leftEyeCoord[0]["y"] - leftEyeCoord[1]["y"])
    distanceDictionary["distanceYLeftEye"] = distanceYLeftEye

    scaledDistanceYLeftEye = distanceYLeftEye / distanceXLeftEye
    distanceDictionary["scaledDistanceYLeftEye"] = scaledDistanceYLeftEye
    normalizedDistanceDictionary["eyes/l-eye-height2-decr|incr"] = normalizeminus11(scaledDistanceYLeftEye, 0.2, 0.7)
    normalizedDistanceDictionary["eyes/l-eye-scale-decr|incr"] = normalizeminus11(scaledDistanceYLeftEye, 0.2, 0.7)


    upLeftEyeSX = normalizedLandmarks[286]
    downLeftEyeSX = normalizedLandmarks[256]

    distanceYLeftEyeSX = abs(upLeftEyeSX["y"] - downLeftEyeSX["y"])
    distanceDictionary["distanceYLeftEyeSX"] = distanceYLeftEyeSX
    normalizedDistanceDictionary["eyes/l-eye-height1-decr|incr"] = normalizeminus11(distanceYLeftEyeSX, 0.052, 0.117);


    upLeftEyeDX = normalizedLandmarks[260]
    downLeftEyeDX = normalizedLandmarks[339]

    distanceYLeftEyeDX = abs(upLeftEyeDX["y"] - downLeftEyeDX["y"])
    distanceDictionary["distanceYLeftEyeDX"] = distanceYLeftEyeDX
    normalizedDistanceDictionary["eyes/l-eye-height3-decr|incr"] = normalizeminus11(distanceYLeftEyeDX, 0.053, 0.12);


    centerPointLeftEye = {
        "centerX": (leftEyeCoord[0]["x"] + leftEyeCoord[1]["x"]) * 0.5,
        "centerY": (leftEyeCoord[0]["y"] + leftEyeCoord[1]["y"]) * 0.5,
    }

    distanceLeftEyeCenterNose = abs(centerPointLeftEye["centerX"] - noseCoord[1]["x"])
    distanceDictionary["distanceLeftEyeCenterNose"] = distanceLeftEyeCenterNose

    distanceLeftEyeNose = abs(centerPointLeftEye["centerX"] - noseCoord[1]["x"])
    distanceDictionary["distanceLeftEyeNose"] = distanceLeftEyeNose
    normalizedDistanceDictionary["eyes/l-eye-trans-in|out"] = normalizeminus11(distanceLeftEyeNose, 0.090, 0.245);


    distanceLeftEyeCenterChin = abs(
        centerPointLeftEye["centerY"] - faceShapeCoord[0]["y"]
    )
    distanceDictionary["distanceLeftEyeCenterChin"] = distanceLeftEyeCenterChin
    normalizedDistanceDictionary["eyes/l-eye-trans-down|up"] = normalizeminus11(distanceLeftEyeCenterChin, 0.47, 1.05);



def calculateEyebrows(
    rightEyeBrowCoord, distanceDictionary, rightEyeCoord, leftEyeBrowCoord, leftEyeCoord
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
    normalizedDistanceDictionary["eyebrows/eyebrows-trans-down|up"] = normalizeminus11(meanDistanceEyeEyeBrow, 0.01, 0.05)
    normalizedDistanceDictionary["eyebrows/eyebrows-angle-down|up"] = normalizeminus11(meanDistanceYEyeBrow, 0.000050, 0.043772)



def calculateLips(normalizedLandmarks, lipsCoord, distanceDictionary):
    upOpenMouth = normalizedLandmarks[13]
    downOpenMouth = normalizedLandmarks[14]
    distanceOpenMouth = abs(upOpenMouth["y"] - downOpenMouth["y"])

    distance_x_lips = abs(lipsCoord[2]["x"] - lipsCoord[3]["x"])
    distanceDictionary["distanceXLips"] = distance_x_lips
    normalizedDistanceDictionary["mouth/mouth-scale-horiz-decr|incr"] = (
        normalizeminus11(distance_x_lips, 0.15, 0.40)
    )


    distance_y_lips = abs(lipsCoord[1]["y"] - lipsCoord[0]["y"]) - distanceOpenMouth
    distanceDictionary["distanceYLips"] = distance_y_lips

    distanceLipsWidthDown = abs(downOpenMouth["y"] - lipsCoord[0]["y"])
    distanceDictionary["distanceLipsWidthDown"] = distanceLipsWidthDown
    normalizedDistanceDictionary["mouth/mouth-lowerlip-height-decr|incr"] = normalizeminus11(distanceLipsWidthDown, 0.037, 0.084)


    distanceLipsWidthUp = abs(upOpenMouth["y"] - lipsCoord[1]["y"])
    distanceDictionary["distanceLipsWidthUp"] = distanceLipsWidthUp
    normalizedDistanceDictionary["mouth/mouth-upperlip-height-decr|incr"] = normalizeminus11(distanceLipsWidthUp, 0.025, 0.06)


    cupidBowSx = normalizedLandmarks[37]
    cupidBowDx = normalizedLandmarks[267]

    distanceCupidBow = abs(cupidBowSx["x"] - cupidBowDx["x"])
    distanceDictionary["distanceCupidBow"] = distanceCupidBow
    normalizedDistanceDictionary["mouth/mouth-cupidsbow-width-decr|incr"] = normalizeminus11(distanceCupidBow, 0.061, 0.136)


    distanceCupidBowY = (
        abs(cupidBowSx["y"] - lipsCoord[1]["y"])
        + abs(cupidBowDx["y"] - lipsCoord[1]["y"])
    ) / 2
    distanceDictionary["distanceCupidBowY"] = distanceCupidBowY
    normalizedDistanceDictionary["mouth/mouth-cupidsbow-decr|incr"] = normalizeminus11(distanceCupidBowY, 0.005, 0.012);


def calculateFaceFeatureDistances(normalizedLandmarks, distance_dictionary, faceShapeCoord, noseCoord, lipsCoord, rightEyeCoord, leftEyeCoord,
                                  rightEyeBrowCoord, leftEyeBrowCoord):
    
    calculate_forehead(faceShapeCoord, noseCoord, distance_dictionary)
    calculateChin(normalizedLandmarks, distance_dictionary, faceShapeCoord, lipsCoord)
    calculateFaceShape(faceShapeCoord, distance_dictionary)
    calculateNose(noseCoord, faceShapeCoord, distance_dictionary, normalizedLandmarks)
    calculateEyes(
        rightEyeCoord,
        distance_dictionary,
        normalizedLandmarks,
        noseCoord,
        faceShapeCoord,
        leftEyeCoord,
    )
    calculateEyebrows(
        rightEyeBrowCoord,
        distance_dictionary,
        rightEyeCoord,
        leftEyeBrowCoord,
        leftEyeCoord,
    )
    calculateLips(normalizedLandmarks, lipsCoord, distance_dictionary)
    
    return normalizedDistanceDictionary


