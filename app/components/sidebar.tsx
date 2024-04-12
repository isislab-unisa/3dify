'use client';

import { FC } from 'react';
import { Menu } from 'antd';
import { UploadOutlined, UserOutlined } from '@ant-design/icons';
import Sider from 'antd/es/layout/Sider';

const items = [
  {
    key: 'my-avatars',
    icon: <UploadOutlined />,
    label: 'My Avatars',
  },
  {
    key: 'logout',
    icon: <UserOutlined />,
    label: 'Logout',
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
        defaultSelectedKeys={['my-avatars']}
        onClick={({ key }) => {
          if (key === 'my-avatars') {
            // TODO: Implement my avatars
            console.log('My Avatars');
          }
          if (key === 'logout') {
            // TODO: Implement logout
            console.log('Logout');
          }
        }}
      >
        {items.map(({ key, icon, label }) => (
          <Menu.Item key={key} icon={icon}>
            {label}
          </Menu.Item>
        ))}
      </Menu>
    </Sider>
  );
};

export default Sidebar;
