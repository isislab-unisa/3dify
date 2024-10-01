'use client';

import { Dispatch, FC, SetStateAction, useState } from 'react';
import { InboxOutlined } from '@ant-design/icons';
import { Alert, message, Upload } from 'antd';
import { useSession } from 'next-auth/react';
import Image from 'next/image';
import Title from 'antd/es/typography/Title';

type Props = {
  setRefresh: Dispatch<SetStateAction<boolean>>;
};

type FileInfo = {
  name: string;
  ext: string;
  type: string;
};

const { Dragger } = Upload;

// const url = 'http://www.isislab.it:3004/api/uploadPhoto';
// const url = 'http://localhost:3000/api/uploadPhoto';

const UploadArea: FC<Props> = ({ setRefresh }) => {
  const [fileInfo, setFileInfo] = useState<FileInfo>({
    name: '',
    ext: '',
    type: '',
  });

  const { data: session, status, update } = useSession();
  if (!session || !session.user) {
    return (
      <Alert
        message='Login to upload'
        description="Login to start uploading your pictures."
        type="warning"
        className='mb-10'
      />
    );
  }

  const beforeUpload = (file: any) => {
    const isImage = file.type.includes('image');
    if (!isImage) {
      message.error(`${file.name} is not an image file.`);
      return false;
    }
    const isJpegOrPng = file.type.includes('png') || file.type.includes('jpeg') || file.type.includes('jpg');
    if (!isJpegOrPng) {
        message.error(`${file.name} is not a PNG or JPEG file.`);
        return false;
    }
    const ext = file.name.split('.').pop();
    setFileInfo({ name: file.name, ext: ext, type: file.type });
    return isImage || Upload.LIST_IGNORE;
  };

  const onChange = (info: any) => {
    const { status } = info.file;
    if (status !== 'uploading') {
      // console.log(
      //   'info',
      //   info,
      //   'info.file ->',
      //   info.file,
      //   'info.fileList ->',
      //   info.fileList
      // );
    }
    if (status === 'done') {
      message.success(`${info.file.name} file uploaded successfully.`);
    } else if (status === 'error') {
      message.error(`${info.file.name} file upload failed.`);
    }
  };

  const customRequest = async (options: any) => {
    const { file, onSuccess, onError } = options;

    try {
      // Read the file as base64
      const reader = new FileReader();

      reader.onload = async (event: any) => {
        const base64Data = event.target.result;

        const response: Response = await fetch(process.env.NEXT_PUBLIC_UPLOAD as string, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            file: base64Data,
            filename: fileInfo.name,
            type: fileInfo.type,
          }),
        });

        const body = await response.json();

        if (Object.keys(body ?? {}).includes('error')) {
          console.log('keys', Object.keys(body ?? {}));
          onError('Failed to upload file');
        } else {
          console.log('keys success', Object.keys(body ?? {}));

          const response: Response = await fetch(process.env.NEXT_PUBLIC_ADD_IMAGE_ID as string, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              email: session?.user?.email,
              imageId: body.bucketName,
            }),
          });
          await response.json()

          setRefresh((prev) => !prev);
          onSuccess();
        }
      };

      reader.readAsDataURL(file);
    } catch (error) {
      onError('Failed to upload file');
    }
  };

  return (
    <div id='upload-area' className='mb-10'>
      <Dragger
        multiple={false}
        listType='picture'
        customRequest={customRequest}
        beforeUpload={beforeUpload}
        onChange={onChange}
        // onDrop={(e) => console.log('Dropped files', e.dataTransfer.files)}
      >
        <p className='ant-upload-drag-icon'>
          <InboxOutlined />
        </p>
        <p className='ant-upload-text'>Click or drag your picture to upload!</p>
      </Dragger>

      <div className='mt-10 flex justify-center'>
        <div className='border-2 flex border-gray-200 pr-8 rounded-xl shadow-xl'>
          <Image
            src='/passport.jpg'
            alt='Passport'
            width={400}
            height={200}
            priority
          />
          <div className='mb-5 ml-10 mt-[7%]'>
            <Title className='inline' level={2}>
              {'You don\'t know which picture to upload?'}
            </Title>
            <br />
            <Title className='inline' level={2}>
              {'We have the perfect example for you!'}
            </Title>
            <br />
            <Title className='inline' level={2}>
              {'Try to look like this passport guy!'}
            </Title>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadArea;
