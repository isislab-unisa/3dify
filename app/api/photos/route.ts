import AWS from 'aws-sdk';
import {
  DeleteBucketRequest,
  DeleteObjectRequest,
  GetObjectRequest,
  ListObjectsV2Request,
} from 'aws-sdk/clients/s3';
import { Buffer } from 'buffer';

type Img = {
  image: string;
  bucket: string;
  name: string;
};

export async function GET() {
  const s3 = new AWS.S3({
    region: process.env.MINIO_REGION as string,
    endpoint: process.env.MINIO_ENDPOINT as string,
    accessKeyId: process.env.MINIO_ACCESS_KEY as string,
    secretAccessKey: process.env.MINIO_SECRET_KEY as string,
    s3ForcePathStyle: true, // Required for MinIO
  });

  try {
    let images: Img[] = [];

    const data = await s3.listBuckets().promise();
    const buckets = data.Buckets;
    if (!buckets) {
      return Response.json({ images });
    }

    for (const bucket of buckets) {
      // List all objects in the bucket with the prefix 'image'
      const listObjectsParams: ListObjectsV2Request = {
        Bucket: bucket.Name as string,
        Prefix: 'image',
      };

      const objectsData = await s3.listObjectsV2(listObjectsParams).promise();
      const objects = objectsData.Contents;
      if (!objects) {
        return Response.json({ images });
      }

      for (const object of objects) {
        const getObjectParams: GetObjectRequest = {
          Bucket: bucket.Name as string,
          Key: object.Key as string,
        };

        const image = await s3.getObject(getObjectParams).promise();
        console.log({image}, getObjectParams.Key);
        if (!image.Body) {
          continue;
        }
        const base64Image = Buffer.from(image.Body as any).toString('base64');
        images.push({
          image: base64Image,
          bucket: bucket.Name as string,
          name: getObjectParams.Key,
        });
      }
    }

    return Response.json({ images });
  } catch (error) {
    console.error('Failed to retrieve images:', error);
    return Response.json({ error: 'Failed to retrieve images' });
  }
}

export async function DELETE() {
  const s3 = new AWS.S3({
    region: 'localhost',
    endpoint: 'http://filestore:9000',
    accessKeyId: 'admin',
    secretAccessKey: 'minioadmin',
    s3ForcePathStyle: true, // Required for MinIO
  });

  try {
    const data = await s3.listBuckets().promise();
    const buckets = data.Buckets;
    if (!buckets) {
      return Response.json({ error: 'No buckets found' });
    }

    for (const bucket of buckets) {
      // List all objects in the bucket with the prefix 'image'
      const listObjectsParams: ListObjectsV2Request = {
        Bucket: bucket.Name as string,
        Prefix: 'image',
      };

      const objectsData = await s3.listObjectsV2(listObjectsParams).promise();
      const objects = objectsData.Contents;
      if (!objects) {
        return Response.json({ error: 'No images found' });
      }

      for (const object of objects) {
        const deleteObjectParams: DeleteObjectRequest = {
          Bucket: bucket.Name as string,
          Key: object.Key as string,
        };

        await s3.deleteObject(deleteObjectParams).promise();
      }

      const deleteBucketParams: DeleteBucketRequest = {
        Bucket: bucket.Name as string,
      };
      await s3.deleteBucket(deleteBucketParams).promise();
    }

    return Response.json({
      message: 'Images and related buckets deleted successfully',
    });
  } catch (error) {
    console.error('Failed to delete images and related buckets:', error);
    return Response.json({
      error: 'Failed to delete images and related buckets',
    });
  }
}
