from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.exceptions import TripPlannerException
from app.api.v1 import auth, trips, locations

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 异常处理
@app.exception_handler(TripPlannerException)
async def trip_planner_exception_handler(request: Request, exc: TripPlannerException):
    return JSONResponse(
        status_code=400,
        content={
            "code": exc.code,
            "message": exc.message,
            "request_id": getattr(request.state, "request_id", "")
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code * 100,
            "message": exc.detail,
            "request_id": getattr(request.state, "request_id", "")
        }
    )

# 路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(trips.router, prefix="/api/v1/trips", tags=["行程"])
app.include_router(locations.router, prefix="/api/v1/locations", tags=["地点"])

@app.get("/")
async def root():
    return {"message": "Trip Planner API", "version": settings.VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
