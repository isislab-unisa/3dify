'use client';

import { FC, useState } from 'react';

import UploadArea from '@/app/components/upload_area';
import Gallery from '@/app/components/gallery';

const Home: FC = () => {
  const [refresh, setRefresh] = useState<boolean>(false);
  return (
    <div className='m-auto ml-8'>
      <UploadArea setRefresh={setRefresh} />
      <Gallery refresh={refresh} />
    </div>
  );
};

export default Home;
