'use client';

import { Dispatch, FC, SetStateAction, useState } from 'react';
import { InboxOutlined } from '@ant-design/icons';
import { message, Upload } from 'antd';

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

  const beforeUpload = (file: any) => {
    const isImage = file.type.includes('image');
    if (!isImage) {
      message.error(`${file.name} is not an image file.`);
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
    </div>
  );
};

export default UploadArea;
