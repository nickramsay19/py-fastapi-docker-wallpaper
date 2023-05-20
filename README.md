# py-fastapi-docker-wallpaper

A simple [Unsplash API](https://unsplash.com/documentation) wrapper in FastAPI that fetches an image URL and redirects to a random nature wallpaper. This is to be used by my mobile devices to grab new wallpapers via scripts. The application runs in a Docker container so it will be compatible with my Nginx setup at [nickramsay.dev](https://nickramsay.dev). 

## Usage
1. Ensure you have [Docker](https://docs.docker.com/get-docker/) installed. Or, if it applies, run `sudo sh setup-debian-bullseye.sh`.
2. Specify the port you wish to expose the container on `start.sh`.
3. Simply run:
```sh
sh build.sh && sh start.sh
# or,
sudo chmod +x build.sh start.sh
sudo ./build.sh && sudo ./start.sh
```
