import fs from 'fs';
import path from 'path';
import exec from 'exec';

export async function POST(req: Request) {
    const body: Body = await req.json();
    console.log(body.text)
    // TODO fix this to run on typescript
    // TODO send json content instead of save file name
    fs.writeFile(path.join(__dirname, 'aaa.json'), body.text, (err) => {
    if (err) {
        return Response.json({ code: '500', status: 'Error on writing file', message: err });
    } else {
        // TODO fix path
        exec('python ' + path.join(__dirname, '..', '..', 'internal', 'MakehumanSocketClient', 'mhrc', 'applyModifiers.py')+ ' ' + path.join(__dirname, 'aaa.json'), 
            (err, stdout, stderr) => {
            if (err) {
                console.error(`exec error: ${err}`);
                return;
            }
            
            console.log(`${stdout}`);
            return Response.json({ code: '200', status: 'OK', message: 'OK' });

        });
    }
    })
}