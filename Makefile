.PHONY: fe fe2 frontend clean_pyc pyflake8 pyoutdated pypylint pystatic pyuser herokupush pymigrate pycron

fe:
	lein clean && lein cljsbuild once min

fe2:
	cd frontend && lein clean && lein cljsbuild once min

frontend: fe fe2

clean_pyc:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

pycron:
	docker-compose -f dev.yml run django python manage.py runscript refresh_users

devpi:
	devpi-server --start --host=0.0.0.0

herokupush:
	git push heroku master
	heroku run python manage.py migrate
	heroku run python manage.py clearsessions

populate_history:
	heroku run python manage.py populate_history --auto

stop:
	docker stop $$(docker ps -aq)
