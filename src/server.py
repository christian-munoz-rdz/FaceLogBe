from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from database.services.database import Database
from routes.area_router import AreaRouter
from routes.face_router import FaceRouter
from routes.user_router import UserRouter


class Server:

    def __init__(self) -> None:
        self.app = FastAPI()
        self.add_middlewares()
        self.add_routes()

        Database.start_database()

    def add_middlewares(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.app.add_exception_handler(HTTPException, self.http_exception_handler)

    @staticmethod
    async def http_exception_handler(request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail, "status_code": exc.status_code}
        )

    def add_routes(self) -> None:
        self.app.include_router(AreaRouter.router)
        self.app.include_router(FaceRouter.router)
        self.app.include_router(UserRouter.router)

    def run(self) -> FastAPI:
        return self.app