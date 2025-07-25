from fastapi import APIRouter, Depends
from config.dependencies import get_redis

router = APIRouter()

@router.post('/')
async def test(key: str, value: str, redis = Depends(get_redis)):
    
    try:
        redis.set(key, value)
    except:
        pass

    return 'Done'

@router.get('/')
async def getvalue(key: str,redis = Depends(get_redis)):
    # value = None
    try:
        value = redis.get(key)
    except:
        return "COnnection to redis is GOne"

    return value