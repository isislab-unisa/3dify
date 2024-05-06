type Body = {
  landmarks: any;
  normalizedLandmarks: any;
  age: number;
  gender: number;
};

export async function GET(req: Request) {
  // get normalized mediapipe landmarks, faceapi age and gender from request json
  const body: Body = await req.json();

  // calculate makehuman parameters
  var makehumanParameters = GetMakehumanParametersFromLandmarks(body.normalizedLandmarks, body.age, body.gender);

  // write and makehuman parameters dictionary to response json

  return Response.json({ code: '200', status: 'OK', message: {makehumanParameters: makehumanParameters} });
}
