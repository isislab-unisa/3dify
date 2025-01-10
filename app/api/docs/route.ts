import { NextResponse } from 'next/server';
import { getApiDocs } from './swagger';

export async function GET() {
  return NextResponse.json(getApiDocs());
}
