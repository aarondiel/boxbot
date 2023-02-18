# installation and running the bot

first clone the repository:

```sh
git clone git@github.com:aarondiel/boxbot
```

---

to run it use `docker` in combination with `docker-compose`.

here is a sample `docker-compose.yaml` file:

```yaml
services:
  boxbot:
    build: ./boxbot
    environment:
      TOKEN: "YOUR_DEV_TOKEN_HERE"
      COMMAND_PREFIX: "box::"
 
    volumes:
      - ~/Pictures/memes:/data/memes:ro
      - ~/Public/elotrix:/data/elotrix:ro
      - ~/Public/offensive_memes.txt:/data/offensive_memes.txt:ro
```

- `build` is the directory you just cloned
- `TOKEN` specifies the api token of your bot
- `COMMAND_PREFIX` is what every command has to be prefixed with (i.e. `box::meme` if `COMMAND_PREFIX="box::"`)
- you need to mount some files to the container, for it to function correctly:
	- `/data/memes` a meme folder
	- `/data/offensive_memes.txt` a blacklist of memes not to show
	- `/data/elotrix` a folder with random screams
