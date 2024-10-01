'use client'

import { signIn } from 'next-auth/react';
import GoogleButton from 'react-google-button';

type Props = {
  className?: string;
};

export default function GoogleSignInButton({ className }: Props) {
  return (
    <GoogleButton
      label='Login with Google'
      className={className}
      onClick={() => signIn('google')}
    />
  );
}