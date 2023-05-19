#!/bin/bash

PORT=8002
docker run -d -p $PORT:80 --name wallpaper wallpaper-nickramsay-dev
