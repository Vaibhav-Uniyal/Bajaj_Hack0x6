from fastapi import FastAPI

# Create FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World", "status": "deployed"}

@app.get("/api/v1/health")
async def health():
    return {"status": "ok", "message": "API is working"}

# Export for Vercel
handler = app
