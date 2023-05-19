#!/bin/bash

# get directory of script
DIR="$(cd "$(dirname "$0")" && pwd)"

docker container stop wallpaper && docker container rm wallpaper
echo hey

docker build -t wallpaper-nickramsay-dev $DIR
