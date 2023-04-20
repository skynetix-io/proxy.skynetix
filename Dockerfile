FROM python:3.10.5

# set work directory
WORKDIR /nodo

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV SECRET_KEY='asdasvasv77sa0970932=/(6'
# copy project
COPY ./app/ /nodo/app/
COPY ./requirements.txt /nodo/

RUN apt-get update && apt-get install -y default-mysql-client && rm -rf /var/lib/apt

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

EXPOSE 5000
CMD ["gunicorn","app:app","-w 1","--bind","0.0.0.0:5000","--timeout","250"]
