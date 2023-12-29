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

=>  there are several packages but since we want alpine type so the previous is enough.

# Testing Using Patch
-> it is one if the unittest.mock module is used for temporarily replacing an object with a mock object. mostly we use it for testing phase to isolate and test specific parts of your code without affecting other
        some key uses for using mocks in Django:
            1-> Isolate Dependancies
            2-> Simulate Behavior(helps to simulate external services like APIs, or Databases..without depending on external services)
            3-> Verify Method Calls(provides the ablity to  verify whether specific methods or functions are called with the expected parameters & ensure that your code is interacts correctly with its dependencies.)

# Django User Model
->it is like the foundation of the django auth system but it has one of the major problem in it , it isnot easy to customize it.
-> The main reason to say this is modifying the User model in Django requires creating a new customer User model, which can lead to complicates with the database migrations and constraints.so who ever read this use your own user  databases
-> the other reason is many django applicationss and third party packages are built with assumptions about the default User model so customizing the User model may require adjustments to these dependancies, potentialy leads to compatability issues.
->So in this project we are going to use "AbstractBaseUser" and "PermissionsMixin" model
-> AbstractBaseUser -> it is a convinient and powerful way to create customer user model with your desired fields and behaviors, So you will have full control over the fields and methods that defines your user model.(like you can customize it in whatever way you want.)

# User model manage
-> it is a class that is responsible for creating, updating and deleting user objects in the database. it also plays crucial roles in Django authentication system and is associated with the user model, which is used for user authentication and authorization within the application.
-> The User model manager typically provides method for common user-related operations like creating new users, retrieving user instances, and managing user permissions.
-> It allows you to perform various tasks related to user management and authentication, including custom queries and user-specific operations


# Django Admin
-> it is one of the GUI for model that is created in django so using admin you can Create, Read, Update, Delete users and other staff.
->  Very little coding required inorder to setup Django admin.

#  Test Admin site
-> Testing Django admin is to ensure the correctness and reliablity of an application adminstrative interface.Django provide a testing framework to test the admin like here is an example.

# DRF(django restframework) automatic documentation
->there is a third party libraries in django which is used to generate documentation called "drf-spectacular".
-> schema means the structure of the API including the avialable endpoint, method, and data format.
-> the drf-spectacular generates Schema(so the schema file is documented in JSON OR YAML) it explains the API(endpoint) in a standrad way.
-> So the schema is going to give a browsable web interface inorder to have infromation about api.

# Open API SCHEMA
-> This will be used by swagger, which is an open source tool that can generate html pages from your code.
-> It uses JSON OR YAML format to describe the structure of the RESTful API.
-> by providing OpenAPI description of your API, you can generate interactive and user friedly description using a tools like Swagger UI or ReDoc so other developer can easily understand API's endpoint, request/response formats, and authentication and mechanism


# Testing
->There are two  types of testing public and private testing. public testing it means that it test unauthenticated requests like registeing a new user

# Serializer
-> use for transforming complex data types such as Django models or querysets, into python data types that can be easily converted to JSON and sent to a client or recieved from a client.
-> some reason why we use serializers are like Data-Validation(they provide a  convinient way to validate an incoming data to ensure that the data meets certain criteria before it passed for further process )
-> A serializer class is responsible for converting complex datatypes into python objects or vice versa.

# types of authentication

->Basic - send username and password with each request
->Token - use a token in the HTTP header
->JSON Web Token(JWT) -Use an access and refresh token
->Session - Use cookies

->But in this project we used TOKEN AUTHENTICATION becouse it simplicity and largely used among Django community and lastly it avoid sending username/password each time.

# TOKEN AUTHENTICATION
-> STEP 1 each time the user logs in the server generates a unique token that is going to be associated with the user.
-> STEP 2 the client stores the token locally, typically with the secure manner like cookie or local storage.
-> STEP3 for each request to the server the client include the token in the request header. so the token is usually sent using Authorization header like this `Autorization: Bearer <token>`.
-> STEP 4  Upon recieving a request the server extracts the token from the request header & validate the token to ensure it's legitimate
-> STEP 5   Token authentication is statless becouse it doesn't store the user session..
-> each token has it's expiration time so if the token expires the user needs to re-authenticate.


# APIView
-> it is more focused on HTTP methods which means like GET, POST, PATCH, DELETE, PUT
-> provide flexiblity over urls and logic
->Useful for non CRUD APIs
        -> Avoid for simple Create,Read, Update, Delete APIs
->it provide also a lots of built- in features such as handling authentication, permissions and responce formatting.so it is a flexible way to structure the views and allows you to define diffrent methods for diffrent HTTP methods in a single class.

# ViewSet
->it is a class that bundles the logic for variouss HTTP methods(GET, POST, PUT, DELETE, etc.) into separate class method. for example 'list' for handling list objects(GET).CREATE for creating an object(POST).'retrieve' for retrieve single object(GET)...
-> Provides actions for list, create, retrieve, update, partial_update, destroy
-> Useful for CRUD APIs
->Use Routers to automatically generate URLs.

# Mixins
-> it is a way to achieve multiple inheritance in Python.It can allows you to inherit functionallity from multiple sources, instead of bieng limited to inherit from single class.
-> for example from the project in recipe app in the view.py file the tagviewset class inherit  two mixin (mixins.ListModelMixin, mixin.UpdateModelMixin) so each mixin it provide a set of functionality.like ListModelMixin provides the list acition for a view, that allows you to retrieve a list of objects from the database(GET Method.) and UpdateModelMixin for updating actions(patch or put.) for updating the tag.


# Refactoring
-> It is a software engineering process that aims to improve the internal structure of code. This can include modifying variables, classes, or functions. Refactoring is performed to enhace readablity and maintainablity as well as to reduce redundancy and improve perfromance.

# static and media file
## Static files are served from a folder named static inside your Django project directory. Generated on build
-> Static files are served from STATIC_ROOT directory.
## medial file are uloaded at runtime like user upload.
 
