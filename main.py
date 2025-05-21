from fastapi import FastAPI, APIRouter

import app.routes.users as user_routes
import app.routes.posts as post_routes
from config import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user_routes.router)
api_router.include_router(post_routes.router)
app.include_router(api_router)
