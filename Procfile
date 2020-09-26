release: python manage.py makemigrations && python manage.py migrate --run-syncdb && python manage.py migrate
web: gunicorn getplacebot.wsgi --log-file -
