#####################################################################################
########################  THIS FILE(view.py) CONTAINS THE USER INTERFACE  ################################################
#######################################################################################

from app import app, mongo #this means from the app folder(which calls on the __init__.py file in the app folder) import the flask init(i.e app = Flask(__name__)) 
import re, time, datetime, uuid, os
from flask import request, render_template, flash, redirect, url_for, session,logging 
from passlib.hash import sha256_crypt
from functools import wraps
import requests, json



app.secret_key = os.urandom(24)

# #CHECK IF USER IS LOGGED IN (DECORATOR)
# def is_logged_in(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         # if "email" in session == "emeka@gmail.com":
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             flash('Unauthorized, Please login','danger')
#             return redirect(url_for("login"))
#     return wrap

#####################################################################################
########################   FUNCTION  ################################################
#######################################################################################
#displays year
year = datetime.date.today().year

#function that displays Nigerian time.
def nigerian_time():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    today = datetime.date.today()
    d2 = today.strftime("%B %d, %Y")
    tm = now.strftime("%H:%M:%S")
    return (d2 +' '+'at'+' '+tm)


#####################################################################################
########################   ENDPOINTS  ################################################
#######################################################################################
#homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method=='POST':
        #get form fields
        reg_id=request.form['registration_id']
        print(reg_id)
        frequency=request.form['frequency']
        print(frequency)
        fees_to_pay=request.form.getlist('fees_to_pay', type=str)
        print(fees_to_pay)
     
        #call the api to save the data
        payload = {
            'registration_id':reg_id,
            'frequency':frequency,
            'fees_to_pay':fees_to_pay
        }

        # try:
        res = requests.post('anyidev.herokuapp.com/api/payfees', json=payload)
        response = res.json()
        # except Exception as e:
        #     flash(e, "danger")
        #     return render_template("index.html", title="Home | Pay School Fees", home="active", year=year)

        print(response)

        #if the api status is FALSE
        if not response["status"]:
            flash(response["message"], "danger")
            return render_template("index.html", title="Home | Pay School Fees", home="active", year=year)
        
        #if the api status is TRUE
        flash(response["message"], "success")
        return redirect("/checkout/{}".format(response["data"]))

    #if the method is GET
    else:
        return render_template("index.html", title="Home | Pay School Fees", home="active", year=year)




@app.route("/checkout/<string:ref>", methods=["GET", "POST"])
def checkout(ref):
    if request.method=='POST':
        flash("Your record is confirmed", "success")
        return render_template("index.html", title="Home | Pay School Fees", home="active", year=year)
        
    #if the method is GET
    else:
        try:
            res = requests.get('anyidev.herokuapp.com/api/payfees/{}'.format(ref))
            response = res.json()
        except Exception as e:
            flash(e, "danger")
            return render_template("index.html", title="Home | Pay School Fees", home="active", year=year)
        
        if not response["status"]:
            flash(response["message"], "danger")
            return render_template("index.html", title="Home | Pay School Fees", home="active", year=year)
        
        data = response["data"]
        length = len(response["data"]["fees"])
        return render_template("checkout.html", title="Checkout | Pay School Fees", data=data, length=length, year=year)
