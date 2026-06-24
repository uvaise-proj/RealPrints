import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import Base, engine
from app.models import user  # noqa: F401 — ensures User table is created by create_all
from app.routers import analytics, auth, process, projects, recommend

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("RealPrints API starting — ensuring database tables exist...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database ready.")
    yield
    logger.info("RealPrints API shutting down.")


app = FastAPI(
    title="RealPrints API",
    description="Textile printing project tracking and machine-settings recommendation system.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(recommend.router)
app.include_router(process.router)
app.include_router(analytics.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s: %s", request.method, request.url, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


@app.get("/health", tags=["Health"], summary="Service health check")
def health_check():
    return {"status": "ok", "version": "1.0.0", "env": settings.APP_ENV}
