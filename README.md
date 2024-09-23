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
![v1](https://github.com/user-attachments/assets/3f51d720-54ff-47f6-bcfe-1865d094d9cd)

#### V2: Class Based with APIView
![v2](https://github.com/user-attachments/assets/9380ca9e-5e6d-4f23-bbe5-dcbecbb6a913)

#### V3: Class Based with GenericView
![v3](https://github.com/user-attachments/assets/a82fc11a-0eab-4c42-90d1-ab2ced756bf8)

#### V4: Class Based with GenericView Concrete Views
![v4](https://github.com/user-attachments/assets/6308fb65-ae7e-4bb3-a836-d6df570e2aeb)

#### V5: class Based with Viewsets and Router
 ![v5](https://github.com/user-attachments/assets/35f18229-3730-4e5f-b0b8-a8c687658fe0)


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
