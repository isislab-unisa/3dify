import { Metadata } from 'next';
import Image from 'next/image';
import { Inter } from 'next/font/google';
import { Button, Layout } from 'antd';
import { Content, Header } from 'antd/es/layout/layout';

import Sidebar from '@/components/sidebar';

import './globals.css';
import Title from 'antd/es/typography/Title';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: '3Dify',
  description: 'Cloud-native 3Dify',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang='en'>
      <body className={inter.className}>
        <Layout>
          <Sidebar />

          <Layout className='w-full'>
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

            <Content className='mb-1'>
              <div
                style={{
                  padding: 8,
                  minHeight: 360,
                  background: 'white',
                }}
              >
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
      </body>
    </html>
  );
}
