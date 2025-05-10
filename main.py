from fastapi import FastAPI

from config import engine

import app.models.users as user_table
import app.routes.users as user_routes
import app.routes.posts as post_routes


user_table.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user_routes.router)
app.include_router(post_routes.router)
