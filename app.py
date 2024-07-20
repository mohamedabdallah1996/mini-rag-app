from fastapi import FastAPI 
from routes import base_routes, data_routes

app = FastAPI()

app.include_router(base_routes.base_router)
app.include_router(data_routes.data_router)