from __future__ import annotations
from typing import Any, Callable
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from urllib.request import urlopen, Request
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl
import os # access API_KEY environment variable
import json # parse the json response

def generate_url_with_params(base_url: str, params: dict[str, str]) -> str:

    # parse the base URL
    parsed_url = urlparse(base_url)
    
    # get the existing query parameters (if any)
    existing_params = dict(parse_qsl(parsed_url.query))
    
    # merge the existing and new parameters
    merged_params = {**existing_params, **params}
    
    # encode the parameters
    encoded_params = urlencode(merged_params)
    
    # build the new URL with the encoded parameters
    new_url = urlunparse(parsed_url._replace(query=encoded_params))
    
    return new_url

RANDOM_IMAGE_URL: str = "https://api.unsplash.com/photos/random"
API_KEY = os.environ["API_KEY"]

TOPICS: dict[str, str] = {
    "nature": "62MVjTLSkeQ",
    "wallpapers": "bo8jQKTaE0Y",
    "street-photography": "",
    "experimental": ""
}

app = FastAPI()

@app.get("/")
def root():
    req_url: str = generate_url_with_params(RANDOM_IMAGE_URL, {
        "topics": "bo8jQKTaE0Y",
        "orientation": "landscape",
    })

    auth_req = Request(req_url)
    auth_req.add_header("Authorization", f"Client-ID {API_KEY}")

    with urlopen(auth_req) as req:
        res: str = req.read()

        # parse json output and extract raw image url
        parsed = json.loads(res)
        img_raw_url = parsed["urls"]["raw"]

        return RedirectResponse(url=img_raw_url)

@app.get("/phone")
def root():

    req_url: str = generate_url_with_params(RANDOM_IMAGE_URL, {
        "topics": "bo8jQKTaE0Y",
        "orientation": "portrait",
    })

    auth_req = Request(req_url)
    auth_req.add_header("Authorization", f"Client-ID {API_KEY}")

    with urlopen(auth_req) as req:
        res: str = req.read()
        
        # parse json output and extract raw image url
        parsed = json.loads(res)
        img_raw_url = parsed["urls"]["raw"]

        return RedirectResponse(url=img_raw_url)
