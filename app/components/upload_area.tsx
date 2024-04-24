'use client';

import { FC, useState } from 'react';
import { InboxOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import { message, Upload } from 'antd';

const { Dragger } = Upload;

const mockAction = 'http://localhost:3000/api/uploadPhoto';

const UploadArea: FC = () => {
  const [fileInfo, setFileInfo] = useState<{
    name: string;
    ext: string;
    type: string;
  }>({ name: '', ext: '', type: '' });

  const beforeUpload = (file: any) => {
    const isImage = file.type.includes('image');
    if (!isImage) {
      message.error(`${file.name} is not an image file.`);
    }
    const ext = file.name.split('.').pop();
    setFileInfo({ name: file.name, ext: ext, type: file.type });
    console.log('fileInfo', { fileInfo });
    return isImage || Upload.LIST_IGNORE;
  };

  const onChange = (info: any) => {
    const { status } = info.file;
    if (status !== 'uploading') {
      console.log(
        'info',
        info,
        'info.file ->',
        info.file,
        'info.fileList ->',
        info.fileList
      );
    }
    if (status === 'done') {
      message.success(`${info.file.name} file uploaded successfully.`);
    } else if (status === 'error') {
      message.error(`${info.file.name} file upload failed.`);
    }
  };

  return (
    <div id='upload-area' className='mb-10'>
      <Dragger
        method='POST'
        action={mockAction}
        name='file'
        headers={{
          filename: fileInfo.name,
          fileext: fileInfo.ext,
          type: fileInfo.type,
        }}
        multiple={false}
        listType='picture'
        beforeUpload={beforeUpload}
        onChange={onChange}
        onDrop={(e) => console.log('Dropped files', e.dataTransfer.files)}
      >
        <p className='ant-upload-drag-icon'>
          <InboxOutlined />
        </p>
        <p className='ant-upload-text'>Click or Drag your Picture to Upload!</p>
      </Dragger>
    </div>
  );
};

export default UploadArea;
