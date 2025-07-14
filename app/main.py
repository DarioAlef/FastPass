from fastapi import FastAPI
from app.routes.home import router as home_router
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(tittle="FastPass")

app.mount("/static", StaticFiles(directory="app/static"), name="static2")

app.include_router(home_router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

