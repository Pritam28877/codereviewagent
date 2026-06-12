from fastapi import FastAPI

from src.config.settings import get_settings
from src.routes.review.router import router as review_router
from src.routes.health.router import router as health_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    app.include_router(health_router, prefix="/v1/health", tags=["health"])
    app.include_router(review_router, prefix="/v1/reviews", tags=["reviews"])

    return app


app = create_app()
