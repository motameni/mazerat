cd .
source ./Scripts/activate
py ./mazeratsite/manage.py runserver

# cd mazeratsite/
# python -m celery -A mazeratsite worker --pool=solo --loglevel=info
# python -m celery -A mazeratsite beat --loglevel=debug
# python -m celery -A mazeratsite flower
# python -m pip check
