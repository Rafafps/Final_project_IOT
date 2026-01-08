"""
Entry point kept for backward compatibility.
The real FastAPI application lives in `api_server.py`.
"""
from .api_server import app  # noqa: F401

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("manager.api_server:app", host="0.0.0.0", port=7070, reload=True)