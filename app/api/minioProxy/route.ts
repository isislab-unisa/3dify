import AWS from 'aws-sdk';
import {
  DeleteObjectRequest,
  GetObjectRequest,
} from 'aws-sdk/clients/s3';
import { Buffer } from 'buffer';

export async function GET(req: Request) {
  const s3 = new AWS.S3({
    region: 'localhost',
    endpoint: 'http://filestore:9000',
    accessKeyId: 'admin',
    secretAccessKey: 'minioadmin',
    s3ForcePathStyle: true, // Required for MinIO
  });

  const { searchParams } = new URL(req.url)
  const bucket = searchParams.get('bucket')
  const filename = searchParams.get('filename')

  try {

    const getObjectParams: GetObjectRequest = {
        Bucket: bucket as string,
        Key: filename as string
        };
    const fileContent = await s3.getObject(getObjectParams).promise();
    if (!fileContent.Body) {
        return Response.json("File not found");
    }
    const base64File = Buffer.from(fileContent.Body as any).toString('base64');
    return Response.json({ code: '200', status: 'OK', message: base64File });
    }
   catch (error) {
    console.error('Failed to retrieve file:', error);
    return Response.json({ code: '400', status: 'error', error: 'Failed to retrieve file' });
  }
}

type DeleteReqBody = {
    bucket: string,
    file: string
  };

export async function DELETE(req: Request) {
  const s3 = new AWS.S3({
    region: 'localhost',
    endpoint: 'http://filestore:9000',
    accessKeyId: 'admin',
    secretAccessKey: 'minioadmin',
    s3ForcePathStyle: true, // Required for MinIO
  });

  try {
    const body: DeleteReqBody = await req.json();
    const deleteObjectParams: DeleteObjectRequest = {
        Bucket: body.bucket,
        Key: body.file
      };
    await s3.deleteObject(deleteObjectParams).promise();
    return Response.json({ code: '200', status: 'OK',message: 'File deleted'});
  } catch (error) {
    console.error('Failed to delete file:', error);
    return Response.json({ code: '400', status: 'error', error: 'Failed to delete file' });
  }
}

type PostReqBody = {
    bucket: string,
    file: string,
    fileType: string,
    fileContent64: string
  };

export async function POST(req: Request) {
  const s3 = new AWS.S3({
    region: 'localhost',
    endpoint: 'http://filestore:9000',
    accessKeyId: 'admin',
    secretAccessKey: 'minioadmin',
    s3ForcePathStyle: true, // Required for MinIO
  });

  try {
    const body: PostReqBody = await req.json();
    const buffer = Buffer.from(body.fileContent64, 'base64');
    await s3.upload({
        Bucket: body.bucket,
        Key: body.file,
        Body: buffer,
        ContentType: body.fileType
    })
    .promise();
    return Response.json({ code: '200', status: 'OK',message: 'File uploaded'});
  } catch (error) {
    console.error('Failed to upload file:', error);
    return Response.json({ code: '400', status: 'error', error: 'Failed to upload file' });
  }
}
