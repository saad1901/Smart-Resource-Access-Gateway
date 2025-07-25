from fastapi import FastAPI
from redis import Redis
from routers import test, events, hotels, jwtSec
from models.Hmodels import Base2
from models.Emodels import Base
from config.dependencies import engine2, engine

app = FastAPI()

# Base.metadata.create_all(bind=engine)
# Base2.metadata.create_all(bind=engine2)

@app.on_event("startup")
async def startup():
    app.state.redis = Redis(host='127.0.0.1', port=6379, decode_responses=True)


@app.on_event("shutdown")
async def shutdown():
    app.state.redis.close()

app.include_router(test.router, prefix='/test', tags=['Test'])
app.include_router(events.router, prefix='/events', tags=['Event'])
app.include_router(hotels.router, prefix='/hotel', tags=['Hotel'])
app.include_router(jwtSec.router, prefix='/security', tags=['Security'])