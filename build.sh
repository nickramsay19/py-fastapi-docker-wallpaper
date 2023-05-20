#!/bin/bash

# get directory of script
DIR="$(cd "$(dirname "$0")" && pwd)"

docker container stop wallpaper && docker container rm wallpaper

# get API_KEY
source $DIR"/.env"

docker build --build-arg API_KEY=$API_KEY -t wallpaper-nickramsay-dev $DIR
