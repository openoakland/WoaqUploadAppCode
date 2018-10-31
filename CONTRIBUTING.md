# Getting set up for collaborative development

## Fork the code

For the main `Ethan-bradley` branch to your github account using the "Fork" button on https://github.com/Ethan-bradley/WoaqUploadAppCode


## Set up your collaborative development workflow


```console
# set up your fork as `origin`
git clone git@github.com:<your-github-username>/WoaqUploadAppCode.git
cd WoaqUploadAppCode
# add the main repo as `upstream`
git remote add upstream git@github.com:Ethan-bradley/WoaqUploadAppCode.git
```

The development workflow:

1. Pull most recent changes from main repo (`upstream`)
2. Commit changes to your fork (`origin`).
3. Push commits to your fork.
4. Open a pull request (PR) on the main repo.
5. Get reviewed.
6. Merge PR!


# Running the site locally

## In a Docker container

[Install docker on your system.](https://docs.docker.com/install/)

```console
# build the woap app docker image
docker build -t woaq-flask .

# start a container
docker run --name my-woaq-flask -p 4555:4555 woaq-flask

# stop the container
docker stop my-woaq-flask

# remove the container
docker rm my-woaq-flask
```

While the container is running, visit localhost:4555 in your web browser.
