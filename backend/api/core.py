from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..db import models
from ..db.database import SessionLocal, engine

from ..routes import auth, users, projects, sentences, translations


# Lifespan to manage app events at app start and stop
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    yield

    # Close connection to database
    SessionLocal.close_all()


# Create FastAPI app
app = FastAPI(lifespan=lifespan)

# Add routes
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(sentences.router)
app.include_router(translations.router)
