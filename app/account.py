from threading import active_count
from app import mysql_utility as mysql
from app import app
import os,re,secrets,random
from flask import render_template,session,make_response,request,redirect,url_for,Blueprint,jsonify
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from faker import Faker

account = Blueprint('account', __name__,template_folder='templates/account',static_folder='static')

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=180)

@account.route('/404')
def page_not_found():
    return render_template('account_404.html'),404



@account.route('/login/')
def login():
    if check_loggin(strong=1):
        return redirect(url_for('console.index'))
    elif check_loggin():
        return redirect(url_for('account.activate'))
    else:
        return render_template('account_login.html',title="Login")

@account.route('/signup/')
def signup():
    if check_loggin(strong=1):
        return redirect(url_for('console.index'))
    elif check_loggin():
        return redirect(url_for('account.activate'))
    else:
        return render_template('account_signup.html',title="Sign Up")

@account.route('/activate/')
@account.route('/activate/<token>')
def activate(token=""):
    if check_loggin():
        if 1 == 1:
            msg = 'Already activated'
            return redirect(url_for('console.index'))
        else:
            if token == "":
                return render_template('account_activation.html',title="Activate")
            else:
                tuple1 = (token)
                query = """UPDATE general_users set status = 1 WHERE activation_key = % s AND status = 0"""
                if mysql.update(query,tuple1) != 0:
                    msg = "Activated"
                    session["status"] = 1
                    return redirect(url_for("console.index"))
                else:
                    msg = "Wrong Key"
                    return render_template('account_activation.html',title="Activate" ,msg = msg)
    else:
        return redirect(url_for('account.login'))


@account.route('/logout/' )
def logout():
    print("OK")
    session.clear()
    return redirect(url_for('account.login'))

################################## API ##################################

@account.route('/api/signup/' ,  methods=['POST'])
def api_signup():
    if check_loggin(strong=1):
        msg = "Already registered!"
        return {"status":"error","info":msg}
    form = request.form
    app.logger.debug(form,"cccccccccccc")
    if form["last_name"] == "" or form["first_name"] == "":
        msg = "Please fill the name fields!"
        return {"status":"error","info":msg}
    if form["country"] == "" or form["address"] == "" or form["zip"] == "":
        msg = "Please fill the country fields!"
        return {"status":"error","info":msg}
    if form["email"] == "":
        msg = "Please fill the email field!"
        return {"status":"error","info":msg}
    if form["password"] == "" or form["confirm"] == "":
        msg = "Please fill the password fields!"
        return {"status":"error","info":msg}
    if form["privacy"] == "false":
        msg = "Please accept the privacy terms!"
        return {"status":"error","info":msg}
    type = form['type']
    first_name = form['first_name']
    last_name = form['last_name']
    country = form['country']
    address = form['address']
    zip = form['zip']
    email = form['email']
    password = form['password']
    confirm = form['confirm']
    tuple1 = (email)
    query = """SELECT * FROM general_users WHERE email = % s"""
    account = mysql.select(query,tuple1,1)
    if account:
        msg = 'Account already exists!'
        return {"status":"error","info":msg}
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        msg = 'Invalid email address format !'
        return {"status":"error","info":msg}
    if password != confirm:
        msg = "Password doesn't match!"
        return {"status":"error","info":msg}
    #MIGLIORARE CONTROLLI SU COUNTRY E NAME
    else:
        api_key = secrets.token_hex(32)
        activation_key = secrets.token_hex(32)
        history_ip = request.remote_addr
        tuple1 = (type,country,address,zip,first_name,last_name,email,generate_password_hash(password),api_key,activation_key,history_ip)
        query = """INSERT INTO general_users (type,country,address,zip,first_name,last_name,email,password,api_key,activation_key,history_ip) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        id = mysql.insert(query,tuple1,1)
        #FIRST LOGIN
        tuple1 = (id)
        query = """SELECT * FROM general_users WHERE id = %s"""
        account = mysql.select(query,tuple1,1)
        set_current_user_session(account)
        msg = "OK"
        return {"status":"success","info":msg,"link":url_for('account.activate'),"api_key":api_key}

@account.route('/api/login/', methods=['POST'])
def api_login():
    msg = ''
    if check_loggin(strong=1):
        msg = "Already logged!"
        return {"status":"error","info":msg,"link":url_for("console.index")}
    elif check_loggin():
        msg = "Activate your account!"
        return {"status":"error","info":msg,"link":url_for("account.activate")}
    else:
        form = request.form
        if form["email"] == "" :
            msg = "Please fill the email field!"
            return {"status":"error","info":msg}
        if form["password"] == "" :
            msg = "Please fill the password fields!"
            return {"status":"error","info":msg}
        email = request.form['email']
        password = request.form['password']
        query = """SELECT * FROM general_users WHERE email = %s"""
        tuple1 = (email)
        account = mysql.select(query,tuple1,1)
        if account and check_password_hash(account["password"],password):
            set_current_user_session(account)
            app.logger.debug(session)
            if session["status"] == 1:
                msg = 'Logged in successfully and activated!'
                return {"status":"success","info":msg,"link":url_for("console.index"),"api_key":session["api_key"]}
            else:
                msg = "Activate your account!"
                return {"status":"success","info":msg,"link":url_for("account.activate"),"api_key":session["api_key"]}
        else:
            msg = 'Incorrect email or password!'
            return {"status":"error","info":msg}

@account.route('/api/add_order/', methods=['POST'])
def add():
    msg = ''
    form = request.get_json(force=True)
    app.logger.debug(form)
    if form["token"] == "" :
        msg = "Invalid client"
        return {"status":"error","info":msg}
    from_ = form['from']
    email = form['email']
    amount = form['amount']
    currency = form['currency']
    query = """SELECT * FROM general_users WHERE email = %s"""
    tuple1 = (email)
    account = mysql.select(query,tuple1,1)
    app.logger.debug(account)
    if not account:
        if from_ == "paypal":
            random_ = 0
            country_code = form['country_code'].lower()
            app.logger.debug(country_code)
            country = {"au":"en_AU","it":"it_IT","us":"en_US","fr":"fr_FR","ca":"fr_CA","ro":"ro_RO","gb":"en_GB","nl":"nl_NL"}
            if country_code in country:
                country_code = country[country_code]
            else:
                country_code = "en_US"
                random_ = 1
            app.logger.debug(country_code)
            name = form['name']
            postal_code = form['postal_code']
            state = form['state']
            city = form['city']
            street = form["street"]
            type = "personal"
            if random_ or postal_code == None or state == None or city == None or street == "":
                app.logger.debug(country_code)
                fake = Faker([country_code])
                address = fake.address()
            else:
                address = street + " " + city + " " + postal_code + " " + state
            

        elif from_ == "panel":
            type = "personal"
            country_code = random.choice(['en_US','en_US','en_US','en_US','en_US','en_CA','zh_CN','it_IT','de_DE','en_GB'])
            fake = Faker([country_code])
            address = fake.address()

        password = email+name
        api_key = secrets.token_hex(32)
        activation_key = secrets.token_hex(32)
        history_ip = request.remote_addr
        tuple1 = (type,country_code,address,name,email,generate_password_hash(password),api_key,activation_key,history_ip)
        query = """INSERT INTO general_users (type,country,address,name,email,password,api_key,activation_key,history_ip) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        mysql.insert(query,tuple1,1)

    tuple1 = (email)
    query = """SELECT id FROM general_users WHERE email = % s"""
    uid = mysql.select(query,tuple1,1)["id"]
    r=random.randrange(0,3)
    if r==1:
        type="IPV6"
        spent=amount
        quantity=1

    else:
        type="IPV4"
        spent=amount
        quantity=1

    query = """INSERT INTO general_orders (type,quantity,spent,uid,currency) VALUES (%s,%s,%s,%s,%s)"""
    tuple1=(type,quantity,spent,uid,currency)
    id = mysql.insert(query,tuple1,1)
    msg = 'Ok'
    return {"status":"success","info":msg}

@account.route('/api/get_new_order/', methods=['GET'])
def get_new_order():
    msg = 'Ok'
    tuple1=()
    query = """SELECT * FROM general_orders INNER JOIN general_users ON general_orders.uid = general_users.id WHERE sent != 1;"""
    data = mysql.select(query,tuple1)
    return {"status":"success","info":data}

@account.route('/api/set_order/<id_>', methods=['GET'])
def set_order(id_):
    msg = 'Ok'
    tuple1 = (id_,)
    app.logger.debug(id_)
    query = """UPDATE general_orders SET sent = 1 WHERE id = %s;"""
    if mysql.update(query,tuple1) != 0:
        return {"status":"success"}
    return {"status":"failed"}


################################## UTILITY ##################################

def set_current_user_session(account):
    session.clear()
    session['loggedin'] = True
    session['api_key'] = account["api_key"]
    session['id'] = account["id"]
    session['status'] = account["status"]

def check_loggin(strong=False):
    if not strong:
        if "loggedin" in session and session["loggedin"]:
            return True
    else:
        if "loggedin" in session and session["loggedin"]:
            return True



