from __future__ import annotations
from typing import Any, Callable
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from urllib.request import urlopen
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

# generate url
URL: str = "https://api.unsplash.com/photos/random"
PARAMS: dict[str, str] = {
    "topics": "bo8jQKTaE0Y",
    "orientation": "landscape",
    "client_id": os.environ["API_KEY"]
}

req_url: str = generate_url_with_params(URL, PARAMS)

app = FastAPI()

@app.get("/")
def root():
    with urlopen(req_url) as req:
        res: str = req.read()
        parsed = json.loads(res)
        img_raw_url = parsed["urls"]["raw"]
        return RedirectResponse(url=img_raw_url)
