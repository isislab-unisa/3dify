import AWS from "aws-sdk";
import { GetObjectRequest, ListObjectsV2Request } from "aws-sdk/clients/s3";

type Body = {
    bucket: string;
    name: string;
    type: 'fbx' | 'mhm' | 'glb';
};

export async function POST(req: Request) {
    try {
        const s3 = new AWS.S3({
            region: process.env.MINIO_REGION as string,
            endpoint: process.env.MINIO_ENDPOINT as string,
            accessKeyId: process.env.MINIO_ACCESS_KEY as string,
            secretAccessKey: process.env.MINIO_SECRET_KEY as string,
            s3ForcePathStyle: true, // required for MinIO
        });

        const body: Body = await req.json();
        let prefix = 'avatar.mhm';
        if (body.type === 'fbx') {
            prefix = 'avatar.zip';
        }
        if (body.type === 'glb') {
            prefix = 'avatar.glb';
        }

        console.log('downloading avatar:',  prefix);
        const listObjectsParams: ListObjectsV2Request = {
            Bucket: body.bucket,
            Prefix: prefix,
        };

        const objectsData = await s3.listObjectsV2(listObjectsParams).promise();
        const objects = objectsData.Contents;
        if (!objects) {
            return Response.json({ message: 'failed to download fbx avatar' });
        }

        for (const object of objects) {
            if (object.Key !== prefix) {
                continue;
            }

            const getObjectParams: GetObjectRequest = {
                Bucket: body.bucket,
                Key: object.Key as string,
            };

            const headData = await s3.headObject(getObjectParams).promise();
            const avatarData = await s3.getObject(getObjectParams).promise();
            
            // set headers to prompt file download
            const headers = new Headers();
            headers.set('Content-Disposition', `attachment; filename="${prefix}"`);
            headers.set('Content-Type', body.type === 'fbx' ? 'application/zip' : 'application/octet-stream');
            headers.set('Content-Length', headData.ContentLength?.toString() || '0');

            return new Response(Buffer.from(avatarData.Body as any), { headers });
        }

        const emptyBuffer = Buffer.alloc(0);
        return new Response(emptyBuffer);
    } catch (error) {
        console.error('failed to download fbx avatar:', error);
        return Response.json({ error: 'failed to download fbx avatar' });
    }
}

export async function GET(req: Request) {
    try {
        const url = new URL(req.url);
        const queryParams = new URLSearchParams(url.search);

        const s3 = new AWS.S3({
            region: process.env.MINIO_REGION as string,
            endpoint: process.env.MINIO_ENDPOINT as string,
            accessKeyId: process.env.MINIO_ACCESS_KEY as string,
            secretAccessKey: process.env.MINIO_SECRET_KEY as string,
            s3ForcePathStyle: true, // required for MinIO
        });

        const type = queryParams.get('type') || ''; // defaults to an empty string if not provided
        const bucket = queryParams.get('bucket');
        if (!bucket) {
            return Response.json({ error: 'Bucket parameter is required' }, { status: 400 });
        }

        let prefix = 'avatar.mhm';
        if (type === 'fbx') {
            prefix = 'avatar.zip';
        } else if (type === 'glb') {
            prefix = 'avatar.glb';
        }

        console.log('GET downloading avatar:', prefix);
        const listObjectsParams: ListObjectsV2Request = {
            Bucket: bucket,
            Prefix: prefix,
        };

        const objectsData = await s3.listObjectsV2(listObjectsParams).promise();
        const objects = objectsData.Contents;
        if (!objects) {
            return Response.json({ message: 'failed to download avatar' });
        }

        for (const object of objects) {
            if (object.Key !== prefix) {
                continue;
            }

            const getObjectParams: GetObjectRequest = {
                Bucket: bucket,
                Key: object.Key as string,
            };

            const headData = await s3.headObject(getObjectParams).promise();
            const avatarData = await s3.getObject(getObjectParams).promise();

            // set headers to prompt file download
            const headers = new Headers();
            headers.set('Content-Disposition', `attachment; filename="${prefix}"`);
            headers.set('Content-Type', type === 'fbx' ? 'application/zip' : 'application/octet-stream');
            headers.set('Content-Length', headData.ContentLength?.toString() || '0');

            return new Response(Buffer.from(avatarData.Body as any), { headers });
        }

        const emptyBuffer = Buffer.alloc(0);
        return new Response(emptyBuffer);
    } catch (error) {
        console.error('failed to download avatar:', error);
        return Response.json({ error: 'failed to download avatar' });
    }
}