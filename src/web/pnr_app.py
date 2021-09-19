"""
- Missing PNR Detector -

This is the implementation of the system for the detection of missing PNR-s. PNR is a record locator
that consists of 6 (six) symbols: letters A-Z and numbers 1-9. Next PNR is determined by
incrementing the previous one.
Here are some examples:
● Current PNR: AAAAAA ; Next PNR: AAAAAB
● Current PNR: AAAAAZ ; Next PNR: AAAAB1
● Current PNR: AAAAA9 ; Next PNR: AAAAAA
We need to find all missing PNRs between the two given ones. If we have the last PNR in our
system AAAAAA, and we receive a new one AAAAAD, our system will need to detect
AAAAAB and AAAAAC as the missing PNRs.
"""

from flask import Flask, jsonify, request 
from flask_restful import Api, Resource
from pymongo import MongoClient


app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")

db = client.MissingPNRs
pnr_col  = db["PNR"]


pnr_col.insert_one({
    "PNR1": 'AAAAAA',
    "PNR2": 'AAAAAA',
    "Missing PNR-s": []
})


def errorMessage(status, message):
    return {
        "status": status,
        "message": message
    }


class FindMissing(Resource):
    def post(self):
        postedData = request.get_json()

        if "PNR1" not in postedData or "PNR2" not in postedData:
            retJson = errorMessage(301, "Not enough parameters. PNR1 and PNR2 required.")
            return jsonify(retJson)


        pnr1 = postedData['PNR1']
        pnr2 = postedData['PNR2']

        symbols = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" #35 symbols
        missing_pnrs = []

        if len(pnr1) != 6 or len(pnr2) != 6:
            retJson = errorMessage(302, "Wrong input, PNR-s must have the length of 6 (six) characters.")
            return jsonify(retJson)
        
        for char in (pnr1+pnr2):
            if char not in symbols:
                retJson = errorMessage(303, "Wrong input, PNR-s can have symbols: letters A-Z and numbers 1-9.")
                return jsonify(retJson)


        # large positive 35-based number to int
        def to_decimal(n):
            n_10 = 0
            for i in range(len(n)):
                n_10 += symbols.index(n[-1-i])*35**i
            return n_10

        # large positive int to 35-based number
        def to_35based(n):
            if n < 35:
                return '' + symbols[n % 35]
            else:
                return to_35based(n // 35) + symbols[n % 35]
                
        pnr1_dec = to_decimal(pnr1)
        pnr2_dec = to_decimal(pnr2)

        for i in range(pnr1_dec+1, pnr2_dec):
            missing_pnrs.append(to_35based(i))
        print(missing_pnrs)

        pnr_col.update_one({}, {
            "$set": {
                "PNR1": pnr1,
                "PNR2": pnr2,
                "Missing PNR-s": missing_pnrs
            }
        })

        retJson = {
            "status": 200,
            "Missing PNR-s": missing_pnrs,
            "message": "Missing PNR-s detected successfully."
        }
        return jsonify(retJson)


class GetMissing(Resource):
    def get(self):
        pnr1 = pnr_col.find({})[0]["PNR1"]
        pnr2 = pnr_col.find({})[0]["PNR2"]
        missing_pnrs = pnr_col.find({})[0]["Missing PNR-s"]
        retJson = {
            "status": 200,
            "PNR1": pnr1,
            "PNR2": pnr2,
            "missing PNR-s": missing_pnrs,
            "message": "Missing PNR-s retrieved successfully."
        }
        return jsonify(retJson)


api.add_resource(FindMissing, '/detect')
api.add_resource(GetMissing, '/get')


if __name__ == "__main__":
    app.run(host='0.0.0.0')