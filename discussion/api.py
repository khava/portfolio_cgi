import requests
from os import path, environ
import sys

abs_path = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))), 'portfolio_cgi')
sys.path.append(abs_path)

environ['DJANGO_SETTINGS_MODULE'] = 'portfolio_cgi.settings'
import django
django.setup()

from discussion.models import Theme
from accounts.models import User

def authentication():

    token = None
    url = 'http://130.193.59.48:9000/auth/token/'

    data = {
        'username': 'superadmin',
        'password': 'root'
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json()['access']

    return token


def get_projects():

    projects = []
    url = 'http://130.193.59.48:9000/api/projects/'

    token = authentication()

    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        projects = response.json()

    return projects


def add_new_projects():

    projects = get_projects()

    for project in projects:
        if not Theme.objects.filter(theme=project['name']).exists():
            Theme.objects.create(
                theme=project['name'],
                problem=project['description'],
                decision=project['description'],
                author=User.objects.get(username='admin')
            )


def main():
    add_new_projects()


if __name__ == '__main__':
    main()   