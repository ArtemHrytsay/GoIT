import redis.asyncio as redis
import time

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.routes import contacts, auth, users

app = FastAPI()


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:8000', 'http://localhost:8000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware('http')
async def custom_middleware(request: Request, call_next):
    start_time = time.time()
    response   = await call_next(request)
    during     = time.time() - start_time
    response.headers['performance'] = str(during)
    return response


@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def root():
    return {"message": "Welcome to RESTapi"}


@app.get("/api/hw-13")
def api_hw12(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Configuration error")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Connection error")


app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
