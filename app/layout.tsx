import { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Layout } from 'antd';
import { Content } from 'antd/es/layout/layout';

import Sidebar from '@/app/components/sidebar';
import Navbar from '@/app/components/navbar';

import './globals.css';

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
        <Navbar />

        <Layout>
          <Sidebar />

          <Layout className='w-full'>
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
      </body>
    </html>
  );
}
