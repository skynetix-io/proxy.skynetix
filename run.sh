
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export FLASK_export=production
export FLASK_DEBUG=0
export SECRET_KEY='asdasvasv77sa0970932=/(6'

while true
do
    gunicorn --certfile=your_domain_chain.crt --keyfile=server.key --bind 0.0.0.0:443 -w 5 app:app
done