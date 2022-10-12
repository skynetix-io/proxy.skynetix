from flask import render_template,session,make_response,request,redirect,url_for,Blueprint
from datetime import timedelta
from app.account import check_loggin
console = Blueprint('console', __name__,template_folder='templates/console',static_folder='static')

@console.before_request
def check_for_maintenance():
    if not check_loggin(strong=True):
        return redirect(url_for("account.login"))
    elif check_loggin():
        return redirect(url_for("account.activate"))

    maintenance = False
    if maintenance: 
        return render_template('console_404.html')

@console.route('/404')
def page_not_found():
    return render_template('console_404.html'),404

@console.route('/')
def index():
    return render_template('console_index.html')

@console.route('/account/')
def account():
    return render_template('console_index.html')