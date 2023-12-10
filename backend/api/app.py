from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from .auth.routes import router as auth_router
from .chat.routes import router as chat_router
from .documents.router import router as doc_router
from .database import init_models
from .web_endpoints import router as web_router
from .email.routers import router as email_router
from .profile.router import router as profile_router


import os
import sys

abspath = os.path.abspath(__file__)
sys.path.append(abspath[:abspath.find('backend')-1])
from telegram.main import send_hi_message, start_bot


def create_app() -> FastAPI:
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(init_models())
    # asyncio.run(init_models())
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)

    _app = FastAPI()
    _app.mount('/static', StaticFiles(directory='frontend/static'), name='static')

    _app.include_router(web_router)
    _app.include_router(chat_router)
    _app.include_router(auth_router)
    _app.include_router(doc_router)
    _app.include_router(email_router)
    _app.include_router(profile_router)

    return _app


app = create_app()


@app.on_event("startup")
async def on_startup():
    # await init_models()
    start_bot()
    pass

