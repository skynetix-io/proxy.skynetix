
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export FLASK_export=production
export FLASK_DEBUG=0
export SECRET_KEY='asdasvasv77sa0970932=/(6'

while true
do
    gunicorn --bind 0.0.0.0:5000 -w 5 app:app
done