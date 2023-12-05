from fastapi import FastAPI
from .auth.routes import router as auth_router
from backend.api.database import init_models
from .chat.routes import router as chat_router
from .documents.router import router as doc_router


def create_app() -> FastAPI:
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
    await init_models()
