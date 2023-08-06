an api that is used for recipe app.

in this Project we are using docker, postgress and django(python web framework) 
# requirements.txt and requirments.dev.txt
->so the main diffrence btn them is we used it for listing all dependancy required for the production enviroment.these are packages needed to run application in stable and reliable manner.

# requirments.dev.txt 
-> we use this for listing the development dependancies like a packages needed for development and testing purpose. eg. flake for linting and testing, debugging

# Docker 
docker is a containerization technology which allows us to package an application with all its dependencies into and also it is an opensource platform that allows developers to automate deployment, scaling, and mangement of applications inside lightweight, portable container. 
# container 
container are self contained units that package all the neccessary software, libraries, and dependancies needed to run an application.
# Docker Compose
-> it is a tool that is provided by a docker that allows to define and manage multi container Docker application. it uses YAML file to configure the services, networks, and volumes required for application enviroment. it can automates the process of starting, stopping, and  connecting multiple container. By writing one single  command you can  bring up an entire application defined in the compose file.
-> in order to use a docker compose we have to create docker-compose.yml file in our project and configure it inside the file.

# 1- create a file named Dockerfile in the root directory of your project with following content:
  

FROM python:3.11-alpine3.17
LABEL maintainer="beba2123"

ENV PYTHONBUFFERED 1  

COPY ./requirements.txt /tmp/requirements.txt   # copy requirements to image
Copy ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false ==>> which means that make development enviroment false 
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirnments.txt && \
    if [$DEV = "true" ], \
        then /py/bin/pip install -r requirments.dev.txt ; \
    fi && \
    rm -rf /tmp \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV  PATH="/py/bin:$PATH"
  
USER django-user


#  2nd step is create a file called docker-compose.yml and inside of it we write 

version: "docker-compose version"

services: 
    app:
        build:
            context: . -> build in side root directory
        ports:
          - "8000:8000" 
        volumes:
          - ./app:/app
        command:  >
        sh -c "python manage,=.py runserver 0.0.0.0:8000"


# 3rd step is linting tool 
-> linting is used for formating your code,  highlighting errors, typos

# How we handle linting
-> install flake8 package
-> Run it through Docker Compose 
command -> docker-compose run --rm app sh -c "flake8"
-> so first we create flake8 file then we write some of file that we are going to exclude from it like 
[flake8]
exclude=
    migrations,
    __pycache__,
    manage.py,
    settings.py



# Testing
-> Django test suite
-> Setup tests per Django app
-> in order to run docker-compose run --rm app sh -c "python manage.py test"


# django project

-> so after setting our docker file we are going to create our project inside our working directory("app")
command ("docker-compose run --rm app sh -c "django-admin startproject app .")  
# NOTE '.' 
-> refers to locate that we are to create our django inside the the working directory.

# Github action

-> They are powerfull automation and CI/CD(continious integration and continious deployment) platform provided by github.They allow developers to define custom workflows to automate tasks,  build, test, and deploy their code directly from their github repository.

->how it works 1st you have to push it to a github then run unit tests and finally watch the result. 
