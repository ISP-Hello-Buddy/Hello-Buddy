<p align="center"><img src='https://user-images.githubusercontent.com/92836354/204365674-a3b8e4c0-39a0-46d3-a4c3-9cf105bd6f2a.png' width=300></p>


# Hello-Buddy
[![Django CI](https://github.com/ISP-Hello-Buddy/Hello-Buddy/actions/workflows/django.yml/badge.svg)](https://github.com/ISP-Hello-Buddy/Hello-Buddy/actions/workflows/django.yml)

a web application for those who need some companion.

## How to install 
make sure that you have python in your computer
first, clone this repository by type this command in your terminal at your choosen path
```
git clone https://github.com/ISP-Hello-Buddy/Hello-Buddy.git
```
go to project directory
```
cd Hallo-Buddy
```

Start the virtual environment.
``` 
python3 -m venv env
```

Activate env
- on macos and linux
```
source env/bin/activate 
```
- on windows
```
env\Scripts\activate.bat
```

make sure that you install all the requirements by run this command, its can be whether pip, pip3
```
pip install -r requirements.txt
```

Create file .env
``` 
Create file name .env and follow the sample.env file in this repository 
```

Create a new database by running migrations the database.
```
python3 manage.py migrate
```
In this time you can run server by use command 
```
python manage.py runserver
```
but you have python3 use command
```
python3 manage.py runserver
```
next you go to `http://127.0.0.1:8000/` or `localhost:8000/` for application.

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [User stories](../../wiki/User%20stories)
- [Requirements](../../wiki/Requirements)
- [Development Plan](../../wiki/Development%20Plan)

## Project Plan
- [Iteration 1](../../wiki/Iteration%201) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/5)
- [Iteration 2](../../wiki/Iteration%202) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/6)
- [Iteration 3](../../wiki/Iteration%203) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/7)
- [Iteration 4](../../wiki/Iteration%204) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/8)
- [Iteration 5](../../wiki/Iteration%205) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/9)
- [Iteration 6](../../wiki/Iteration%206) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/10)
- [Iteration 7](../../wiki/Iteration%207) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/11)
- [Iteration 8](../../wiki/Iteration%208) and [Task Board](https://github.com/orgs/ISP-Hello-Buddy/projects/1/views/12)

## Code Review
- [Code Review Docs](https://docs.google.com/document/d/1RFhCYMuJuZ3QQoBI4gucfbdxvh8CyPY8-IAQZVW8HFE/edit#) and [Code Review Wiki](../../wiki/Code%20Review)
- [Code Review Summary](https://docs.google.com/document/d/1nu7uUv_mmL0KtEfbb8aDok8sVXAqvJvsyUHIno5fWPY/edit)

