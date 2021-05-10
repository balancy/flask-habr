1. Run db by `docker-compose up -d`

[comment]: <> (2. Connect to db)
2. Initialize db by `flask db init`   
3. Make migration db by `flask db migrate -m 'Initial migration'`
4. Upgrade db by `flask db upgrade` 