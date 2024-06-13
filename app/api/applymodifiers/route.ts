import path from 'path';
import {exec} from 'child_process';
import util from 'util';

type Body = {
    text: string;
};

export async function POST(req: Request) {
    const body: Body = await req.json();
    console.log(body.text)
    const proc: string = 'python3 ' + path.join('app', 'internal', 'MakehumanSocketClient', 'applyModifiers.py')+ ' \"' + body.text + '\"';
    console.log(proc)
    const execPromise = util.promisify(exec);
    try
    {
        const {stdout, stderr} = await execPromise(proc);
        console.log(stdout)        
        return Response.json({ code: '200', status: 'OK', message: 'OK' });
    }
    catch(error)
    {   
        console.log(error)     
        return Response.json({ code: '500', status: 'Error', message: 'Error' });        
    }
}
