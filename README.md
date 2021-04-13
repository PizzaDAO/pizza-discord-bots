# pizza-discord-bots

For Laszlo!

## Instructions

- Clone Repository

    ```bash
    git clone git@github.com:PizzaDAO/pizza-discord-bots.git && cd pizza-discord-bots
    ```

- Run Docker Container

```bash
docker-compose up --build
```

If you're new to docker, don't fret; check out [this guide](https://docs.docker.com/get-started/)

## Updating Requirements

```bash
pip freeze > requirements.txt
```

Using `pip freeze` installs all packages, even those from other projects

Instead, you can update requirements by using `pipreqs`

```bash
pip install pipreqs
```

then

```bash
pipreqs path/to/project
```

If you're running it within the repo (i.e. `cd pizza-discord-bots`), you can use the following command

```bash
pipreqs .  --force
```

`--force` is used to overwrite existing file.

## Run unit tests

TODO
