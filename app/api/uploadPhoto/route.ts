import { NextApiRequest } from 'next';
import AWS from 'aws-sdk';
import { Readable } from 'stream';
import { headers } from 'next/headers';

export async function POST(req: NextApiRequest) {
  try {
    const s3 = new AWS.S3({
      region: 'localhost',
      endpoint: 'http://filestore:9000',
      accessKeyId: 'admin',
      secretAccessKey: 'minioadmin',
      s3ForcePathStyle: true, // Required for MinIO
    });

    const fileBuffer: Buffer = req.body;
    const fileName: string = headers().get('filename') as string;
    const fileExt: string = headers().get('fileext') as string;
    const fileType: string = headers().get('type') as string;

    // Create bucket with the name of the file
    const bucketName: string = fileName
      .toLowerCase()
      .replace(/[^a-z0-9]/g, '-');
    const bucketExists = await s3
      .headBucket({ Bucket: bucketName })
      .promise()
      .then(() => true)
      .catch(() => false);
    if (!bucketExists) {
      await s3.createBucket({ Bucket: bucketName }).promise();
    }

    // Upload file to the created bucket
    await s3
      .upload({
        Bucket: bucketName,
        Key: `${fileName}`,
        Body: Readable.from(fileBuffer),
        ContentType: fileType,
      })
      .promise();

    return Response.json({ message: 'File uploaded successfully' });
  } catch (error) {
    console.error('Error:', error);
    return Response.json({ error: 'Failed to upload file' });
  }
}
