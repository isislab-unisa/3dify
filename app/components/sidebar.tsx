'use client';

import { FC } from 'react';
import { Menu } from 'antd';
import { FileImageOutlined, UploadOutlined } from '@ant-design/icons';
import Sider from 'antd/es/layout/Sider';

const items = [
  {
    key: 'my-avatars',
    icon: <FileImageOutlined />,
    label: 'Pictures & Avatars',
  },
  {
    key: 'upload',
    icon: <UploadOutlined />,
    label: 'Upload',
  },
];

const Sidebar: FC = () => {
  return (
    <Sider
      theme='light'
      breakpoint='lg'
      collapsedWidth='0'
      style={{ backgroundColor: '#eaf4fc' }}
    >
      <Menu
        style={{ backgroundColor: '#eaf4fc' }}
        items={items}
        defaultSelectedKeys={['my-avatars']}
        onClick={({ key }) => {
          if (key === 'my-avatars') {
            // TODO: Implement my avatars
            console.log('My Avatars');
          }
          if (key === 'upload') {
            // TODO: Implement upload
            console.log('Upload');
          }
        }}
      />
    </Sider>
  );
};

export default Sidebar;
