# Discord-Python

## Setup
### Creating docker image
install the postgres alpine version from docker, then create image:
```
docker run --name discord-py-postgres -e POSTGRES_USER=username -e POSTGRES_PASSWORD=pw -d -p 5432:5432 postgres:alpine
```

### Updating Repo
```
docker build --tag discord-py .
docker tag discord-py harryludemann/discord-py
docker push harryludemann/discord-py
docker run discord-py
```
