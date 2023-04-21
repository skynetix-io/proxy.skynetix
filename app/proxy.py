from app import mysql,app
from flaskext.mysql import MySQL
import re,requests,json
from flask import render_template,session,make_response,request,redirect,url_for,Blueprint
from datetime import timedelta


proxy = Blueprint('proxy', __name__,template_folder='templates/proxy',static_folder='static')


@proxy.route('/.well-known/pki-validation/EA0CF13C2FDF500CEDC8E55B263A5409.txt')
def page_not_found():
    return "F9B132B44A7A8D687A32A1158118CC8EAF1E56CFAD0F8AD4CB7448AA8F8C2E52 comodoca.com 6441587cee89d",200

@proxy.route('/404')
def page_not_found():
    return render_template('proxy_404.html'),404

@proxy.route('/<path:path>')
def static_file(path):
    return proxy.send_static_file(path)

@proxy.route('/')
def index():
    return render_template('proxy_index.html',title="Home")

@proxy.route('/contact/')
def contact():
    return render_template('proxy_contact.html')

@proxy.route('/faq/')
def faq():
    return render_template('proxy_faq.html')

@proxy.route('/terms/')
def terms():
    return render_template('proxy_terms.html',title="Terms")

@proxy.route('/refund_policy/')
def rp():
    return render_template('proxy_refund_policy.html',title="Refund")

@proxy.route('/sla/')
def sla():
    return render_template('proxy_sla.html',title="SLA")

@proxy.route('/fup/')
def fup():
    return render_template('proxy_fup.html',title="FUP")

@proxy.route('/residential/')
def residential():
    return render_template('proxy_residential.html')

@proxy.route('/datacenter/')
def datacenter():
    return render_template('proxy_datacenter.html')

@proxy.route('/api/price/' ,  methods=['POST'])
def api_price():
    

    form = request.form
    proxy_type=form["proxy_type"]
    country=form["country"]
    rental_period=form["rental_period"]
    quantity=form["quantity"]


    if quantity=="":
        return {"status":"error","exit":1}
    elif "Select" in proxy_type:
        return {"status":"error","exit":2}
    elif "Select" in country:
        return {"status":"error","exit":3}
    elif "Select" in rental_period:
        return {"status":"error","exit":4}
    

    if "3 days" in rental_period:
        rental_period=3
    elif "1 week" in rental_period:
        rental_period=7
    elif "2 weeks" in rental_period:
        rental_period=14
    elif "1 month" in rental_period:
        rental_period=30
    elif "2 months" in rental_period:
        rental_period=60
    elif "3 months" in rental_period:
        rental_period=90
  
    if "IPV4" in proxy_type:
        proxy_type=4
    elif "IPV6" in proxy_type:
        proxy_type=6
    


    
    req=requests.get(f"https://proxy6.net/api/4cb5b0f5fa-f3835cbb85-781822e7cb/getprice?count={quantity}&period={rental_period}&version={proxy_type}")
    req=req.json()
    req["price"]=round(req["price"]*0.3+req["price"],2)
    req["price_single"]=round(req["price_single"]*0.3+req["price_single"],2)

    return req





    

