from fastapi import FastAPI
from src.authentication.routes import router as auth_routes
from src.community.routes import router as community_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Community Platform",
    description="New platform for users to create communities for anything",
    version="1.0.0"
)

app.include_router(auth_routes)
app.include_router(community_routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home_root():
    return { "message": "Hello there beta" }