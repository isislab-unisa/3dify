import { GetGenderAndAgeFromPhoto } from "@/app/internal/scanface";

type Body = {
  img: string,
  width: number
};

export async function OPTIONS(req: Request) {
  return Response.json({ code: '200', status: 'OK', message: 'OK' });
}

export async function POST(req: Request) {  
  const body: Body = await req.json();

  // run faceapi on photo
  const scanFaceOut = await GetGenderAndAgeFromPhoto(body.img, body.width);

  // extract faceapi age and gender
  return Response.json({ code: '200', status: 'OK', message: scanFaceOut });
}
