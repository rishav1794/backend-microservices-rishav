from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="User Service", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Welcome to the user service!"}

@app.get("/health")
def health_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "service": "user-service"
        }
    )