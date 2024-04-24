'use client';

import { FC } from 'react';
import { InboxOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import { message, Upload } from 'antd';

const { Dragger } = Upload;

const mockAction = 'https://660d2bd96ddfa2943b33731c.mockapi.io/api/upload';

const props: UploadProps = {
  method: 'POST',
  action: mockAction,
  name: 'file',
  multiple: false,
  listType: 'picture',
  beforeUpload: (file) => {
    const isImage = file.type.includes('image');
    if (!isImage) {
      message.error(`${file.name} is not an image file.`);
    }
    return isImage || Upload.LIST_IGNORE;
  },
  onChange(info) {
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
  },
  onDrop(e) {
    console.log('Dropped files', e.dataTransfer.files);
  },
};

const UploadArea: FC = () => (
  <div id='upload-area' className='mb-10'>
    <Dragger {...props}>
      <p className='ant-upload-drag-icon'>
        <InboxOutlined />
      </p>
      <p className='ant-upload-text'>Click or Drag your Picture to Upload!</p>
    </Dragger>
  </div>
);

export default UploadArea;
