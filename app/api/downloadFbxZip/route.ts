import path from 'path';
import exec from 'exec';

import AdmZip from 'adm-zip';

export async function GET(req: Request) {
    // TODO fix path
    exec('python3 ' + path.join(__dirname, '..', '..', 'internal', 'MakehumanSocketClient', 'mhrc', 'genericCommand.py') + ' exportFbx',
    (err: any, stdout: any, stderr: any) => {
      if (err) {
        console.error(`exec error: ${err}`);
        return Response.json({ code: '500', status: 'Can\'t access makehuman server', message: {err}} );
      }
      var zip = new AdmZip();
      // add local file
      var tempFolder = `${stdout}`.replace(/(\r\n|\n|\r)/gm, "");
      zip.addLocalFile(path.join(tempFolder, 'myHuman.fbx'));
      zip.addLocalFolder(path.join(tempFolder, 'textures/'), "/textures");
      // get everything as a buffer
      var zipFileContents = zip.toBuffer();
      /*
      const fileName = 'avatar.zip';
      const fileType = 'application/zip';
      res.writeHead(200, {
          'Content-Disposition': `attachment; filename="${fileName}"`,
          'Content-Type': fileType,
        })*/
      
      console.log(`${stdout}`);
      return Response.json({ code: '200', status: 'OK', message: zipFileContents });
    });
}
