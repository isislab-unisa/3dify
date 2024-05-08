const makeHumanParameters = {
    "# Written by MakeHuman": "1.2.0 final",
    "version": "v1.2.0",
    "modifier head/head-round": "0",
    "modifier head/head-rectangular": "0",
    "modifier eyebrows/eyebrows-angle-down|up": "0",
    "modifier eyebrows/eyebrows-trans-down|up": "0",
    "modifier eyes/r-eye-height2-decr|incr": "0",
    "modifier eyes/r-eye-scale-decr|incr": "0",
    "modifier eyes/r-eye-trans-in|out": "0",
    "modifier eyes/r-eye-trans-down|up": "0",
    "modifier eyes/l-eye-height2-decr|incr": "0",
    "modifier eyes/l-eye-scale-decr|incr": "0",
    "modifier eyes/l-eye-trans-in|out": "0",
    "modifier eyes/l-eye-trans-down|up": "0",
    "modifier nose/nose-trans-down|up": "0",
    "modifier nose/nose-scale-vert-decr|incr": "0",
    "modifier nose/nose-scale-horiz-decr|incr": "0",
    "modifier mouth/mouth-scale-horiz-decr|incr": "0",
    "modifier mouth/mouth-scale-vert-decr|incr": "0",
    "modifier breast/BreastSize": "0.500000",
    "modifier breast/BreastFirmness": "0.500000",
    "modifier macrodetails/Gender": "1.000000",
    "modifier macrodetails/Age": "0.500000",
    "modifier macrodetails/African": "0.333333",
    "modifier macrodetails/Asian": "0.333333",
    "modifier macrodetails/Caucasian": "0.333333",
    "modifier macrodetails-universal/Muscle": "0.500000",
    "modifier macrodetails-universal/Weight": "0.500000",
    "modifier macrodetails-height/Height": "0.500000",
    "modifier macrodetails-proportions/BodyProportions": "0.500000",
    "skeleton": "default_no_toes.mhskel",
    "eyebrows eyebrow001": "9c81ec3a-faa5-4c94-9cdb-992300ba3084",
    "eyes HighPolyEyes": "2c12f43b-1303-432c-b7ce-d78346baf2e6",
    "clothesHideFaces": "True",
    "skinMaterial": "skins/middleage_caucasian_male/middleage_caucasian_male.mhmat",
    "material HighPolyEyes": "2c12f43b-1303-432c-b7ce-d78346baf2e6 eyes/materials/brown.mhmat",
    "material eyebrow001": "9c81ec3a-faa5-4c94-9cdb-992300ba3084 eyebrow001.mhmat"
}
 

export function GetMakehumanParametersFromLandmarks(normalizedLandmarks, age, gender)
{
    makeHumanParameters["modifier macrodetails/Gender"] = gender.toString();
    makeHumanParameters["modifier macrodetails/Age"] = age.toString();

    //Points ID for feature extraction
    let nosePoints = [2, 9, 129, 358]; //GIU, SU, SX, DX
    let faceShapePoints = [152, 10, 234, 454, 136, 365]; //GIU. SU, SX, DX, SX_GIU, DX_GIU
    let rightEyePoints = [23, 27, 130, 243]; //GIU, SU, SX, DX
    let rightEyeBrowPoints = [46, 55, 52, 65, 70, 107, 105, 66]; //GIU_SX, GIU_DX, GIU_CENT_SX, GIU_CENT_DX, SU_SX, SU_DX, SU_CENT_SX, SU_CENT_DX
    let leftEyePoints = [253, 257, 463, 359]; //GIU, SU, SX, DX
    let leftEyeBrowPoints = [285, 276, 282, 295, 336, 300, 334, 296]; //GIU_SX, GIU_DX, GIU_CENT_SX, GIU_CENT_DX, SU_SX, SU_DX, SU_CENT_SX, SU_CENT_DX
    let lipsPoints = [17, 0, 61, 291] //GIU, SU, SX, DX

    let points = [nosePoints, faceShapePoints, rightEyePoints, rightEyeBrowPoints, leftEyePoints, leftEyeBrowPoints, lipsPoints];

    let noseCoord = [];
    let faceShapeCoord = [];
    let rightEyeCoord = [];
    let rightEyeBrowCoord = [];
    let leftEyeCoord = [];
    let leftEyeBrowCoord = [];
    let lipsCoord = [];

    let coord = {
        noseCoord: noseCoord,
        faceShapeCoord: faceShapeCoord,
        rightEyeCoord: rightEyeCoord,
        rightEyeBrowCoord: rightEyeBrowCoord,
        leftEyeCoord: leftEyeCoord,
        leftEyeBrowCoord: leftEyeBrowCoord,
        lipsCoord: lipsCoord
    }

    //Disegna tutti i punt estratti e li salva in un array
    for (let p of points){
        for (let i = 0; i < p.length; i++){
            let lm1 = normalizedLandmarks[0][p[i]];
            switch (p) {
                case nosePoints:
                    noseCoord.push(lm1);
                    break;
                case faceShapePoints:
                    faceShapeCoord.push(lm1);
                    break;
                case rightEyePoints:
                    rightEyeCoord.push(lm1);
                    break;
                case rightEyeBrowPoints:
                    rightEyeBrowCoord.push(lm1);
                    break;
                case leftEyePoints:
                    leftEyeCoord.push(lm1);
                    break;
                case leftEyeBrowPoints:
                    leftEyeBrowCoord.push(lm1);
                    break;
                case lipsPoints:
                    lipsCoord.push(lm1);
                    break;
            }

            let x1 = lm1.x * squareSize + startX;
            let y1 = lm1.y * squareSize + startY;

            ctx.fillRect(x1, y1, 2, 2);

        }
    }


    console.log("Coordinates")
    console.log(coord);


    //Convert points to feature for makehuman and save them in a distance dictionary and then normalize them between 0 and 1 for the sliders
    let distanceDictionary = {}
    let normalizedDistanceDictionary = {}

    normalizedDistanceDictionary["head/head-age-decr|incr"] = ageValue;

    //LIPS
    calculateLips(normalizedLandmarks, lipsCoord, distanceDictionary, normalizedDistanceDictionary);
    //EYEBROWs
    calculateEyebrows(rightEyeBrowCoord, distanceDictionary, rightEyeCoord, leftEyeBrowCoord, leftEyeCoord, normalizedDistanceDictionary);
    //EYES
    calculateEyes(rightEyeCoord, distanceDictionary, normalizedDistanceDictionary, normalizedLandmarks, noseCoord, faceShapeCoord, leftEyeCoord);
    //NOSE
    calculateNose(noseCoord, faceShapeCoord, distanceDictionary, normalizedDistanceDictionary, normalizedLandmarks, squareSize, startX, startY);
    //FACE SHAPE
    calculateFaceShape(faceShapeCoord, distanceDictionary, normalizedDistanceDictionary);
    //CHIN
    calculateChin(normalizedLandmarks, distanceDictionary, normalizedDistanceDictionary, faceShapeCoord, lipsCoord);
    //FOREHEAD
    calculateForehead(faceShapeCoord, noseCoord, distanceDictionary);

    for(let key in normalizedDistanceDictionary){
        makeHumanParameters["modifier " + key] = normalizedDistanceDictionary[key].toString();
    }
    
    console.log("Distance Dictionary");
    console.log(distanceDictionary);

    console.log("Normalized Distance Dictionary");
    console.log(normalizedDistanceDictionary);

    console.log("MakeHuman Parameters");
    console.log(makeHumanParameters);
    return makeHumanParameters;
}


function calculateForehead(faceShapeCoord, noseCoord, distanceDictionary) {
    //Distanza tra punto alto del naso e punto alto della faccia
    let distanceForehead = Math.abs(faceShapeCoord[1].y - noseCoord[1].y);
    distanceDictionary["distanceForehead"] = distanceForehead;
    // normalizedDistanceDictionary["forehead/forehead-scale-vert-decr|incr"] = normalizeminus11(distanceForehead, 0.130, 0.294);
}

function calculateChin(normalizedLandmarks, distanceDictionary, normalizedDistanceDictionary, faceShapeCoord, lipsCoord) {
    let chinSX = normalizedLandmarks[0][176];
    let chinDX = normalizedLandmarks[0][400];

    //Distanza x tra estremo SX e estremo DX
    let distanceChin = Math.abs(chinSX.x - chinDX.x);
    distanceDictionary["distanceChin"] = distanceChin;
    normalizedDistanceDictionary["chin/chin-width-decr|incr"] = normalizeminus11(distanceChin, 0.11, 0.40);

    //Chin Height
    //Distanza y tra labbro inferiore e parte bassa della faccia
    let distanceChinLips = Math.abs(faceShapeCoord[0].y - lipsCoord[0].y);
    distanceDictionary["distanceChinLips"] = distanceChinLips;
    // normalizedDistanceDictionary["chin/chin-height-decr|incr"] = normalizeminus11(distanceChinLips, 0.000000, 1.000000);
}

function calculateFaceShape(faceShapeCoord, distanceDictionary, normalizedDistanceDictionary) {
    //Head-round
    //Distanza x tra estremo SX e estremo DX
    let distanceUpperFace = Math.abs(faceShapeCoord[2].x - faceShapeCoord[3].x);
    distanceDictionary["distanceUpperFace"] = distanceUpperFace;
    // normalizedDistanceDictionary["head/head-round"] = normalize(distanceUpperFace, 0.818938, 1.000000);
    normalizedDistanceDictionary["head/head-round"] = normalize(distanceUpperFace, 0.871, 1.742);


    //Head-rectangular
    //Distanza x tra estremo SX e mento SX
    let distanceLeftLowerFace = Math.abs(faceShapeCoord[2].x - faceShapeCoord[4].x);

    // distanceDictionary["distanceLeftLowerFace"] = distanceLeftLowerFace;
    //Distanza x tra estremo DX e mento DX
    let distanceRightLowerFace = Math.abs(faceShapeCoord[3].x - faceShapeCoord[5].x);

    // distanceDictionary["distanceRightLowerFace"] = distanceRightLowerFace;
    //media delle due distance
    let meanDistanceLowerFace = (distanceLeftLowerFace + distanceRightLowerFace) * 0.5;
    distanceDictionary["meanDistanceLowerFace"] = meanDistanceLowerFace;
    // normalizedDistanceDictionary["head/head-fat-decr|incr"] = normalizeminus11(meanDistanceLowerFace, 0.001, 0.23);
    normalizedDistanceDictionary["head/head-fat-decr|incr"] = normalizeminus11(meanDistanceLowerFace, 0.043, 0.196); //0.196


    // normalizedDistanceDictionary["chin/chin-bones-decr|incr"] = normalizeminus11(meanDistanceLowerFace, 0.087, 0.196); //0.196
    normalizedDistanceDictionary["head/head-rectangular"] = normalizeminus11(meanDistanceLowerFace, 0.087, 0.196);

    //Distanza tra punto in lato e punto in basso
    let distanceUpDownFace = Math.abs(faceShapeCoord[0].y - faceShapeCoord[1].y);
    distanceDictionary["distanceUpDownFace"] = distanceUpDownFace;
    // normalizedDistanceDictionary["head/head-scale-vert-decr|incr"] = normalizeminus11(distanceUpDownFace, 0.000000, 1.000000);
}

function calculateNose(noseCoord, faceShapeCoord, distanceDictionary, normalizedDistanceDictionary, normalizedLandmarks, squareSize, startX, startY) {
    //Distanza Y dal punto basso del naso al mento
    let distanceLowNoseChin = Math.abs(noseCoord[0].y - faceShapeCoord[0].y);
    distanceDictionary["distanceLowNoseChin"] = distanceLowNoseChin;
    normalizedDistanceDictionary["nose/nose-trans-down|up"] = normalizeminus11(distanceLowNoseChin, 0.269, 0.606);

    //Distanza Y dal punto piu alto al puno piu basso del naso
    let distanceLowHighNose = Math.abs(noseCoord[1].y - noseCoord[0].y);
    distanceDictionary["distanceLowHighNose"] = distanceLowHighNose;
    normalizedDistanceDictionary["nose/nose-scale-vert-decr|incr"] = normalizeminus11(distanceLowHighNose, 0.263, 0.55); //0.5925

    //Provare ad aggiungere il septum angle e nostril angle e forse anche volume
    //Distanza x tra le due narici
    let distanceNostrilNose = Math.abs(noseCoord[2].x - noseCoord[3].x);
    distanceDictionary["distanceNostrilNose"] = distanceNostrilNose;
    normalizedDistanceDictionary["nose/nose-scale-horiz-decr|incr"] = normalizeminus11(distanceNostrilNose, 0.149, 0.3);
    normalizedDistanceDictionary["nose/nose-width3-decr|incr"] = normalizeminus11(distanceNostrilNose, 0.149, 0.3);

    //NOSTRILS
    let nostril1SX = normalizedLandmarks[0][59];
    let nostril1DX = normalizedLandmarks[0][238];

    let nostril2SX = normalizedLandmarks[0][458];
    let nostril2DX = normalizedLandmarks[0][289];

    //Apertura delle narici
    let distanceNostril1 = Math.abs(nostril1SX.x - nostril1DX.x);
    let distanceNostril2 = Math.abs(nostril2SX.x - nostril2DX.x);

    let meanDistanceNostril = (distanceNostril1 + distanceNostril2) * 0.5;
    distanceDictionary["meanDistanceNostril"] = meanDistanceNostril;
    // normalizedDistanceDictionary["nose/nose-nostrils-width-decr|incr"] = normalizeminus11(meanDistanceNostril, 0.03, 0.067);
    normalizedDistanceDictionary["nose/nose-flaring-decr|incr"] = normalizeminus11(meanDistanceNostril, 0.03, 0.067);


    //Distanza y delle narici dal punto centrale del naso
    //punto centrale naso
    let noseCenter = normalizedLandmarks[0][5];

    let distanceNostrilUpDownSX = Math.abs(noseCenter.y - nostril1SX.y);
    let distanceNostrilUpDownDX = Math.abs(noseCenter.y - nostril2DX.y);

    //media delle distanze
    let meanDistanceNostrilUpDown = (distanceNostrilUpDownSX + distanceNostrilUpDownDX) * 0.5;
    distanceDictionary["meanDistanceNostrilUpDown"] = meanDistanceNostrilUpDown;
    // normalizedDistanceDictionary["nose/nose-nostrils-angle-down|up"] = reverse_normalizeminus11(meanDistanceNostrilUpDown, 0.016, 0.036);
    // normalizedDistanceDictionary["nose/nose-septumangle-decr|incr"] = reverse_normalizeminus11(meanDistanceNostrilUpDown, 0.016, 0.036);


    //Parti del naso verticali
    let noseMediumDX = normalizedLandmarks[0][174];
    let noseMediumSX = normalizedLandmarks[0][399];


    let distanceNoseMedium = Math.abs(noseMediumDX.x - noseMediumSX.x);
    distanceDictionary["distanceNoseMedium"] = distanceNoseMedium;
    normalizedDistanceDictionary["nose/nose-width2-decr|incr"] = normalizeminus11(distanceNoseMedium, 0.075, 0.168);

    let noseHighDX = normalizedLandmarks[0][193];
    let noseHighSX = normalizedLandmarks[0][417];

    let distanceNoseHigh = Math.abs(noseHighDX.x - noseHighSX.x);
    distanceDictionary["distanceNoseHigh"] = distanceNoseHigh;
    normalizedDistanceDictionary["nose/nose-width1-decr|incr"] = normalizeminus11(distanceNoseHigh, 0.052, 0.117);
}

function calculateEyes(rightEyeCoord, distanceDictionary, normalizedDistanceDictionary, normalizedLandmarks, noseCoord, faceShapeCoord, leftEyeCoord) {
    //RIGHT EYE
    //Distanza x tra estremi dx e sx
    let distanceXRightEye = Math.abs(rightEyeCoord[2].x - rightEyeCoord[3].x);
    distanceDictionary["distanceXRightEye"] = distanceXRightEye;
    // normalizedDistanceDictionary["eyes/r-eye-scale-decr|incr"] = normalizeminus11(distanceXRightEye, 0.135, 0.303);

    //Distanza y tra estremi up e dw
    let distanceYRightEye = Math.abs(rightEyeCoord[0].y - rightEyeCoord[1].y);
    distanceDictionary["distanceYRightEye"] = distanceYRightEye;
    let scaledDistanceYRightEye = distanceYRightEye / distanceXRightEye;
    distanceDictionary["scaledDistanceYRightEye"] = scaledDistanceYRightEye;
    normalizedDistanceDictionary["eyes/r-eye-height2-decr|incr"] = normalizeminus11(scaledDistanceYRightEye, 0.2, 0.7);
    normalizedDistanceDictionary["eyes/r-eye-scale-decr|incr"] = normalizeminus11(scaledDistanceYRightEye, 0.2, 0.7);

    //Distanza y tra estremi up e dw a sx
    let upRightEyeSX = normalizedLandmarks[0][56];
    let downRightEyeSX = normalizedLandmarks[0][26];
    let distanceYRightEyeSX = Math.abs(upRightEyeSX.y - downRightEyeSX.y);
    distanceDictionary["distanceYRightEyeSX"] = distanceYRightEyeSX;
    normalizedDistanceDictionary["eyes/r-eye-height1-decr|incr"] = normalizeminus11(distanceYRightEyeSX, 0.052, 0.117);

    //distanza y tra estremi up e dw a dx
    let upRightEyeDX = normalizedLandmarks[0][30];
    let downRightEyeDX = normalizedLandmarks[0][110];
    let distanceYRightEyeDX = Math.abs(upRightEyeDX.y - downRightEyeDX.y);
    distanceDictionary["distanceYRightEyeDX"] = distanceYRightEyeDX;
    normalizedDistanceDictionary["eyes/r-eye-height3-decr|incr"] = normalizeminus11(distanceYRightEyeDX, 0.053, 0.12);

    //Distanza x dal centro degli occhi ad un punto del naso (punto in alto)
    //Punto centrale degli occhi
    let centerPointRightEye = {
        x: (rightEyeCoord[0].x + rightEyeCoord[1].x) * 0.5,
        y: (rightEyeCoord[0].y + rightEyeCoord[1].y) * 0.5
    };

    //Distanza X dal punto centrale degli occhi al punto del naso
    let distanceRightEyeCenterNose = Math.abs(centerPointRightEye.x - noseCoord[1].x);
    distanceDictionary["distanceRightEyeCenterNose"] = distanceRightEyeCenterNose;
    //distanza X dal punto a DX degli occhi al punto superiore del naso
    // let distanceRightEyeNose = Math.abs(rightEyeCoord[3].x - noseCoord[1].x);
    let distanceRightEyeNose = Math.abs(centerPointRightEye.x - noseCoord[1].x);
    distanceDictionary["distanceRightEyeNose"] = distanceRightEyeNose;
    normalizedDistanceDictionary["eyes/r-eye-trans-in|out"] = normalizeminus11(distanceRightEyeNose, 0.090, 0.245); //0.265

    //Distanza Y dal punto centrale degli occhi al mento
    let distanceRightEyeCenterChin = Math.abs(centerPointRightEye.y - faceShapeCoord[0].y);
    distanceDictionary["distanceRightEyeCenterChin"] = distanceRightEyeCenterChin;
    normalizedDistanceDictionary["eyes/r-eye-trans-down|up"] = normalizeminus11(distanceRightEyeCenterChin, 0.47, 1.05);


    //LEFT EYE
    //Distanza x tra estremi dx e sx
    let distanceXLeftEye = Math.abs(leftEyeCoord[2].x - leftEyeCoord[3].x);
    distanceDictionary["distanceXLeftEye"] = distanceXLeftEye;
    // normalizedDistanceDictionary["eyes/l-eye-scale-decr|incr"] = normalizeminus11(distanceXLeftEye, 0.132, 0.297);

    //Distanza y tra estremi up e dw
    let distanceYLeftEye = Math.abs(leftEyeCoord[0].y - leftEyeCoord[1].y);
    distanceDictionary["distanceYLeftEye"] = distanceYLeftEye;
    let scaledDistanceYLeftEye = distanceYLeftEye / distanceXLeftEye;
    distanceDictionary["scaledDistanceYLeftEye"] = scaledDistanceYLeftEye;
    normalizedDistanceDictionary["eyes/l-eye-height2-decr|incr"] = normalizeminus11(scaledDistanceYLeftEye, 0.2, 0.7);
    normalizedDistanceDictionary["eyes/l-eye-scale-decr|incr"] = normalizeminus11(scaledDistanceYLeftEye, 0.2, 0.7);

    //Distanza y tra estremi up e dw a sx
    let upLeftEyeSX = normalizedLandmarks[0][286];
    let downLeftEyeSX = normalizedLandmarks[0][256];
    // let distanceYLeftEyeSX = Math.abs(upRightEyeSX.y - downRightEyeSX.y);
    let distanceYLeftEyeSX = Math.abs(upLeftEyeSX.y - downLeftEyeSX.y);
    distanceDictionary["distanceYLeftEyeSX"] = distanceYLeftEyeSX;
    normalizedDistanceDictionary["eyes/l-eye-height1-decr|incr"] = normalizeminus11(distanceYLeftEyeSX, 0.052, 0.117);

    //distanza y tra estremi up e dw a dx
    let upLeftEyeDX = normalizedLandmarks[0][260];
    let downLeftEyeDX = normalizedLandmarks[0][339];
    let distanceYLeftEyeDX = Math.abs(upLeftEyeDX.y - downLeftEyeDX.y);
    distanceDictionary["distanceYLeftEyeDX"] = distanceYLeftEyeDX;
    normalizedDistanceDictionary["eyes/l-eye-height3-decr|incr"] = normalizeminus11(distanceYLeftEyeDX, 0.053, 0.12);

    //Distanza x dal centro degli occhi ad un punto del naso (punto in alto)
    //Punto centrale degli occhi
    let centerPointLeftEye = {
        x: (leftEyeCoord[0].x + leftEyeCoord[1].x) * 0.5,
        y: (leftEyeCoord[0].y + leftEyeCoord[1].y) * 0.5
    };

    //Distanza X dal punto centrale degli occhi al punto del naso
    let distanceLeftEyeCenterNose = Math.abs(centerPointLeftEye.x - noseCoord[1].x);
    distanceDictionary["distanceLeftEyeCenterNose"] = distanceLeftEyeCenterNose;
    //distanza X dal punto a SX degli occhi al punto superiore del naso
    // let distanceLeftEyeNose = Math.abs(leftEyeCoord[2].x - noseCoord[1].x);
    let distanceLeftEyeNose = Math.abs(centerPointLeftEye.x - noseCoord[1].x);
    distanceDictionary["distanceLeftEyeNose"] = distanceLeftEyeNose;
    normalizedDistanceDictionary["eyes/l-eye-trans-in|out"] = normalizeminus11(distanceLeftEyeNose, 0.090, 0.245);


    //Distance Y dal punto centrale degli occhi al mento
    let distanceLeftEyeCenterChin = Math.abs(centerPointLeftEye.y - faceShapeCoord[0].y);
    distanceDictionary["distanceLeftEyeCenterChin"] = distanceLeftEyeCenterChin;
    normalizedDistanceDictionary["eyes/l-eye-trans-down|up"] = normalizeminus11(distanceLeftEyeCenterChin, 0.47, 1.05);
}

function calculateEyebrows(rightEyeBrowCoord, distanceDictionary, rightEyeCoord, leftEyeBrowCoord, leftEyeCoord, normalizedDistanceDictionary) {
    //EYEBROW DX
    //Calcola un riferimento come media dei due riferimenti presenti
    let rightPointSX = midpoint(rightEyeBrowCoord[0].x, rightEyeBrowCoord[0].y, rightEyeBrowCoord[4].x, rightEyeBrowCoord[4].y);
    let rightPointMidSX = midpoint(rightEyeBrowCoord[2].x, rightEyeBrowCoord[2].y, rightEyeBrowCoord[6].x, rightEyeBrowCoord[6].y);
    let rightPointMidDX = midpoint(rightEyeBrowCoord[3].x, rightEyeBrowCoord[3].y, rightEyeBrowCoord[7].x, rightEyeBrowCoord[7].y);
    let rightPointDX = midpoint(rightEyeBrowCoord[1].x, rightEyeBrowCoord[1].y, rightEyeBrowCoord[5].x, rightEyeBrowCoord[5].y);

    //Differenza delle y dei punti esterni
    let distanceYEyeBrowDX = Math.abs(rightPointSX.y - rightPointDX.y);
    distanceDictionary["distanceYEyeBrowDX"] = distanceYEyeBrowDX;

    //Differenza delle y dei punti centrali rispetto agli esterni
    let meanEyeBrowRightExtY = (rightPointSX.y + rightPointDX.y) * 0.5;
    let meanEyeBrowRightIntY = (rightPointMidSX.y + rightPointMidDX.y) * 0.5;
    let distanceEyeBrowRightY = Math.abs(meanEyeBrowRightExtY - meanEyeBrowRightIntY);
    distanceDictionary["distanceEyeBrowRightY"] = distanceEyeBrowRightY;

    //Differnza dei punti centrali dal punto superiore degli occhi
    let distanceEyeEyeBrowRight = Math.abs(rightEyeCoord[1].y - rightPointMidSX.y);
    distanceDictionary["distanceEyeEyeBrowRight"] = distanceEyeEyeBrowRight;

    //EYEBROW SX
    //Calcola un riferimento come media dei due riferimenti presenti
    let leftPointSX = midpoint(leftEyeBrowCoord[0].x, leftEyeBrowCoord[0].y, leftEyeBrowCoord[4].x, leftEyeBrowCoord[4].y);
    let leftPointMidSX = midpoint(leftEyeBrowCoord[2].x, leftEyeBrowCoord[2].y, leftEyeBrowCoord[6].x, leftEyeBrowCoord[6].y);
    let leftPointMidDX = midpoint(leftEyeBrowCoord[3].x, leftEyeBrowCoord[3].y, leftEyeBrowCoord[7].x, leftEyeBrowCoord[7].y);
    let leftPointDX = midpoint(leftEyeBrowCoord[1].x, leftEyeBrowCoord[1].y, leftEyeBrowCoord[5].x, leftEyeBrowCoord[5].y);

    //Differenza delle y dei punti esterni
    let distanceYEyeBrowSX = Math.abs(leftPointSX.y - leftPointDX.y);
    distanceDictionary["distanceYEyeBrowSX"] = distanceYEyeBrowSX;

    //Differenza delle y dei punti centrali rispetto agli esterni
    let meanEyeBrowLeftExtY = (leftPointSX.y + leftPointDX.y) * 0.5;
    let meanEyeBrowLeftIntY = (leftPointMidSX.y + leftPointMidDX.y) * 0.5;
    let distanceEyeBrowLeftY = Math.abs(meanEyeBrowLeftExtY - meanEyeBrowLeftIntY);
    distanceDictionary["distanceEyeBrowLeftY"] = distanceEyeBrowLeftY;

    //distanza dei punti centrali dal punto superiore degli occhi
    let distanceEyeEyeBrowLeft = Math.abs(leftEyeCoord[1].y - leftPointMidSX.y);
    distanceDictionary["distanceEyeEyeBrowLeft"] = distanceEyeEyeBrowLeft;

    let meanDistanceYEyeBrow = (distanceYEyeBrowDX + distanceYEyeBrowSX) * 0.5;
    distanceDictionary["meanDistanceYEyeBrow"] = meanDistanceYEyeBrow;
    let meanDistanceEyeBrowY = (distanceEyeBrowRightY + distanceEyeBrowLeftY) * 0.5;
    distanceDictionary["meanDistanceEyeBrowY"] = meanDistanceEyeBrowY;
    let meanDistanceEyeEyeBrow = (distanceEyeEyeBrowRight + distanceEyeEyeBrowLeft) * 0.5;
    distanceDictionary["meanDistanceEyeEyeBrow"] = meanDistanceEyeEyeBrow;
    normalizedDistanceDictionary["eyebrows/eyebrows-trans-down|up"] = normalizeminus11(meanDistanceEyeEyeBrow, 0.01, 0.05);
    normalizedDistanceDictionary["eyebrows/eyebrows-angle-down|up"] = normalizeminus11(meanDistanceYEyeBrow, 0.000050, 0.043772);
}

function calculateLips(normalizedLandmarks, lipsCoord, distanceDictionary, normalizedDistanceDictionary) {
    //Distanza tra i punti interni della bocca per calcolare eventuale spazio per la bocca aperta
    let upOpenMouth = normalizedLandmarks[0][13];
    let downOpenMouth = normalizedLandmarks[0][14];
    let distanceOpenMouth = Math.abs(upOpenMouth.y - downOpenMouth.y);

    //Distanza x tra i punti esterni della bocca DX e SX
    let distanceXLips = Math.abs(lipsCoord[2].x - lipsCoord[3].x);
    distanceDictionary["distanceXLips"] = distanceXLips;
    // normalizedDistanceDictionary["mouth/mouth-scale-horiz-decr|incr"] = normalizeminus11(distanceXLips, 0.242151, 0.398220);
    normalizedDistanceDictionary["mouth/mouth-scale-horiz-decr|incr"] = normalizeminus11(distanceXLips, 0.15, 0.40);

    //Distanza y tra i punti esterni della bocca UP e DW
    let distanceYLips = Math.abs(lipsCoord[1].y - lipsCoord[0].y) - distanceOpenMouth;
    distanceDictionary["distanceYLips"] = distanceYLips;
    // normalizedDistanceDictionary["mouth/mouth-scale-vert-decr|incr"] = normalizeminus11(distanceYLips, 0.090961 ,0.185984);
    // normalizedDistanceDictionary["mouth/mouth-scale-vert-decr|incr"] = normalizeminus11(distanceYLips, 0.076, 0.171);

    //Larghezza del labbro inferiore
    let distanceLipsWidthDown = Math.abs(downOpenMouth.y - lipsCoord[0].y);
    distanceDictionary["distanceLipsWidthDown"] = distanceLipsWidthDown;
    // normalizedDistanceDictionary["mouth/mouth-lowerlip-height-decr|incr"] = normalizeminus11(distanceLipsWidthDown, 0.001, 0.112);
    normalizedDistanceDictionary["mouth/mouth-lowerlip-height-decr|incr"] = normalizeminus11(distanceLipsWidthDown, 0.037, 0.084);

    //Larghezza del labbro superiore
    let distanceLipsWidthUp = Math.abs(upOpenMouth.y - lipsCoord[1].y);
    distanceDictionary["distanceLipsWidthUp"] = distanceLipsWidthUp;
    normalizedDistanceDictionary["mouth/mouth-upperlip-height-decr|incr"] = normalizeminus11(distanceLipsWidthUp, 0.025, 0.06);

    //Cupid Bow Width
    //Distanza x tra i punti esterni del cupid bow
    let cupidBowSx = normalizedLandmarks[0][37];
    let cupidBowDx = normalizedLandmarks[0][267];

    let distanceCupidBow = Math.abs(cupidBowSx.x - cupidBowDx.x);
    distanceDictionary["distanceCupidBow"] = distanceCupidBow;
    normalizedDistanceDictionary["mouth/mouth-cupidsbow-width-decr|incr"] = normalizeminus11(distanceCupidBow, 0.061, 0.136);

    //Cupid Bow Shape
    //Distanza media y tra i punti esterni del cupid bow e il punto superiore del labbro
    let distanceCupidBowY = (Math.abs(cupidBowSx.y - lipsCoord[1].y) + Math.abs(cupidBowDx.y - lipsCoord[1].y))/2;
    distanceDictionary["distanceCupidBowY"] = distanceCupidBowY;
    normalizedDistanceDictionary["mouth/mouth-cupidsbow-decr|incr"] = normalizeminus11(distanceCupidBowY, 0.005, 0.012);

}