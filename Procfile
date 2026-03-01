web: gunicorn quran_project.wsgi --bind 0.0.0.0:$PORT
release: python manage.py migrate && python manage.py load_quran_data
