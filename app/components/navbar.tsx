'use client';

import { FC } from 'react';
import Image from 'next/image';
import { Header } from 'antd/es/layout/layout';
import Title from 'antd/es/typography/Title';
// import SignInButton from './signin_button';
import SignOutButton from './signout_button';
import { useSession } from 'next-auth/react';

const Navbar: FC = () => {
  const { data: session, status, update } = useSession();
  console.log('session', {session});

  const storeUser = async () => {
    if (!session || !session.user) {
      console.log('No session or user.');
      return;
    }

    try {
      const response: Response = await fetch(process.env.NEXT_PUBLIC_STORE_USER as string, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: session.user?.name,
          email: session.user?.email,
          imageIds: [],
        }),
      });

      await response.json();
    } catch (error: any) {
      console.error('Error storing user.', error);
    }
  };

  storeUser();

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
      <div className='flex'>
        {session ?
            <div className='flex'>
              {/* <Image
                src={session.user?.image ?? ''}
                alt='ISISLab Logo'
                width={36}
                height={12}
                priority
              /> */}
              <div className='text-nowrap mr-5'>{session.user?.name}</div>
              <SignOutButton/>
            </div>
            :
            <>
              {/* <SignInButton/> */}
            </>}

      </div>
    </Header>
  );
};

export default Navbar;
