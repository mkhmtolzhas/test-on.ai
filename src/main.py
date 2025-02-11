from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.global_router import router

class AppCreator:
    def __init__(self, allow_origins: list[str] = ["*"]):
        self.app = FastAPI(
            title="Test task",
            description="Test task",
            version="0.1.0",
        )
        self.setup_middlewares(allow_origins)

        self.app.include_router(router)


    def setup_middlewares(self, allow_origins: list[str]):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    

    def get_app(self) -> FastAPI:
        return self.app
    

app_creator = AppCreator()
app = app_creator.get_app()


@router.get("/ping")
async def ping():
    return {"ping": "pong"}
