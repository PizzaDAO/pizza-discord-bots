[![Build Status](https://dev.azure.com/dayvihd/RarePizzas/_apis/build/status/PizzaDAO.pizza-discord-bots?branchName=main)](https://dev.azure.com/dayvihd/RarePizzas/_build/latest?definitionId=6&branchName=main)

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

## Release Process

We are using Azure Services to host our web app for containers.
We have also integrated Azure DevOps to set up a minimal viable CI/CD pipeline.

Currently, you can trigger a container build pipeline by creating a PR with the `main` branch. If the build is successful, the image is pushed to our Azure container registry. Subsequently, the PR will update with the build status. Once a PR is approved, the production release pipeline is triggered. This simply takes the image from our container registry and deploys it to our Azure App Service.

You can monitor the status of the web app and discord bot here:
https://super-pizza-trainer.azurewebsites.net/

Because we have no intermediary stages (i.e. dev, staging, qa, etc.) you need to ensure the image you build locally works.
I suggest creating a separate discord server (it's free) and spinning up a new bot that you can use to test your changes.
Simply do the following once you have a new discord server:

1. Create a new bot [here](https://discord.com/developers/applications)
2. Apply the same permissions as the bot you are modifying
3. Create a `.env` file
4. Add the following env variables

   - `TOKEN=<your-new-test-bot-token-hurr>`
   - `WEBSITES_PORT=8080`

5. Create and start all the services by running the following command:
   `docker-compose up --build`
6. Manually test away!
7. Oh and add unit tests! :)

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

`--force` is used to overwrite existing file

## Run Unit Tests

TODO
