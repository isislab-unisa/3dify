import { GetLandmarksFromPhoto } from "@/app/internal/scanface";

type Body = {
  img: string,
  width: number
};

export async function POST(req: Request) {  
  const body: Body = await req.json();

  // run faceapi and mediapipe on photo
  const scanFaceOut = await GetLandmarksFromPhoto(body.img, body.width);

  // extract normalized mediapipe landmarks, faceapi age and gender, minio guid and write it to the response
  return Response.json({ code: '200', status: 'OK', message: scanFaceOut });
}
