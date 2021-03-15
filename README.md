# Popular repositories

## Service description:
Service in charge of checking whether the provided GitHub repository is popular
or not. Here, popular GitHub repository means one for which `score >= 500` where:

- `score = num_stars * 1 + num_forks * 2.`


## Tech stack used:
- Python 3.7
- Django 3.1.7
- Django REST framework 3.12.2
- drf-yasg 1.20.0 - Swagger generator


## Instructions:

## Github API Token
Edit `settings.py` file located at:
- `popular_repositories\popular_repositories\repo\settings.py`

Update `GITHUB_TOKEN` variable with your own
- `GITHUB_TOKEN = '{Github API Token}'`

## Docker
First you need to build the image:
- `docker build -t popular_repositories .`

Then you can run the container for the service:
- `docker run --name popular_repositories_container -t -p 7000:7000 popular_repositories`

## Unit tests
In order to run unit tests you need to enter container:
- `docker exec -it popular_repositories_container /bin/bash`

Then in container you can run tests:
- `python manage.py test`

## Health Check
In order to check health for service you have to open a browser and go to:
- `http://127.0.0.1:7000/health`

## Running Service
In order to run the service you have to open a browser and go to:
- `http://127.0.0.1:7000/swagger`

There you will see all methods available

## Things to improve
- How Github API Token is passed to the service