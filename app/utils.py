from __future__ import annotations
from typing import Any, Callable
from fastapi import Response
from fastapi.responses import StreamingResponse
from urllib.request import urlopen, Request
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl
import re # for splitting path names by multiple delimiters
import io # for io.BytesIO

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

async def get_topic_slugs(path: str, topics: dict[str, str]) -> str:
    """translates our custom user friendly path notation 'topic1+topic2' or 'topic1|topic2' notation to Unsplash's slug query parameter notation '62MVjTLSkeQ,bo8jQKTaE0Y'."""

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

async def img_response(img_url: str) -> StreamingResponse | Response:

    res = urlopen(img_url) 

    if res.getcode() == 200:
        # create byte iterator
        img_bytes = io.BytesIO(res.read())
        img_bytes.seek(0)
        img_bytes_iter = iter(img_bytes.read, b"")

        return StreamingResponse(img_bytes_iter, media_type="image/jpeg")            
    else:
        return Response(f"Error: In retrieving image from \"{img_url}\", got error code: {img_res.getcode()}.")

