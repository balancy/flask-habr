# Habr news

Web-app representing simplified version of [habr.com](https://habr.com/ru/).

![App image](https://i.ibb.co/82z4Zxy/habr.png)

In the app it's possible:
1. To see last posts
2. To see one post in details
3. To see all posts that have a specified tag in it
4. To see all posts that are written by specified user
5. To login, register, logout
6. To parse last news from original site if you are logged in

## Install app

Python3 and Git should be already installed. 

1. Clone the repository by command:
```console
git clone https://github.com/balancy/flask-habr
```

2. Go inside cloned repository and create virtual environment by command:
```console
python -m venv env
```

3. Activate virtual environment. For linux-based OS:
```console
source env/bin/activate
```
&nbsp;&nbsp;&nbsp;
For Windows:
```console
env\scripts\activate
```

4. Install requirements by command:
```console
pip install -r requirements.txt
```

5. Rename `.env.example` to `.env` and define your proper values for environmental variables:

- `POSTGRES_USER` — postgres db user
- `POSTGRES_PASSWORD` — postgres db password
- `POSTGRES_HOST` — host where you run the app

## Launch db

1. Run docker container with postgresql db
```console
docker-compose up -d 
```

2. Initialize db by command:
```console
flask db init
```

3. Upgrade db by command:
```console
flask db upgrade
```

4. You can create an admin by command
```console
python3 create_admin.py
```

## Launch app

App is launched by command
```console
python3 wsgi.py
```

## Populate DB

It's possible to populate DB in the app. You need to be logged in. You write `/refresh` after your host name.
```
host_name/refresh
```

## Project goals

Code is written for study purpose.

