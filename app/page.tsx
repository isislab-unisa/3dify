'use client';

import { FC } from 'react';

import UploadArea from '@/app/components/upload_area';
import Gallery from '@/app/components/gallery';

const Home: FC = () => {
  return (
    <div className='m-auto ml-8'>
      <UploadArea />
      <Gallery />
    </div>
  );
};

export default Home;
