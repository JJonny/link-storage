from fastapi import FastAPI
from src.v1.routes import router


app = FastAPI()
app.include_router(router=router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)