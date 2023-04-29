# running the bot

you can run the bot using the latest github package.

for that create a `docker-compose.yaml` file:

```yaml
services:
  boxbot:
    image: ghcr.io/aarondiel/boxbot
    restart: unless-stopped
    container_name: boxbot
    hostname: boxbot
    environment:
      TOKEN: "YOUR_DEV_TOKEN_HERE"
    
    volumes:
    - ~/Pictures/memes:/data/memes:ro
    - ~/Public/elotrix:/data/elotrix:ro
    - ~/Public/offensive_memes.txt:/data/offensive_memes.txt
```

# necessary options

environment variables:
- `TOKEN` specifies the api token of your bot

you need to mount some files to the container, for it to function correctly:
- `/data/memes` a meme folder
- `/data/elotrix` a folder with random screams
- `/data/offensive_memes.txt` a blacklist of memes not to show

# building from source

first clone the repository:

```sh
git clone git@github.com:aarondiel/boxbot
```

---

to build and run it use `docker` in combination with `docker-compose`.

here is a sample `docker-compose.yaml` file:

```yaml
services:
  boxbot:
    build: .
    restart: no
    container_name: boxbot
    hostname: boxbot
    environment:
      TOKEN: "YOUR_DEV_TOKEN_HERE"
 
    volumes:
    - ~/Pictures/memes:/data/memes:ro
    - ~/Public/elotrix:/data/elotrix:ro
    - ~/Public/offensive_memes.txt:/data/offensive_memes.txt
```

run `docker compose up` to start the docker container
