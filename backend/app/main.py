from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import simulation

app = FastAPI(title="Sworm System API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulation.router, prefix="/api/simulation", tags=["simulation"])

@app.get("/")
async def root():
    return {"message": "Sworm System Backend is Running"}
