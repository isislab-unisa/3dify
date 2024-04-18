'use client';

import { FC } from 'react';
import Image from 'next/image';
import { Header } from 'antd/es/layout/layout';
import Title from 'antd/es/typography/Title';
import { Button } from 'antd';

const Navbar: FC = () => {
  return (
    <Header
      className='flex w-full justify-between'
      style={{ backgroundColor: '#eaf4fc' }}
    >
      <div className='flex items-center'>
        <Image
          src='/isislab.png'
          alt='ISISLab Logo'
          width={36}
          height={12}
          priority
        />
        <Title className='ml-2 mt-3 inline' level={3}>
          3Dify
        </Title>
      </div>
      <div className='flex items-center'>
        <Button type='primary' size='large' block ghost>
          Logout
        </Button>
      </div>
    </Header>
  );
};

export default Navbar;
