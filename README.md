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
Please refer to the [Testing](https://github.com/PizzaDAO/pizza-discord-bots#testing) section below.

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

## Testing

### Unit Tests

TODO

### Manual Testing

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

### Intro to Git and GitHub

If you're new to contributing to open source projects and/or projects with many different contributors, being familiar with Git is basically a must. There are several version control systems but Git is probably the most common.

Checkout [this article](https://product.hubspot.com/blog/git-and-github-tutorial-for-beginners) to familiarize yourself with Git.

Here is the tl;dr for getting started with this repo:

Initial setup:
  1. Create a folder where you want all your pizzaDAO repos to live in `mkdir pizzaDAO`
  2. Change into that directory `cd pizzaDAO`
  3. Clone the repo `git clone https://github.com/PizzaDAO/pizza-discord-bots.git`

You should now have the latest and greatest version of the code on your local machine. The following steps/commands will be used frequently so really try to familiarize yourself with them. This is what streamlines collaboration between many people across the world!

1.  `git switch main` makes sure you are on the main branch! This is set to track the `main` branch you see on the website.
2.  `git pull` this grabs any updates to the `main` branch on the website that others might have made. You always want to have the latest changes to avoid any unnecessary conflicts. Conflicts happen when two or more people make changes to the same code in a file. These usually are resolved on their own but sometimes, if the changes are complex, a human has to manually resolve the conflicts.
3.  `git checkout -b <new_feature>` make sure you work on a new branch which you will push to the website.
4.  `git add -A` once you have made all the changes and tested, add all the files that you want to commit. You can also add specific files by listing them in place of `-A` i.e. `git add file_1.py file_2.py` etc.
5.  `git commit -m"enter a message here about the changes you made"` commits the files; add a nice short message that summarizes the changes you made.This helps devs understand the history of the code. To view past commits use `git log` and tap the space bar to scroll down; type q to exit that view. I usually do the following `git log | head -n 15` where -n is the # of lines you want to view starting from the top. 15 is usually enough to view the last 2-3 commits.
6.  `git push -u origin <new_feature_branch>` where `new_feature_branch` is whatever you named your branch in `step 3` above.
7.  Finally, go to the website and create a Pull Request (PR) request from `new_feature_branch` into `main`. Enter a short descriptive title and fill out the description with any relevant details/questions/concerns you have regarding the PR. Tag someone for a review and let them give you feedback; if it's good to go, they will approve and merge.

If changes are requested, simply make the changes on the same branch and start from step 4 above to push the updates! It will update the same PR so ignore step 7. Please don't create a new PR since we want to maintain all of the feedback in one location so that if many people are reviewing it, they are aware of why certain changes have been made.


For a deeper dive into Git, checkout thier website: https://git-scm.com/