
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export FLASK_export=production
export FLASK_DEBUG=0
export SECRET_KEY='asdasvasv77sa0970932=/(6'


gunicorn --bind 0.0.0.0:80 -w 5 app:app