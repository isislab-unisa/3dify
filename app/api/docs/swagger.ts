import { createSwaggerSpec } from 'next-swagger-doc';

const apiVersion = '1.0.0';

// Define your Swagger specification
const spec = {
  openapi: '3.0.0',
  info: {
    title: '3Dify Next.js API Documentation',
    version: apiVersion,
    description: 'Documentation for the Next.js API endpoints',
    license: {
      name: 'MIT',
      url: 'https://spdx.org/licenses/MIT.html',
    },
  },
  servers: [
    {
      url: process.env.SWAGGER_HOST as string,
      description: 'Development server',
    },
  ],
  // Base configuration for all API paths
  tags: [
    {
      name: 'Face Analysis',
      description: 'Face Analysis operations',
    },
    // Add more tags as needed
  ],
};

export const getApiDocs = () => {
  return createSwaggerSpec({
    definition: spec,
    apiFolder: '/app/api', // Path to your API routes
  });
};