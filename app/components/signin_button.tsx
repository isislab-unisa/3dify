'use client'

import { Button } from 'antd';
import { signIn } from 'next-auth/react';

export default function SignInButton() {
  return (
    <Button
      type='primary'
      size='large'
      block
      ghost
      className='mt-3'
      onClick={() => signIn('google')}
    >
      Login with Google
    </Button>
  );
}