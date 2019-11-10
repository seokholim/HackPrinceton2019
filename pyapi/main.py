from flask import Flask, request #import main Flask class and request object
from sqlalchemy import create_engine

import requests, googlemaps, json, datetime, os
import datetime as dt
import sqlalchemy as db

app = Flask(__name__) #create the Flask app
gmaps = googlemaps.Client(key='AIzaSyD255iu19fCeI7Tzsz-cWWTmkmXdfmpfOI')

engine = create_engine("postgresql+psycopg2://postgres:Password99@/postgres?host=/cloudsql/hackprinceton-258521:us-east1:hackprinceton") #os.environ['SQLALCHEMY_DATABASE_URI']
connection = engine.connect()
metadata = db.MetaData()
paths = db.Table('paths', metadata, autoload=True, autoload_with=engine)
print(census.columns.keys())

@app.route('/', methods=['GET', 'POST'])
def ReadSMS():
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.json
    phone = request_json['phone']
    num_passengers = request_json['num_passengers']
    start_time = request_json['start_time']
    end_loc = request_json['end_loc']
    start_loc = request_json['start_loc']
    isDriver = request_json['is_driver']

    start_loc = getCordinates(start_loc)
    end_loc = getCordinates(end_loc)
    return pathCalc(phone, start_loc, end_loc, start_time, num_passengers)



def getCordinates(loc):
    geocode_result = geocode_result = gmaps.geocode(loc)
    coordinates = geocode_result[0]["geometry"]["location"]

    return json.dumps(coordinates)

def pathCalc(phone, start, end, time, seats):
    aviable_paths = sqlalchemy.select([paths]).where(census.start_time > DATEADD(hour, -1, time))
    print(aviable_paths)

    return aviable_paths

if __name__ == "__main__":
    app.run(debug=True)
