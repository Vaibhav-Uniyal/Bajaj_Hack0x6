# 🚀 Vercel Deployment Guide

## Overview
This guide will help you deploy your LLM-Powered Intelligent Query–Retrieval System to Vercel for production use.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Environment Variables**: Set up your API keys

## 🔧 Setup Steps

### 1. Environment Variables
Set these environment variables in your Vercel project:

```bash
# Authentication
AUTH_TOKEN=db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6

# Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Pinecone Configuration (Optional)
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=your_index_name
```

### 2. Deploy to Vercel

#### Option A: Using Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

#### Option B: Using Vercel Dashboard
1. Connect your GitHub repository to Vercel
2. Import the project
3. Set environment variables
4. Deploy

### 3. Configuration Files

The following files are already configured for Vercel:

- `vercel.json`: Vercel configuration
- `api/index.py`: Serverless function entry point
- `requirements-vercel.txt`: Optimized dependencies
- `src/api_serverless.py`: Serverless-optimized API

## 🌐 API Endpoints

Once deployed, your API will be available at:

```
https://your-project-name.vercel.app/api/v1/hackrx/run
https://your-project-name.vercel.app/api/v1/hackrx/run/detailed
https://your-project-name.vercel.app/api/v1/health
```

## 📝 Usage Examples

### Basic Query
```bash
curl -X POST "https://your-project-name.vercel.app/api/v1/hackrx/run" \
  -H "Authorization: Bearer db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": ["https://example.com/policy.pdf"],
    "questions": ["What is the grace period for premium payment?"]
  }'
```

### Detailed Query
```bash
curl -X POST "https://your-project-name.vercel.app/api/v1/hackrx/run/detailed" \
  -H "Authorization: Bearer db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": ["https://example.com/policy.pdf"],
    "questions": ["What is the grace period for premium payment?"]
  }'
```

## 🔍 Testing Your Deployment

Use the provided test script:

```bash
python test_vercel_deployment.py
```

## ⚠️ Important Notes

### Cold Starts
- The first request may take longer due to cold starts
- Subsequent requests will be faster
- Consider using Vercel Pro for better performance

### Memory Limits
- Vercel has memory limits for serverless functions
- Large documents may require optimization
- Consider chunking very large documents

### Timeout Limits
- Vercel has a 60-second timeout limit
- Complex queries may need optimization
- Consider breaking large requests into smaller ones

### Environment Variables
- Make sure all required environment variables are set
- Double-check API keys are correct
- Test with a simple request first

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are in `requirements-vercel.txt`
2. **Timeout Errors**: Optimize your queries or break them into smaller chunks
3. **Memory Errors**: Consider using smaller chunk sizes or optimizing the model
4. **Authentication Errors**: Verify your AUTH_TOKEN is set correctly

### Debugging

1. Check Vercel logs in the dashboard
2. Test locally first with `python src/api_serverless.py`
3. Use the health endpoint to verify system status

## 📊 Monitoring

Monitor your deployment using:
- Vercel Analytics
- Function logs in Vercel dashboard
- Custom logging in your application

## 🔄 Updates

To update your deployment:
1. Push changes to your GitHub repository
2. Vercel will automatically redeploy
3. Or manually trigger a deployment from the dashboard

## 🎉 Success!

Once deployed, your API will be publicly accessible and ready to handle real-world queries!
