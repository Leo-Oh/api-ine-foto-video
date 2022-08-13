from fastapi import FastAPI
from routes.routesFiles import router
app = FastAPI()

app.include_router(router)