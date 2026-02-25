import logging
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Middleware configuration for CORS
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.get("/")
def read_root():
    logger.info("Root endpoint called")
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    logger.info(f"Fetching item with id: {item_id}")
    if item_id < 0:
        logger.error("Item ID must be a positive integer")
        raise HTTPException(status_code=400, detail="Item ID must be a positive integer")
    return {"item_id": item_id}