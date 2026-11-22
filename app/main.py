from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.config import client, create_indexs
from app.api.routes.health import router as health_router
from app.users.routes import router as auth_router
from app.workspaces.routes import router as workspace_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await client.admin.command("ping")
    await create_indexs()
    print("MongoDB connected successfully!")

    yield

    await client.close()
    print("Mongodb connection close")


app = FastAPI(lifespan=lifespan)


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(workspace_router)
