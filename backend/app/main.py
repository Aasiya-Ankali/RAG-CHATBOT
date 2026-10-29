from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.powerplant_routes import router as powerplant_dashboard
from app.routes.chat_routes import router as chat_router

app = FastAPI(
    title="RAG Project",
    description="Chat with power plant information",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_fun():
    return "Hello !!! Server is running ."


# app.include_router(router, prefix="/api")
app.include_router(powerplant_dashboard)
app.include_router(chat_router, prefix="/api")
