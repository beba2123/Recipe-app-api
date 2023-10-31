an api that is used for recipe app.

in this Project we are using docker, postgress and django(python web framework) 
# requirements.txt and requirments.dev.txt
->so the main diffrence btn them is we used it for listing all dependancy required for the production enviroment.these are packages needed to run application in stable and reliable manner.

# requirments.dev.txt 
-> we use this for listing the development dependancies like a packages needed for development and testing purpose. eg. flake for linting and testing, debugging

# Docker 
docker is a containerization technology which allows us to package an application with all its dependencies into and also it is an opensource platform that allows developers to automate deployment, scaling, and mangement of applications inside lightweight, portable container. 
# Docker images
-> they are a blue print for container which means that they can be runtime enviroment, application code, commands, or any dependancies

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

# Django test framework

=> django comes with a built in testing framework that makes it easy to write and run unit tests for your web applications. the testing framework provides testcases, running tests, and asserting expected behavior.
=> 1 test cases is defined as subclass of 'django.test.TestCase'. Test cases can contain one or more method that represent a specific test scenario.
=> 2 Fixtures are states  of predefined data used to setup intial state for your tests.

=> 3 Assertions -> django provides a set of assertion method that allows to check certain condtion are met during testing.

=> 4 Test Clients ->testing client simulates making requests to your views and testing responces.it allows you to interact with your views and testing the rendering templates.
 

# where do you put tests?

-> by creating placeholder or a file like tests.py and added to each app
-> or create test/ subdirectory to split tests up
NOTE!! only use one of the two not both
       test modules must starts with test_
       test files can be named anything but they should end with _test.py
       test directories must contain __init__.py


# Test classes 
    -> SimpleTestCase
        --> we use it for no database is required for a test
        --> save time during excuting test.
    -> TestCase
        --> Database integration
        --> Useful  for testing code that uses database


# Mocking 
    -> it one of the technique that is used for testing a software.it is particularly used for when testing interaction between diffrent component or a system that are not easily testable due to dependancies, external services, or complexity so mocking allows us to  isolate the code that going to be tested.
# benefits of mocking
    ->avoid unintended consequences(it allows you to eliminate unitended side effects by replacing real components with controlled substitutes.)
    ->avoid relying on external services.
    ->speed up testing 
    -> focused testing
    -> reduce dependencies
    -> make tests more reliable

# How to write mocks in python ?
    -> we use unittest.mock
     


# Test request in django using APIClient
->Testing requests is used to ensure that the API endpoints in your django application work as expected. so django provides a testing framework that makes it easy to create test cases for your views, APIs, and other components. you can use this framework to stimulate HTTP request and validate reponce.

-> first import APIClient from rest_framework.test
-> then call client = APIClient() inside our test class
-> now we have access to all methods available in API Client like get, post etc...
-> make request by using the endpoint that we want
-> check the result by using assertEqual

EXAMPLE
from rest_framework.test import APIClient

    class TestViews(simpleTestCase):

        def test_get_greeting(self):
        """test getting greeting"""
            client = APIClient()
            res = client.get('/greeting/')
            self.assertEqual(res.status_code , status.HTTP_200_OK)
            self.assertEqual(
                res.data, ["hello", "akaam", "endet nehe", hola! ],
            )


# Configuring Database

-> in this project we are going to use PostgreSQL database(open source database) and it can integrate well with django.


 # how to set up network connectivity between the database(Postgres) and Django(app)
-> we can automatically using docker-compose
   1st -> we setup depends_on on app service to start db(database) first to make sure that one service is start overone another.
   2nd -> docker-compose creates a network on the background between app service and db service in which the db uses it as a hostname

-> Volumes
    -> it is how we store persistent data using docker compose.they are a way to share data and store data separately from the container's file system, and they play crucial role in making data available to container, even if the containers are stopped, started, or even deleted.

-> Enviroments 
    -> used for configuring and customizing how the services run and the configuration and the services happens without affecting the source code.
    -> it creates a dynamic behavior in your application for example if you want to run your application in debug mode or in production mode you can use envriroments.

# Psycopg2
-> it is popular open source PostgreSQL database adapter for pyhton programming language it allows python application to interact with PostgreSQL databases by providing db API to perform various database operation like quering, manupilating, connecting data. 

# Docker services timeline
-> first the docker database start first then (service start) after the service started  then django app service start and then both the postgres and App start simultinously but the postgres to begin the process to begin it takes quite a lot time to start but App will start and setup the connection for the database and try to connect to the database(Postgres) but this one create an error becouse postgres still is not ready to connect so this create an error.

=>> so the solution is using wait_for_db command in django which means that it continiously check until the database is ready(postgresql database) so when it is ready it connect to the Django app.

# installing postgresql in dockerfile

=> So in this project the package that we are going to use inorder to install for the alpine version ->postgresql-client
               ->Build-base
               ->postgresql-dev
               ->musl-dev
=>there are several packages but since we want alpine type so the previous is enough.

