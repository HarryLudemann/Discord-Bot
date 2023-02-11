# Discord Bot

## Local Setup
Locally running the bot is possible, so long as .env are set, requirements are installed and a postgres server running and accessible.
### 1. Clone Repository
Clone the repository and move into the cloned folder.
```
git clone https://github.com/HarryLudemann/Discord-Python
cd KyraDiscordBot
```
### 2. Create .env File
Create .env file in folder to store environment variables, set the following variables.
```
BOT_TOKEN=
POSTGRES_HOST=
POSTGRES_DATABASE=postgres
POSTGRES_USER=
POSTGRES_PASSWORD=
```
### 3. Install Requirements
```
pip install -r requirements.txt
```
### 4. Run Bot
```
python start.py
```

## Docker Setup
### 1. Start Postgres Server
Install the postgres alpine version from docker hub, then run the following command.
```
docker run --name postgres -e POSTGRES_USER=username -e POSTGRES_PASSWORD=pw -d -p 5432:5432 postgres:alpine
```

### 2. Clone Repository
Clone the repository and move into the cloned folder.
```
git clone https://github.com/HarryLudemann/Discord-Python
cd KyraDiscordBot
```
### 3. Create .env File
Create .env file in folder to store environment variables, set the following.
```
BOT_TOKEN=
POSTGRES_HOST=
POSTGRES_DATABASE=postgres
POSTGRES_USER=
POSTGRES_PASSWORD=
```
### 4. Build/Run Docker Image
Build and run the Discord bot with following commands.
```
docker build --tag discord-py .
docker run --name discord-py discord-py
```

## Development
### Build/Push Docker Image
Run the following commands to build a docker image from project.
```
docker build --tag discord-py .
docker tag discord-py harryludemann/discord-py
docker push harryludemann/discord-py
docker run --name discord-py discord-py
```
