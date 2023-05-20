from __future__ import annotations
from typing import Any, Callable
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from urllib.request import urlopen, Request
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl
import os # access API_KEY environment variable
import json # parse the json response
import re # for splitting path names by multiple delimiters
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def generate_url_with_params(base_url: str, params: dict[str, str]) -> str:
    """generates a raw parameterised url from a param dict"""

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
    "street-photography": "xHxYTMHLgOc",
    "experimental": "qPYsDzvJOYc",
    "3d-renders": "CDwuwXJAbEw",
}

async def get_topic_slugs_or(path: str, topics: dict[str, str], default: str) -> str:
    """translates our custom user friendly path notation 'topic1+topic2' or 'topic1|topic2' notation to Unsplash's slug query parameter notation '62MVjTLSkeQ,bo8jQKTaE0Y'."""
    
    if path == '' or path == None:
        return default

    topic_names: list[str] = re.split(r'\||\+', path)
    
    # attempt to build list of slugs
    slugs: list[str] = []
    for t in topic_names:
        if t in topics.keys():
            slugs.append(topics[t])
        else:
            return None

    # generate unsplash comma delimited query param notation
    joined = ','.join(slugs)
    return joined

app = FastAPI()

# define this first to prevent '/{topic}' catching 'phone'
@app.get("/phone/{topic_names}")
async def phone(topic_names: str = ''):
    
    # generate topics query params or default to 'nature'
    if (topic_slugs := await get_topic_slugs_or(topic_names, TOPICS, TOPICS['nature'])) == None:
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

        return RedirectResponse(url=img_raw_url)

@app.get("/")
async def root():

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

        return RedirectResponse(url=img_raw_url)

@app.get("/{topic_names}")
async def root_with_topics(topic_names: str):

    # generate topics query params or default to 'nature'
    if (topic_slugs := await get_topic_slugs_or(topic_names, TOPICS, TOPICS['nature'])) == None:
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

        return RedirectResponse(url=img_raw_url)


