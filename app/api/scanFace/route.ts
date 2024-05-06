type Body = {
  img: any;
};

export async function GET(req: Request) {
  // TODO get photo from uuid 
  const body: Body = await req.json();

  // run faceapi and mediapipe on photo
  var scanFaceOut =  await GetLandmarksFromPhoto(body.img);

  // extract normalized mediapipe landmarks, faceapi age and gender, minio guid and write it to the response
  return Response.json({ code: '200', status: 'OK', message: scanFaceOut });
}
