'use client';

import { Alert, Empty, Image, Space, Spin, Tooltip, message } from 'antd';
import {
  DownloadOutlined,
  EditOutlined,
  LinkOutlined,
  RotateLeftOutlined,
  RotateRightOutlined,
  SwapOutlined,
  ZoomInOutlined,
  ZoomOutOutlined,
} from '@ant-design/icons';
import { FC, useEffect, useState } from 'react';

const PreviewGroup = Image.PreviewGroup;

// TODO: replace with actual images from the server
// const src = 'https://picsum.photos/500';
// const images = Array.from({ length: 20 }, (_, i) => ({
//   width: 200,
//   height: 200,
//   src:
//     i == 0
//       ? 'https://images.unsplash.com/photo-1712698396006-1996dc7cb2cc?q=80&w=2701&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
//       : `${src}?random=${i}`,
// }));

type Props = {
  refresh: boolean;
};

type Img = {
  image: string;
  bucket: string;
  name: string;
}

type PhotoData = {
  images: Img[];
};

// const url = 'http://www.isislab.it:3004/api/photos';
// const url = 'http://localhost:3000/api/photos';

const fallback =
  'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMIAAADDCAYAAADQvc6UAAABRWlDQ1BJQ0MgUHJvZmlsZQAAKJFjYGASSSwoyGFhYGDIzSspCnJ3UoiIjFJgf8LAwSDCIMogwMCcmFxc4BgQ4ANUwgCjUcG3awyMIPqyLsis7PPOq3QdDFcvjV3jOD1boQVTPQrgSkktTgbSf4A4LbmgqISBgTEFyFYuLykAsTuAbJEioKOA7DkgdjqEvQHEToKwj4DVhAQ5A9k3gGyB5IxEoBmML4BsnSQk8XQkNtReEOBxcfXxUQg1Mjc0dyHgXNJBSWpFCYh2zi+oLMpMzyhRcASGUqqCZ16yno6CkYGRAQMDKMwhqj/fAIcloxgHQqxAjIHBEugw5sUIsSQpBobtQPdLciLEVJYzMPBHMDBsayhILEqEO4DxG0txmrERhM29nYGBddr//5/DGRjYNRkY/l7////39v///y4Dmn+LgeHANwDrkl1AuO+pmgAAADhlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAAqACAAQAAAABAAAAwqADAAQAAAABAAAAwwAAAAD9b/HnAAAHlklEQVR4Ae3dP3PTWBSGcbGzM6GCKqlIBRV0dHRJFarQ0eUT8LH4BnRU0NHR0UEFVdIlFRV7TzRksomPY8uykTk/zewQfKw/9znv4yvJynLv4uLiV2dBoDiBf4qP3/ARuCRABEFAoBEgghggQAQZQKAnYEaQBAQaASKIAQJEkAEEegJmBElAoBEgghggQAQZQKAnYEaQBAQaASKIAQJEkAEEegJmBElAoBEgghggQAQZQKAnYEaQBAQaASKIAQJEkAEEegJmBElAoBEgghggQAQZQKAnYEaQBAQaASKIAQJEkAEEegJmBElAoBEgghggQAQZQKAnYEaQBAQaASKIAQJEkAEEegJmBElAoBEgghggQAQZQKAnYEaQBAQaASKIAQJEkAEEegJmBElAoBEgghggQAQZQKAnYEaQBAQaASKIAQJEkAEEegJmBElAoBEgghggQAQZQKAnYEaQBAQaASKIAQJEkAEEegJmBElAoBEgghggQAQZQKAnYEaQBAQaASKIAQJEkAEEegJmBElAoBEgghggQAQZQKAnYEaQBAQaASKIAQJEkAEEegJmBElAoBEgghggQAQZQKAnYEaQBAQaASKIAQJEkAEEegJmBElAoBEgghggQAQZQKAnYEaQBAQaASKIAQJEkAEEegJmBElAoBEgghgg0Aj8i0JO4OzsrPv69Wv+hi2qPHr0qNvf39+iI97soRIh4f3z58/u7du3SXX7Xt7Z2enevHmzfQe+oSN2apSAPj09TSrb+XKI/f379+08+A0cNRE2ANkupk+ACNPvkSPcAAEibACyXUyfABGm3yNHuAECRNgAZLuYPgEirKlHu7u7XdyytGwHAd8jjNyng4OD7vnz51dbPT8/7z58+NB9+/bt6jU/TI+AGWHEnrx48eJ/EsSmHzx40L18+fLyzxF3ZVMjEyDCiEDjMYZZS5wiPXnyZFbJaxMhQIQRGzHvWR7XCyOCXsOmiDAi1HmPMMQjDpbpEiDCiL358eNHurW/5SnWdIBbXiDCiA38/Pnzrce2YyZ4//59F3ePLNMl4PbpiL2J0L979+7yDtHDhw8vtzzvdGnEXdvUigSIsCLAWavHp/+qM0BcXMd/q25n1vF57TYBp0a3mUzilePj4+7k5KSLb6gt6ydAhPUzXnoPR0dHl79WGTNCfBnn1uvSCJdegQhLI1vvCk+fPu2ePXt2tZOYEV6/fn31dz+shwAR1sP1cqvLntbEN9MxA9xcYjsxS1jWR4AIa2Ibzx0tc44fYX/16lV6NDFLXH+YL32jwiACRBiEbf5KcXoTIsQSpzXx4N28Ja4BQoK7rgXiydbHjx/P25TaQAJEGAguWy0+2Q8PD6/Ki4R8EVl+bzBOnZY95fq9rj9zAkTI2SxdidBHqG9+skdw43borCXO/ZcJdraPWdv22uIEiLA4q7nvvCug8WTqzQveOH26fodo7g6uFe/a17W3+nFBAkRYENRdb1vkkz1CH9cPsVy/jrhr27PqMYvENYNlHAIesRiBYwRy0V+8iXP8+/fvX11Mr7L7ECueb/r48eMqm7FuI2BGWDEG8cm+7G3NEOfmdcTQw4h9/55lhm7DekRYKQPZF2ArbXTAyu4kDYB2YxUzwg0gi/41ztHnfQG26HbGel/crVrm7tNY+/1btkOEAZ2M05r4FB7r9GbAIdxaZYrHdOsgJ/wCEQY0J74TmOKnbxxT9n3FgGGWWsVdowHtjt9Nnvf7yQM2aZU/TIAIAxrw6dOnAWtZZcoEnBpNuTuObWMEiLAx1HY0ZQJEmHJ3HNvGCBBhY6jtaMoEiJB0Z29vL6ls58vxPcO8/zfrdo5qvKO+d3Fx8Wu8zf1dW4p/cPzLly/dtv9Ts/EbcvGAHhHyfBIhZ6NSiIBTo0LNNtScABFyNiqFCBChULMNNSdAhJyNSiECRCjUbEPNCRAhZ6NSiAARCjXbUHMCRMjZqBQiQIRCzTbUnAARcjYqhQgQoVCzDTUnQIScjUohAkQo1GxDzQkQIWejUogAEQo121BzAkTI2agUIkCEQs021JwAEXI2KoUIEKFQsw01J0CEnI1KIQJEKNRsQ80JECFno1KIABEKNdtQcwJEyNmoFCJAhELNNtScABFyNiqFCBChULMNNSdAhJyNSiECRCjUbEPNCRAhZ6NSiAARCjXbUHMCRMjZqBQiQIRCzTbUnAARcjYqhQgQoVCzDTUnQIScjUohAkQo1GxDzQkQIWejUogAEQo121BzAkTI2agUIkCEQs021JwAEXI2KoUIEKFQsw01J0CEnI1KIQJEKNRsQ80JECFno1KIABEKNdtQcwJEyNmoFCJAhELNNtScABFyNiqFCBChULMNNSdAhJyNSiECRCjUbEPNCRAhZ6NSiAARCjXbUHMCRMjZqBQiQIRCzTbUnAARcjYqhQgQoVCzDTUnQIScjUohAkQo1GxDzQkQIWejUogAEQo121BzAkTI2agUIkCEQs021JwAEXI2KoUIEKFQsw01J0CEnI1KIQJEKNRsQ80JECFno1KIABEKNdtQcwJEyNmoFCJAhELNNtScABFyNiqFCBChULMNNSdAhJyNSiEC/wGgKKC4YMA4TAAAAABJRU5ErkJggg==';

const Gallery: FC<Props> = ({ refresh }) => {
  const [photos, setPhotos] = useState<Img[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    setLoading(true);
    const fetchPhotos = async () => {
      try {
        const response: Response = await fetch(process.env.NEXT_PUBLIC_GALLERY as string);
        console.log('response:', response);
        const body = await response.json();
        console.log('body:', body);

        if (Object.keys(body ?? {}).includes('error')) {
          message.error('Error fetching photos:', body.error);
        } else {
          const data = body as PhotoData;
          setPhotos(data.images);
        }
        setLoading(false);
      } catch (error: any) {
        console.error('Error fetching photos.', error);
        message.error('Error fetching photo.');
      }
    };

    fetchPhotos();
  }, [refresh]);

  const images = photos.map((photo) => ({
    width: 250,
    height: 250,
    src: `data:image/png;base64,${photo.image}`,
    bucket: photo.bucket,
    name: photo.name,
  }));

  const onDownload = (imgIndex: number) => {
    const img = images[imgIndex];
    fetch(img.src)
      .then((response) => response.blob())
      .then((blob) => {
        const url = URL.createObjectURL(new Blob([blob]));
        const link = document.createElement('a');
        link.href = url;
        link.download = 'image.png';
        document.body.appendChild(link);
        link.click();
        URL.revokeObjectURL(url);
        link.remove();
      });
  };

  const linkToAvatar = (imgIndex: number, type: string) => {
    const img = images[imgIndex];
    const name = img.name;
    const bucket = img.bucket;
    const url = `${process.env.NEXT_PUBLIC_DOWNLOAD_FBX as string}?name=${name}&bucket=${bucket}&type=${type}`;
    navigator.clipboard.writeText(url);
    message.success(`Copied link to your ${type.toUpperCase()} avatar`);
  }

  const onDownloadAvatar = async (imgIndex: number, type: string) => {
    const img = images[imgIndex];
    const name = img.name;
    const bucket = img.bucket;
    try {
      const response = await fetch(process.env.NEXT_PUBLIC_DOWNLOAD_FBX as string, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          bucket,
          type,
        }),
      });

      if (!response.ok) {
        console.log(`failed to download ${type} avatar`);
        message.error(`Failed to download your ${type.toUpperCase()} avatar`);
        return;
      }

      const blob = await response.blob();
      if (blob.size < 1) {
        console.log(`failed to download ${type} avatar because it is empty`);
        message.error(`Use the Customize button to create your ${type.toUpperCase()} avatar first`);
        return;
      }

      let ext = 'mhm';
      if (type === 'fbx') {
        ext = 'zip';
      }
      if (type === 'glb') {
        ext = 'glb';
      }

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `avatar.${ext}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      message.success(`Your ${type.toUpperCase()} avatar was downloaded successfully`);
    } catch (error) {
      console.error('failed to download fbx avatar:', error);
    }
  };

  const getImgBucket = (imgIndex: number): string => {
    const img = images[imgIndex];
    return img.bucket;
  };

  const getImgName = (imgIndex: number): string => {
    const img = images[imgIndex];
    return img.name;
  };

  if (loading) {
    return (
      <div>
        <Spin size='large' /> Loading...
      </div>
    );
  }

  if (!loading && photos.length === 0) {
    return (
      <Empty
        description={
          <Alert
            message='No images found. Upload a picture to get started!'
            type='info'
          />
        }
      ></Empty>
    );
  }

  return (
    <div id='gallery'>
      <PreviewGroup
        preview={{
          countRender: () => null,
          toolbarRender: (
            _,
            {
              transform: { scale },
              actions: {
                onFlipY,
                onFlipX,
                onRotateLeft,
                onRotateRight,
                onZoomOut,
                onZoomIn,
              },
              current,
            }
          ) => {
            // TODO: handle max zoom in and outs
            return (
              <Space size={30} className='toolbar-wrapper'>
                <DownloadOutlined
                  onClick={() => onDownload(current)}
                  className='toolbar-icon'
                />
                <SwapOutlined
                  rotate={90}
                  onClick={onFlipY}
                  className='toolbar-icon'
                />
                <SwapOutlined onClick={onFlipX} className='toolbar-icon' />
                <RotateLeftOutlined
                  onClick={onRotateLeft}
                  className='toolbar-icon'
                />
                <RotateRightOutlined
                  onClick={onRotateRight}
                  className='toolbar-icon'
                />
                <ZoomOutOutlined
                  disabled={scale === 1}
                  onClick={onZoomOut}
                  className='toolbar-icon'
                />
                <ZoomInOutlined
                  disabled={scale === 50}
                  onClick={onZoomIn}
                  className='toolbar-icon'
                />
                <Tooltip title='Customize your Avatar!'>
                  <a
                    href={`${process.env.NEXT_PUBLIC_UNITY as string}?id=${getImgBucket(current)}&name=${getImgName(current)}`}
                    target='_blank'
                    className='toolbar-icon'
                  >
                    <div style={{ textAlign: 'center' }}>
                      <EditOutlined /> <br/> Customize
                    </div>
                  </a>
                </Tooltip>
                <Tooltip title={(
                  <div className='text-center'>
                    Download your Makehuman Avatar (.mhm).
                    <br />
                    <br />
                    You need to first create your Makehuman Avatar using the Customize button!
                  </div>
                )}>
                  <div
                    onClick={() => onDownloadAvatar(current, 'mhm')}
                    className='toolbar-icon'
                    style={{ textAlign: 'center' }}
                  >
                    <DownloadOutlined /> <br/> Makehuman
                  </div>
                </Tooltip>
                <Tooltip title={(
                  <div className='text-center'>
                    Download your FBX Avatar (.fbx).
                    <br />
                    <br />
                    You need to first create your FBX Avatar using the Customize button!
                  </div>
                )}>
                  <div
                    onClick={() => onDownloadAvatar(current, 'fbx')}
                    className='toolbar-icon'
                    style={{ textAlign: 'center' }}
                  >
                    <DownloadOutlined /> <br/> FBX
                  </div>
                </Tooltip>
                <Tooltip title={(
                  <div className='text-center'>
                    Link to FBX Avatar (.fbx).
                    <br />
                    <br />
                    You need to first create your FBX Avatar using the Customize button!
                  </div>
                )}>
                  <div
                    onClick={() => linkToAvatar(current, 'fbx')}
                    className='toolbar-icon'
                    style={{ textAlign: 'center' }}
                  >
                    <LinkOutlined /> <br/> to FBX Avatar
                  </div>
                </Tooltip>
                <Tooltip title={(
                  <div className='text-center'>
                    Download your GLB Avatar (.glb).
                    <br />
                    <br />
                    You need to first create your GLB Avatar using the Customize button!
                  </div>
                )}>
                  <div
                    onClick={() => onDownloadAvatar(current, 'glb')}
                    className='toolbar-icon'
                    style={{ textAlign: 'center' }}
                  >
                    <DownloadOutlined /> <br/> GLB
                  </div>
                </Tooltip>
                <Tooltip title={(
                  <div className='text-center'>
                    Link to GLB Avatar (.glb).
                    <br />
                    <br />
                    You need to first create your GLB Avatar using the Customize button!
                  </div>
                )}>
                  <div
                    onClick={() => linkToAvatar(current, 'glb')}
                    className='toolbar-icon'
                    style={{ textAlign: 'center' }}
                  >
                    <LinkOutlined /> <br/> to GLB Avatar
                  </div>
                </Tooltip>
              </Space>
            );
          },
        }}
      >
        {images.map(({ width, height, src }, i) => (
          <Image
            alt={`Image ${i}`}
            key={i}
            height={height}
            src={src}
            fallback={fallback}
            className='p-0.5 border-gray-200 shadow-lg'
            preview={{
              mask: 'Preview & Customize',
              visible: true,
            }}
          />
        ))}
      </PreviewGroup>
    </div>
  );
};

export default Gallery;
