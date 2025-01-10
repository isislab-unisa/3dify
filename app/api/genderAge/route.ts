/**
 * @swagger
 * /api/genderAge:
 *   post:
 *     description: Analyzes a photo for age and gender.
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - img
 *               - width
 *             properties:
 *               img:
 *                 type: string
 *                 format: base64
 *                 description: The base64-encoded image for analysis.
 *                 example: "iVBORw0KGgoAAAANSUhEUgAA... (base64 string)"
 *               width:
 *                 type: number
 *                 description: The width of the image (in pixels) for scaling.
 *                 example: 400
 *     responses:
 *       200:
 *         description: Successful analysis.
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 code:
 *                   type: string
 *                   description: A unique code for the response.
 *                   example: "200"
 *                 status:
 *                   type: string
 *                   description: Status of the analysis.
 *                   example: "OK"
 *                 message:
 *                   type: object
 *                   description: The output from faceapi.
 *                   properties:
 *                     age:
 *                       type: number
 *                       description: The predicted age of the person.
 *                       example: 25
 *                     gender:
 *                       type: string
 *                       description: The predicted gender of the person.
 *                       example: "male"
 *       202:
 *         description: Error in faceapi detection.
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 code:
 *                   type: string
 *                   description: A unique error code.
 *                 status:
 *                   type: string
 *                   description: Error status.
 *                 error:
 *                   type: string
 *                   description: A brief error message.
 *                 message:
 *                   type: object
 *                   description: Detailed error explanation.
 *                   properties:
 *                     age:
 *                       type: number
 *                       description: The default age (if available) in case of error.
 *                     gender:
 *                       type: string
 *                       description: The default gender (if available) in case of error.
 *     tags:
 *       - Face Analysis
 */
import { GetGenderAndAgeFromPhoto } from "@/app/internal/scanface";
import { Gender } from "face-api.js";

type Body = {
  img: string,
  width: number
};

export async function OPTIONS(req: Request) {
  return Response.json({ code: '200', status: 'OK', message: 'OK' });
}

export async function POST(req: Request) {  
  try{
    const body: Body = await req.json();

    // run faceapi on photo
    const scanFaceOut = await GetGenderAndAgeFromPhoto(body.img, body.width);
  
    // extract faceapi age and gender
    return Response.json({ code: '200', status: 'OK', message: scanFaceOut });
  }catch(e){
    console.error(e);
    const defaultAge = 50.0;
    const defaultGender = "male";
    const responseInit : ResponseInit = {status: 202, statusText: "Error in faceapi detection"};
    const responseContent = {age: defaultAge, gender: defaultGender};
    const responseBody = JSON.stringify({code:'202', status:"ERROR", error: "Error in faceapi detection", message: responseContent});
    return new Response(responseBody, responseInit);
}
}
