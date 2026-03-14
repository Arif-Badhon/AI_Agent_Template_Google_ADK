from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.backend.core.config import settings
from src.backend.api.v1.router import api_router
from src.backend.core.security import get_api_key
import uuid
from fastapi import Request
from loguru import logger
import time

def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
    )

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(api_router, prefix=settings.API_V1_STR, dependencies=[Depends(get_api_key)])

    return app

app = get_application()

@app.middleware("http")
async def add_process_time_and_trace(request: Request, call_next):
    trace_id = str(uuid.uuid4())
    # Add trace_id to logger context
    with logger.contextualize(trace_id=trace_id):
        start_time = time.time()
        
        logger.info(f"Incoming request: {request.method} {request.url.path}")
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Trace-ID"] = trace_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"
        
        logger.info(f"Completed request in {process_time:.4f}s")
        return response

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME}