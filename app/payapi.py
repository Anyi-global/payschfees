from app import app, mongo, api
import re, time, datetime, uuid, os
from flask import request, jsonify
from flask_restful import Resource, Api, reqparse
from app.view import nigerian_time


#api that saves payment details and generates reference number
class PaymentDetails(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('registration_id', 
                        type=str,
                        required=True, 
                        help="Enter registration ID. Field cannot be left blank")

    parser.add_argument('frequency', 
                        type=str,
                        required=True, 
                        help="Example 'Termly'. Field cannot be left blank")

    parser.add_argument('fees_to_pay',
                        action='append',
                        required=True, 
                        help="Fees to pay. Field cannot be left blank")

    def post(self):
        data = PaymentDetails.parser.parse_args()

        # check if the length of registration_id is upto 10 digits
        if len(data['registration_id']) != 10 or len(''.join(i for i in data['registration_id'] if i.isdigit())) != 10:
            return {"status":False, "message":"Registration number must be 10 digits"}, 404
        
        _id= data["registration_id"]
        freq= data["frequency"]
        fees= data["fees_to_pay"]

        # print(fees)

        #generete 10 digit ref no
        ref  = str(uuid.uuid4().int)[:10]

        #send the data to database
        mongo.db.payfees.insert({"registration_id":_id, "frequency":freq, "fees":fees, "ref":ref, "date":nigerian_time()})

        #return sucess status
        msg = "Data recorded. Your reference number is {}".format(ref)
        return {"status":True, "message":msg, "data":ref}, 200

    
    def get(self):
        #get all the data in the database
        getall = mongo.db.payfees.find({}, {"_id":0})
        result = []
        for element in getall:
            result.append(element)
        if result == []:
            return {"message":'Oops! no recorded information yet.'}, 200
            
        return {"status":True, "message":'data retrieved', "data":result}, 200

api.add_resource(PaymentDetails, '/api/payfees')


class GetOneRecord(Resource):
    def get(self, reference):
        #get all the data in the database
        getone = mongo.db.payfees.find_one({"ref":reference}, {"_id":0})
        if not getone:
            return {"message":'No record found for the user'}, 200
            
        return {"status":True, "message":'data retrieved', "data":getone}, 200


    def put(self, reference):
        #get all the data in the database
        getone = mongo.db.payfees.update_one({"ref":reference}, {'$set': {"date":nigerian_time(), "frequency":"fine"}})
        if not getone:
            return {"message":'No record found for the user'}, 200
            
        return {"status":True, "message":'data updated successfully'}, 200

api.add_resource(GetOneRecord, '/api/payfees/<string:reference>')