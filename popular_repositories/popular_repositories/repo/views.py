import requests
from .constants import *
from ..settings import GITHUB_TOKEN
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def is_ok(request):
    return HttpResponse('OK')


@swagger_auto_schema(method='post',
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'repository': openapi.Schema(type=openapi.TYPE_STRING,
                                                          description='Repository route. Format: {user}/{repo_name}'),
                         },
                         required=['repository'],
                     ),
                     responses={status.HTTP_200_OK: openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'num_stars': openapi.Schema(type=openapi.TYPE_NUMBER, description='Number of stars'),
                             'num_forks': openapi.Schema(type=openapi.TYPE_NUMBER, description='Number of forks'),
                             'score': openapi.Schema(type=openapi.TYPE_NUMBER, description='Repository score'),
                             'result': openapi.Schema(type=openapi.TYPE_STRING, description='Popular / Not so popular'),
                         },
                     ), status.HTTP_400_BAD_REQUEST: openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'message': openapi.Schema(type=openapi.TYPE_NUMBER, description='Error message'),
                         },
                     )}
)
@api_view(['POST'])
def calculate_popularity(request):
    """Calculate repository popularity"""
    if request.method == 'POST':
        repository, error_message = get_parameters(request)

        if error_message == '':
            headers = {'Authorization': 'token {}'.format(GITHUB_TOKEN)}
            response = requests.get(GITHUB_API_URL.format(repository), headers=headers)

            if response.status_code == 200:
                returned_data = compute_popularity(response)
                return Response(returned_data)
            else:
                error_message = ERROR_MESSAGE

        return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)


def get_parameters(request):
    repository = request.data.get('repository', '')
    error_message = ''

    if repository == '':
        error_message = ENTER_REPOSITORY_MESSAGE

    return repository, error_message


def compute_popularity(response):
    response_data = response.json()
    num_stars = response_data.get('stargazers_count', NOT_PROVIDED)
    num_forks = response_data.get('forks_count', NOT_PROVIDED)
    score = calculate_score(num_forks, num_stars)
    result = calculate_result(score)

    return {'num_stars': num_stars, 'num_forks': num_forks, 'score': score, 'result': result}


def calculate_score(num_forks, num_stars):
    return num_stars * 1 + num_forks * 2 \
        if num_stars != NOT_PROVIDED and num_forks != NOT_PROVIDED \
        else NOT_PROVIDED


def calculate_result(score):
    return POPULAR_REPO_MESSAGE \
        if score != NOT_PROVIDED and score >= 500 else NOT_POPULAR_MESSAGE
