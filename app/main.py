from __future__ import annotations
from typing import Any, Callable
from fastapi import FastAPI, Response 
from fastapi.responses import RedirectResponse
from urllib.request import urlopen, Request
import os # access API_KEY environment variable
import json # parse the json response
import logging
from .utils import generate_url_with_params, get_topic_slugs, img_response

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

RANDOM_IMAGE_URL: str = "https://api.unsplash.com/photos/random"
API_KEY = os.environ["API_KEY"]

TOPICS: dict[str, str] = {
    "nature": "6sMVjTLSkeQ",
    "wallpapers": "bo8jQKTaE0Y",
    "street-photography": "xHxYTMHLgOc",
    "experimental": "qPYsDzvJOYc",
    "3d-renders": "CDwuwXJAbEw",
}

app = FastAPI()

@app.get("/phone")
async def phone():

    req_url: str = await generate_url_with_params(RANDOM_IMAGE_URL, {
        "orientation": "portrait",
        "topics": TOPICS['nature'],
    })

    # add the auth token to the request
    auth_req = Request(req_url)
    auth_req.add_header("Authorization", f"Client-ID {API_KEY}")

    with urlopen(auth_req) as req:
        res: str = req.read()
        
        # parse json output and extract raw image url
        parsed = json.loads(res)
        img_raw_url = parsed["urls"]["raw"]

        return await img_response(img_raw_url)

# define this first to prevent '/{topic}' catching 'phone'
@app.get("/phone/{topic_names}")
async def phone_with_topics(topic_names):

    # generate topics query params or default to 'nature'
    if (topic_slugs := await get_topic_slugs(topic_names, TOPICS)) == None:
        return Response(f"Error: Invalid topic names.\n\nHey dumb dumb, valid topic names are: {', '.join(TOPICS.keys())}.\nYou may delimit topic names via a \"+\" or \"|\" symbol.\nAdditionally, you may leave the topics blank to default to a the \"nature\" topic.")

    req_url: str = await generate_url_with_params(RANDOM_IMAGE_URL, {
        "orientation": "portrait",
        "topics": topic_slugs,
    })

    # add the auth token to the request
    auth_req = Request(req_url)
    auth_req.add_header("Authorization", f"Client-ID {API_KEY}")

    with urlopen(auth_req) as req:
        res: str = req.read()
        
        # parse json output and extract raw image url
        parsed = json.loads(res)
        img_raw_url = parsed["urls"]["raw"]

        return await img_response(img_raw_url)

@app.get("/")
async def root():

    req_url: str = await generate_url_with_params(RANDOM_IMAGE_URL, {
        "orientation": "landscape",
        "topics": TOPICS['nature'],
    })

    # add the auth token to the request 
    auth_req = Request(req_url)
    auth_req.add_header("Authorization", f"Client-ID {API_KEY}")

    with urlopen(auth_req) as res:
        parsed = json.loads(res.read())
        img_raw_url = parsed["urls"]["raw"]

        return await img_response(img_raw_url)

@app.get("/{topic_names}")
async def root_with_topics(topic_names: str):

    # generate topics query params or default to 'nature'
    if (topic_slugs := await get_topic_slugs(topic_names, TOPICS)) == None:
        return Response(f"Error: Invalid topic names.\n\nHey dumb dumb, valid topic names are: {', '.join(TOPICS.keys())}.\nYou may delimit topic names via a \"+\" or \"|\" symbol.\nAdditionally, you may leave the topics blank to default to a the \"nature\" topic.")

    req_url: str = await generate_url_with_params(RANDOM_IMAGE_URL, {
        "orientation": "landscape",
        "topics": topic_slugs,
    })

    # add the auth token to the request 
    auth_req = Request(req_url)
    auth_req.add_header("Authorization", f"Client-ID {API_KEY}")

    with urlopen(auth_req) as req:
        res: str = req.read()

        # parse json output and extract raw image url
        parsed = json.loads(res)
        img_raw_url = parsed["urls"]["raw"]

        return await img_response(img_raw_url)
