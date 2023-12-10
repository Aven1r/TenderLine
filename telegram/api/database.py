import asyncio

from sqlalchemy import event, Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs, async_sessionmaker
import typer

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///db.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, class_=AsyncSession, bind=engine,
                                  expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


cli = typer.Typer()


@cli.command()
def init_db():
    asyncio.run(init_models())


if __name__ == '__main__':
    cli()
