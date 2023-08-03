an api that is used for recipe app.

in this Project we are using docker, postgress and django(python web framework) 

# Docker 
docker is a containerization technology which allows us to package an application with all its dependencies into and also it is an opensource platform that allows developers to automate deployment, scaling, and mangement of applications inside lightweight, portable container. 
# container 
container are self contained units that package all the neccessary software, libraries, and dependancies needed to run an application.
# Docker Compose
-> it is a tool that is provided by a docker that allows to define and manage multi container Docker application. it uses YAML file to configure the services, networks, and volumes required for application enviroment. it can automates the process of starting, stopping, and  connecting multiple container. By writing one single  command you can  bring up an entire application defined in the compose file.
-> in order to use a docker compose we have to create docker-compose.yml file in our project and configure it inside the file.

1- create a file named Dockerfile in the root directory of your project with following content:
```dockerfile   

FROM python:3.11-alpine3.17
LABEL maintainer="beba2123"

ENV PYTHONBUFFERED 1  

COPY ./requirements.txt /tmp/requirements.txt   # copy requirements to image
Copy ./app /app
WORKDIR /app
EXPOSE 8000
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirnments.txt && \
    rm -rf /tmp \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV  PATH="/py/bin:$PATH"

USER django-user


# 2nd step is create a file called docker-compose.yml and inside of it we write 
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
