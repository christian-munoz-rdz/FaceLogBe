import os

import uvicorn
from dotenv import load_dotenv

from server import Server


def app():
    """
    This function gets called by main in `uvicorn.run`
    """
    server = Server()
    return server.run()


if __name__ == "__main__":
    load_dotenv("config.env")
    if os.getenv("ENV") == "production":
        print("Production")
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=int(os.getenv("APP_PORT"))
        )
    else:
        print("localhost")
        uvicorn.run(
            "main:app",
            host="localhost",
            port=int(os.getenv("APP_PORT")),
            reload=True
        )
