from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def enable_cors(app: FastAPI):
    """
    Enables CORS for all origins (*), all headers, and all methods.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=False,
    )
    return app