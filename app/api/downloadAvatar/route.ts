import AWS from "aws-sdk";
import { GetObjectRequest, ListObjectsV2Request } from "aws-sdk/clients/s3";

type Body = {
    bucket: string;
    name: string;
    type: 'fbx' | 'mhm';
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
        const prefix = body.type === 'fbx' ? 'avatar.zip' : 'avatar.mhm';
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
            headers.set('Content-Disposition', `attachment; filename="${prefix}.${body.type === 'fbx' ? 'zip' : 'mhm'}"`);
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