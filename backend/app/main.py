from fastapi import FastAPI

app = FastAPI(
    title="AI-First CRM API",
    description="Backend API for the HCP Interaction CRM module",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {
        "message": "AI-First CRM API is running",
        "status": "healthy",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI-First CRM Backend",
    }