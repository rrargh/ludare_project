# Simple TODOs API

## About
This is a simple API for creating, viewing, updating and deleting to-do tasks, with the design based on:
https://github.com/kasulani/drf_tutorial

## Tech Stack
* Python
* Django
* Django REST Framework
* SQLite

## Requirements
* Python 3.6
* Django 2.1

## Installation guide
This guide assumes you are using Ubuntu 18.04.  Install basic requirements such as Python 3, Git and Vim
```
sudo apt install git vim python3 python3-distutils
```

Install Pip for Python 3 by first getting then running get-pip.py:
```
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
```

Install Pipenv using Pip for Python 3
```
sudo pip install pipenv
git clone https://github.com/rrargh/ludare_project.git
```

Go to project root and use Pipenv to install the other dependencies, including Django 2.1:
```
cd ludare_project
pipenv install --three
```

Start a shell activating the virtual environment by running:
```
pipenv shell
```

## Testing the app
Run the test script by going to the ludare_project/ludare_project folder and typing:
```python
python manage.py test
```

## Running the app
Run the app by going to the ludare_project/ludare_project folder and typing:
```python
python manage.py runserver
```

On your web browser, verify that the app is running by going to:
http://127.0.0.1:8000/api/v1/todos/

On your web browser, access the app admin interface by going to:
http://127.0.0.1:8000/admin/

## Running the app in Docker

Install Docker CE for Ubuntu
https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository

Add your current user account to the docker group, then restart Ubuntu
```
sudo usermod -aG docker $(whoami)
```
Navigate to the project root directory, and build the requirements file from the Pip environment
```
pip freeze > requirements.txt
```

Navigate to the project root directory, and write the **Dockerfile** with parameters pertaining to the app details
```
FROM django:python3-onbuild
ADD . ~/ludare_project/ludare_project/ludare_app
WORKDIR ~/ludare_project/ludare_project/ludare_app
EXPOSE 8000
RUN pip install --upgrade pip && pip install -r requirements.txt
ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
```

Build the Docker image
```
docker build -t ludare-project
```

Verify if Docker image was built successfully
```
docker images
```

Run the Docker container using the image built from the Dockerfile
```
docker run -it --rm ludare-project
```

Verify that the container is running, and note the *container ID*
```
docker ps -a
```

To navigate to the web site of the container, first get the IP address of the container from the results of running:
```
docker inspect [container ID]
```

Once you get the IP address, be sure to include it in *settings.py* of the Django app, specifically in *ALLOWED_HOSTS*
```python
ALLOWED_HOSTS = ["172.17.0.2"]
```

If you update *settings.py*, build the Docker image again before running a new container for it

Finally, navigate to the web site of the container, use the container's IP address
http://[container_IP_address]:8000/api/v1/todos/
