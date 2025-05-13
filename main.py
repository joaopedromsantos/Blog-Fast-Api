from fastapi import FastAPI

import app.routes.users as user_routes
import app.routes.posts as post_routes
from config import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(post_routes.router)
