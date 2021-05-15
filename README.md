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

2. Rename `.env.example` to `.env` and define your proper values for environmental variables:

- `POSTGRES_USER` — postgres db user
- `POSTGRES_PASSWORD` — postgres db password
- `POSTGRES_DB` — postgres db name

## Launch app in docker container

Docker should be already installed.

1. Build db and app by command:
```console
docker-compose build 
```

2. Run db by command:
```console
docker-compose build db -d 
```

2. Run app by command:
```console
docker-compose up app -d
```

App will be available via:
```
host_name:5050
```
where `host_name` is the name of your host

## Populate DB

It's possible to populate DB in the app. You need to be logged in. You write `/refresh` after your host name.
```
host_name/refresh
```

## Project goals

Code is written for study purpose.

