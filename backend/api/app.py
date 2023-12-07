from fastapi import FastAPI
from .auth.routes import router as auth_router
from backend.api.database import init_models, Base, engine
from .chat.routes import router as chat_router
from .documents.router import router as doc_router
import asyncio

def create_app() -> FastAPI:
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(init_models())
    # asyncio.run(init_models())
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)

    _app = FastAPI()
    _app.include_router(chat_router)
    _app.include_router(auth_router)
    _app.include_router(doc_router)

    return _app


app = create_app()


@app.on_event("startup")
async def on_startup():
    # await init_models()
    pass