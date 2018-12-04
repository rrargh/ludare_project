# Simple TODOs API

## About
### This is a simple API for creating, viewing, updating and deleting to-do tasks, with the design based on:
https://github.com/kasulani/drf_tutorial

## Tech Stack
* Python
* Django
* Django REST Framework
* SQLite

## Requirements
* Python 3.6
* Django 2.1

## Installation
### Install basic requirements such as Python 3, Git and Vim
`sudo apt install python3 git vim`

### Install Pip for Python 3 by first getting then running get-pip.py:
`wget https://bootstrap.pypa.io/get-pip.py`
`sudo python3 get-pip.py`

### Install Pipenv using Pip for Python 3
`sudo pip install pipenv`
`git clone https://github.com/rrargh/ludare_project.git`

### Go to project root and use Pipenv to install the other dependencies, including Django 2.1:
`cd ludare_project`
`pipenv install --three`

### Start a shell activating the virtual environment by running:
`pipenv shell`

## Testing the app
### Run the test script by going to the ludare_project/ludare_project folder and typing:
`python manage.py test`

## Running the app
### Run the app by going to the ludare_project/ludare_project folder and typing:
`python manage.py runserver 0.0.0.0:8000`

### On your web browser, verify that the app is running by going to:
http://127.0.0.1:8000/api/v1/todos/

### On your web browser, access the app admin interface by going to:
http://127.0.0.1:8000/admin/
