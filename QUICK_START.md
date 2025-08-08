# 🚀 Quick Start: Deploy to Vercel

## ⚡ 5-Minute Deployment

### 1. Install Vercel CLI
```bash
npm i -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy
```bash
vercel --prod
```

### 4. Set Environment Variables
In your Vercel dashboard, add these environment variables:
- `AUTH_TOKEN`: `db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6`
- `GEMINI_API_KEY`: Your Gemini API key

### 5. Test Your API
```bash
python test_vercel_deployment.py
```

## 🌐 Your API URLs

Once deployed, your API will be available at:
- **Health Check**: `https://your-project.vercel.app/api/v1/health`
- **Basic Query**: `https://your-project.vercel.app/api/v1/hackrx/run`
- **Detailed Query**: `https://your-project.vercel.app/api/v1/hackrx/run/detailed`

## 📝 Example Usage

```bash
curl -X POST "https://your-project.vercel.app/api/v1/hackrx/run" \
  -H "Authorization: Bearer db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": ["https://example.com/policy.pdf"],
    "questions": ["What is the grace period for premium payment?"]
  }'
```

## 🎉 Done!

Your LLM-Powered Intelligent Query–Retrieval System is now live and ready to handle requests!
