# Improved Error Handling and Logging for Vercel Serverless Function

import { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(req: VercelRequest, res: VercelResponse) {
    try {
        // Simulate logic here
        const data = await someAsyncFunction(req.body);
        res.status(200).json(data);
    } catch (error) {
        console.error('Error occurred:', error); // Improved logging
        res.status(500).json({ message: 'Internal Server Error', error: error.message }); // Enhanced error messaging
    }
}