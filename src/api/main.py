from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI agent for detecting behavioral trading patterns",
    version="0.1.0",
    debug=settings.debug,
)

# Add CORS middleware (allow frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.environment}

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Trade Behavioral Agent API",
        "docs": "/docs",
        "version": "0.1.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
