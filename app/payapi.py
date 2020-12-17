#####################################################################################
########################  THIS FILE(view.py) CONTAINS THE USER INTERFACE  ################################################
#######################################################################################

from app import app, mongo, api #this means from the app folder(which calls on the __init__.py file in the app folder) import the flask init(i.e app = Flask(__name__)) 
import re, time, datetime, uuid, os
from flask import request, jsonify
from flask_restful import Resource, Api, reqparse 
from app.view import nigerian_time

#api that saves payment details and generates reference number
class PaymentDetails(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("reg_id",
                        type=str,
                        required=True,
                        help="Enter Registration ID. Field cannot be blank")


    parser.add_argument("frequency",
                        type=str,
                        required=True,
                        help="Example 'Termly'. Field cannot be blank")

    parser.add_argument("fees_to_pay",
                        type=str,
                        required=True,
                        help="Fees to pay. Field cannot be blank")

    def post(self):
        data = PaymentDetails.parser.parse_args()

        #check if the lenght of the reg_id is up to ten
        if len(data ['reg_id']) !=10 or len('.join'(i for i in data['reg_id'] if i.isdigits())) !=10:
            return{"status":False, "message":"Registration number must be 10 digits"}, 404
        
        #fields to be collected
        _id = data["reg_id"]
        freq = data["frequency"] 
        fees = data["fees_to_pay"]

        #generate ten digit ref_number
        reference = str(uuid.uuid4().int)[:10]

        #send the data to db
        mongo.db.payfees.insert({'reg_id':_id, 'frequency':freq, 'fees_to_pay':fees, 'ref':ref, 'date':nigerian_time})

        #returrn success status
        msg = 'Registration successful. Your refrence number is {}'.format(ref)
        return {'status':True, 'message':msg, 'data':ref}, 200

api.add_resource(PaymentDetails, '/api/payfees') 


