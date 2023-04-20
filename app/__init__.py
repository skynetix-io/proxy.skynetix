from flask import Flask
from app.config import Config
from flaskext.mysql import MySQL


app = Flask(__name__)

app.config.from_object(Config)
mysql = MySQL()
mysql.init_app(app)

from app import general
from app.account import account
from app.proxy import proxy
from app.console import console
app.register_blueprint(account)
app.register_blueprint(proxy)
app.register_blueprint(console)


