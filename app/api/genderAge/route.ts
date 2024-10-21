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
    const responseBody = JSON.stringify({code:'202', status:"ERROR", message: "Error in faceapi detection", age: defaultAge, gender: defaultGender});
    return new Response(responseBody, responseInit);
}
}
