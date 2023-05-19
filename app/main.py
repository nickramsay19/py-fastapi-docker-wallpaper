from __future__ import annotations
from typing import Any, Callable, Maybe
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "wallpaper fastapi server" 
