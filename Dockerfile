FROM python:3.11.3-bullseye

WORKDIR /

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./app ./app

# you must load the API_KEY value when building
ARG API_KEY
ENV API_KEY=${API_KEY}

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
