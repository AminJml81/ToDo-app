# ToDo app


## Project Description
* Custom user with email as username.
* custom backend which users can login with email.
* Users SignUp, Login, Logout, password change and reset functionality.
* CRUD functionlity for tasks.
* REST API version with rest_framework with 5 versions explained below.
* search, custom filterset , pagnation functionality


## API Versions Description
#### V1: Function Based with APIView
![v1](https://github.com/user-attachments/assets/87dc0f6d-8ad9-4887-a1ee-4519119c4ad2)

#### V2: Class Based with APIView
![v2](https://github.com/user-attachments/assets/fa6782ac-68f4-4e53-b5fe-5c7c8e216d0f)

#### V3: Class Based with GenericView
![v3](https://github.com/user-attachments/assets/10114f69-377f-4ee3-befa-dffafa45631c)

#### V4: Class Based with GenericView Concrete Views
![v4](https://github.com/user-attachments/assets/a98b19db-d51e-4c54-91a5-bb02d309b7ae)

#### V5: class Based with Viewsets and Router
 ![v5](https://github.com/user-attachments/assets/bd54031f-02f0-42c1-85b2-731f84fa854c)


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
![task_model_schema](https://github.com/user-attachments/assets/d57397d6-f6a0-42e8-b196-b6bdf92544d7)
