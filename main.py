from fastapi import FastAPI
from redis import Redis
from routers import test

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.redis = Redis(host='127.0.0.1', port=6379, decode_responses=True)


@app.on_event("shutdown")
async def shutdown():
    app.state.redis.close()

app.include_router(test.router, prefix='/test', tags=['Test'])