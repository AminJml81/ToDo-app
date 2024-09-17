# ToDo app


## Project Description
* Custom user with email as username.
* custom backend which users can login with email.
* Users SignUp, Login, Logout, password change and reset functionality.
* CRUD functionlity for tasks.
* REST API version with rest_framework with 5 versions explained below.
* search, custom filterset , pagnation functionality


## API Versions Description
### V1: Function Based with APIView
### V2: Class Based with APIView
### V3: Class Based with GenericView
### V4: Class Based with GenericView Concrete Views
### V5: class Based with Viewsets and Router
 

## Technologies used
* Django
* DjangoRestFramework
* DjangoFilters
* sites framework
* Postgresql
* Docker


## URLS
* admin/

* tasks/
* tasks/ create/
* tasks/ <slug:slug>/
* tasks/api/v[1-5]/ GET, POST
* tasks/api/v[1-5]/<slug:slug> GET, POST, PUT, PATCH

* accounts/
* accounts/ login/
* accounts/ signup/
* accounts/ logout/
* accounts/ password/change/
* accounts/ password/reset/
* accounts/ password/reset/done/
* accounts/ password/reset/confirm/<uidb64>/<token>/
* accounts/ password/reset/complete/


## TODO
* add authentication api
* add tests


## Project Model Schema
![Project Model Schema](/images/model_schema.png)
