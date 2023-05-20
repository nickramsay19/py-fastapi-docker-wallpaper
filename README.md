# py-fastapi-wallpaper

A simple [Unsplash API](https://unsplash.com/documentation) wrapper in FastAPI that fetches an image URL and redirects to a random nature wallpaper. This is to be used by my mobile devices to grab new wallpapers via scripts. The application runs in a Docker container so it will be compatible with my Nginx setup at [nickramsay.dev](https://nickramsay.dev). 

To run, simply choose the port you wish to expose it on in `start.sh`, and then run:
```sh
sh build.sh && sh start.sh
```
