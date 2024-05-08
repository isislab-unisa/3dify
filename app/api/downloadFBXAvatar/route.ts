import { downloadFBX, sendJsonModifiers } from "@/app/internal/downloadFBXAvatar";

type Body = {
  makehumanParameters: any;
};

export async function GET(req: Request) {
  // get makehuman parameters from request
  const body: Body = await req.json();

  // use makehuman sockets to apply modifiers got from parameters (sendJsonModifiers)
  await sendJsonModifiers(body.makehumanParameters);

  // get fbx from makehuman daemon (applySliderValuesAndDownloadFbx)
  const outputFBX = await downloadFBX();

  return Response.json({ code: '200', status: 'OK', message: outputFBX });
}


