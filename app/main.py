from fastapi import FastAPI
from fastapi.responses import Response
from dotenv import load_dotenv

from app.api.v1.routes import statements, quotes

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# routers
app.include_router(statements.router, prefix="/api/v1/statements")
app.include_router(quotes.router, prefix="/api/v1/quotes")

@app.get("favicon.ico") # Just to remove the error log.
async def favicon():
    return Response(status_code=204) # No Content