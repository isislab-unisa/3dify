import { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Layout } from 'antd';
import { Content } from 'antd/es/layout/layout';
import Title from 'antd/es/typography/Title';
import { getServerSession } from 'next-auth';

import Sidebar from '@/app/components/sidebar';
import Navbar from '@/app/components/navbar';
import SessionProvider from '@/app/components/provider';
import GoogleSignInButton from '@/app/components/google_signin_button';

import { authOptions } from './api/auth/[...nextauth]/authOptions';

import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: '3Dify',
  description: 'Cloud-native 3Dify',
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const session = await getServerSession(authOptions);
  if (!session || !session.user) {
    return (
      <html lang='en'>
        <body className={inter.className}>
          <SessionProvider session={session}>
            <Navbar />

            <Layout className='bg-white border-none'>
              <Content className='mt-[10%] flex justify-center items-center'>
                <div className='flex-col border-gray-400 p-16 rounded-xl shadow-2xl'>
                  <div className='flex justify-center'>
                    <Title className='block' level={1}>
                      {'Welcome to 3Dify!'}
                    </Title>
                  </div>
                  <div className='flex justify-center'>
                    <Title className='block' level={4}>
                      {'Login to start creating your own Avatars!'}
                    </Title>
                  </div>
                  <div className='flex justify-center mt-8'>
                    <GoogleSignInButton />
                  </div>
                </div>
              </Content>
            </Layout>
          </SessionProvider>
        </body>
      </html>
    );
  }

  return (
    <html lang='en'>
      <body className={inter.className}>
        <SessionProvider session={session}>
          <Navbar />

          <Layout>
            {session && session?.user && <Sidebar />}

            <Layout className='w-full bg-white'>
              <Content className='mb-1'>
                <div className='min-h-screen items-center justify-between p-8'>
                  {children}
                </div>
              </Content>

              {/* <Footer className='bg-white'>
                <div className='flex items-center justify-center'>
                  <span>3Dify ©{new Date().getFullYear()} Created by </span>
                  <Image
                    src='/isislab.png'
                    alt='ISISLab Logo'
                    width={30}
                    height={10}
                    priority
                    className='ml-2'
                  />
                </div>
              </Footer> */}
            </Layout>
          </Layout>
        </SessionProvider>
      </body>
    </html>
  );
}
