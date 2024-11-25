from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config.database import create_db_and_tables  # , delete_db_and_tables
from config.env import FRONTEND_SETTINGS
from routers import token, user

@asynccontextmanager
async def lifespan(app: FastAPI):
    # delete_db_and_tables()
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user.router)
app.include_router(token.router)


origins = [FRONTEND_SETTINGS.FRONTEND_URL]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
