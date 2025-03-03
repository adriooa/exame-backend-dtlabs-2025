from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.routes import sensor_data_controller
from app.core.config import configs
from app.core.container import Container
from app.core.database.db import Base, engine


Base.metadata.create_all(bind=engine)

def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(
        title=configs.PROJECT_NAME,
        openapi_url="/openapi.json",
        version="0.0.1",
    )

    if hasattr(configs, 'BACKEND_CORS_ORIGINS') and configs.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin)
                           for origin in configs.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.get("/")
    def root():
        return "Service is working"

    app.include_router(sensor_data_controller.router)

    app.container = container
    return app


app = create_app()
