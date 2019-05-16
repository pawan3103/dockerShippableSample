# README for 2.0 setup #

Backend for Fintify based on Django REST Framework

### What is this repository for? ###

* The fintify backend

### How do I get set up? ###

* Install [docker compose](https://docs.docker.com/compose/install/)
* `fab dev build` to build the containers.
* `fab dev up` to start the containers.
* Open `http://localhost:8000/`

For further information, see [this](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html).

To create django superuser, run `fab dev django:createsuperuser`.

### Production ###

* Install [docker compose](https://docs.docker.com/compose/install/)
* `fab prod build` to build the containers.
* `fab prod up` to start the containers.
* Open `http://localhost/`

You may need to delete an earlier postgres volume: `docker-compose rm postgres`

For further information, see [this](https://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

### Development commands ###

* To run django's `manage.py` tasks on the dev container, run for eg.:  `fab django:makemigrations`

### Database Information ###

For backing up or restoring the postgres database, see [this](https://cookiecutter-django.readthedocs.io/en/latest/docker-postgres-backups.html).

1. Firstly backup the database: `docker-compose -f dev.yml run postgres backup`
1. Make sure that no container is running.
1. Start only the postgres container: `docker-compose -f dev.yml up postgres`
1. Now restore the database: `docker-compose -f dev.yml run postgres restore <filename>`

Also see, [heroku docs](https://devcenter.heroku.com/articles/heroku-postgres-import-export)

You can also connect to PostgreSQL running inside docker by running:

```bash
psql -h localhost -p 5432 -U finchest
```

### Backing up database on Heroku ###

First backup and download database to local filesystem.

```
$ heroku pg:backups:capture
$ heroku pg:backups:download
```

Now copy the `latest.dump` file generated to `postgres` volume

```
docker cp <file> <container-id>:/backups
```

You can get `container-id` by doing `docker ps` and getting the id from image `*_postgres`. Now follow the restoring database information.

### Useful Docker commands ###

* `docker ps` - to see running instances
* `docker-compose rm <image>` - to delete a particular image associated with the orchestration.
* `docker stop $(docker ps -a -q)` - to stop all containers
* `docker rm $(docker ps -a -q)` - to delete all containers
* `docker rmi $(docker images -q)` - to delete all images
* `docker system prune` - Delete dangling resources

On setting memory limits in docker-compose, see [this](https://docs.docker.com/compose/compose-file/#/cpushares-cpuquota-cpuset-domainname-hostname-ipc-macaddress-memlimit-memswaplimit-oomscoreadj-privileged-readonly-restart-shmsize-stdinopen-tty-user-workingdir).

### Updating Python Dependencies ###

Use [pip-upgrader](https://github.com/simion/pip-upgrader) to update python dependencies. See [this post](https://stackoverflow.com/questions/2720014/upgrading-all-packages-with-pip/43642193#43642193) for details.

- `pip install pip-upgrader`
- `pip-upgrade <requirements-file>`

### For slow network connections ###

When `requirements.txt` files change, for incremental building of docker containers, pip reaches out to the network for all packages.
To cache PIP packages on your laptop:

1. Setup a [devpi server](http://doc.devpi.net/latest/quickstart-server.html)
1. Start the devpi server on all interfaces as follows: `make devpi`
1. Note the IP address of the `docker0` interface, and replace the IP below with it
1. Setup the `PIP_ARGS` environment variable as follows:  `export PIP_ARGS='--trusted-host <DOCKER0_IP> -i http://<DOCKER0_IP>:3141/root/pypi/+simple/'`
1. Build containers `fab dev build` or `fab prod build`
1. Subsequent builds will use the local server
1. Setup the `DEFAULT_FROM_EMAIL_NAME` environment variable as follows: `export DEFAULT_FROM_EMAIL_NAME=<DEFAULT_FROM_EMAIL_NAME>`
1. Setup the `API_BASE_URL` environment variable as follows: `export API_BASE_URL=<API_BASE_URL>`
1. Setup the `KEY` environment variable as follows: `export KEY=<KEY>`
1. Setup the `SANDBOX` environment variable as follows: `export SANDBOX=<SANDBOX>`
1. Setup the `AUTHY_KEY` environment variable as follows: `export AUTHY_KEY=<AUTHY_KEY>`




