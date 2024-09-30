'use client'

import { Button } from 'antd';
import { signOut } from 'next-auth/react';

export default function SignOutButton() {
  console.log('signout button');
  return (
    <Button
      type='primary'
      size='large'
      block
      ghost
      className='mt-3'
      onClick={() => signOut()}
    >
      Logout
    </Button>
  );
}