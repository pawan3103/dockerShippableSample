
from fabric.api import env, local, run, task
from fabric.context_managers import shell_env

# Commands which should work in all environments
# -------------------------------------------------

@task
def build():
    """Build the docker containers."""
    vars = dict(COMPOSE_FILE=env.COMPOSE_FILE, DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE)
    with shell_env(**vars):
        local("docker-compose build")

@task
def up():
    """Start the docker containers."""
    vars = dict(COMPOSE_FILE=env.COMPOSE_FILE, DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE)
    with shell_env(**vars):
        local("docker-compose up -d")

@task
def stop():
    """Stop the docker containers."""
    vars = dict(COMPOSE_FILE=env.COMPOSE_FILE, DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE)
    with shell_env(**vars):
        local("docker-compose stop")

@task
def outdated():
    """Show outdates python packages."""
    vars = dict(COMPOSE_FILE=env.COMPOSE_FILE, DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE)
    with shell_env(**vars):
        local("docker-compose run django pip list --outdated")

@task
def config():
    """See config variables passed to docker containers."""
    vars = dict(COMPOSE_FILE=env.COMPOSE_FILE, DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE)
    with shell_env(**vars):
        local("docker-compose config")


# Commands for specific environments
# -------------------------------------------------
@task
def django(task=""):
    """Run the make target in the dev environment"""
    env.COMPOSE_FILE = 'dev.yml'
    env.DJANGO_SETTINGS_MODULE = 'config.settings.local'
    vars = dict(COMPOSE_FILE=env.COMPOSE_FILE,
                DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE)
    with shell_env(**vars):
        local("docker-compose run django python manage.py " + task)

@task
def migrate():
    django("migrate")

@task
def test(watch="false", shippable="false"):
    """Run tests in test profile."""
    if shippable == 'true':
        env.COMPOSE_FILE = 'shippable-test.yml'
    else:
        env.COMPOSE_FILE = 'dev-test.yml'
    env.DJANGO_SETTINGS_MODULE = 'config.settings.test'
    env.PYTEST_WATCH = '1' if watch == 'true' else '0'
    vars = dict(COMPOSE_FILE=env.COMPOSE_FILE,
                DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE,
                PYTEST_WATCH=env.PYTEST_WATCH)
    with shell_env(**vars):
        local("docker-compose rm -v --force postgres")
        local("docker-compose build")
        local("docker-compose up --abort-on-container-exit")

@task
def lint(runner='pylint'):
    """Run pylint in test profile."""
    env.COMPOSE_FILE = 'dev-test.yml'
    env.DJANGO_SETTINGS_MODULE = 'config.settings.test'
    vars = dict(COMPOSE_FILE=env.COMPOSE_FILE,
                DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE,)
    with shell_env(**vars):
        local("docker-compose build")
        if runner == 'pylint':
            local("docker-compose run django pylint --load-plugins pylint_django,pylint_common,pylint_celery server/")
        elif runner == 'flake':
            local("docker-compose run django flake8")


@task
def static():
    """Run collectstatic in dev profile"""
    env.COMPOSE_FILE = 'dev.yml'
    env.DJANGO_SETTINGS_MODULE = 'config.settings.local'
    vars = dict(COMPOSE_FILE=env.COMPOSE_FILE,
                DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE)
    with shell_env(**vars):
        local("docker-compose run django python manage.py collectstatic --noinput --clear")

@task
def fixture():
    """Generate fixture data in test profile"""
    env.COMPOSE_FILE = 'dev-test.yml'
    env.DJANGO_SETTINGS_MODULE = 'config.settings.local' # Intentionally use local settings for password hashing
    vars = dict(COMPOSE_FILE=env.COMPOSE_FILE,
                DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE,
                PYTEST_WATCH='0')
    with shell_env(**vars):
        local("docker-compose rm -v --force postgres")
        local("docker-compose build")
        local("docker-compose run django /build-fixtures.sh")


#  Enviroments & Deployments
# ---------------------------------------------------------

@task
def prod():
    """Set environment as production"""
    env.COMPOSE_FILE = 'docker-compose.yml'
    env.DJANGO_SETTINGS_MODULE = 'config.settings.production'

@task
def dev():
    """Set environment as local"""
    env.COMPOSE_FILE = 'dev.yml'
    env.DJANGO_SETTINGS_MODULE = 'config.settings.local'

@task
def production():
    """Set environment as production"""
    env.COMPOSE_FILE = 'aws-rds-docker-compose.yml'
    env.DJANGO_SETTINGS_MODULE = 'config.settings.production'

@task
def staging():
    """Set environment as staging"""
    env.COMPOSE_FILE = 'aws-rds-staging-docker-compose.yml'
    env.DJANGO_SETTINGS_MODULE = 'config.settings.staging'
