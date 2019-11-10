from flask import Flask, request #import main Flask class and request object
from sqlalchemy import create_engine, text

import requests, googlemaps, json, os
import sqlalchemy as db
from datetime import datetime, timedelta
import time

app = Flask(__name__) #create the Flask app
gmaps = googlemaps.Client(key='AIzaSyD255iu19fCeI7Tzsz-cWWTmkmXdfmpfOI')

engine = create_engine("postgresql+psycopg2://postgres:Password99@/postgres?host=/cloudsql/hackprinceton-258521:us-east1:hackprinceton") #os.environ['SQLALCHEMY_DATABASE_URI']
connection = engine.connect()
metadata = db.MetaData()
paths = db.Table('paths', metadata, autoload=True, autoload_with=engine)
print(paths.columns.keys())

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
    geocode_result = gmaps.geocode(loc)
    coordinates = geocode_result[0]["geometry"]["location"]

    return coordinates

def pathCalc(phone, start, end, time, seats):
    timesub1h = datetime.strptime(time,'%Y-%m-%d %H:%M') - timedelta(hours=1)
    timeadd1h = datetime.strptime(time,'%Y-%m-%d %H:%M') + timedelta(hours=1)

    QUERY = """SELECT path_id, start_lat, start_log, end_lat, end_log, start_time FROM paths WHERE start_time > :timesub1h AND start_time < :timeadd1h ORDER BY (POW((start_log-:s_lng),2) + POW((start_lat-:s_lat),2)) + (POW((end_log-:e_lng),2) + POW((end_lat-:e_lat),2)) LIMIT 1"""

    ResultProxy = connection.execute(text(QUERY), timesub1h=timesub1h, timeadd1h=timeadd1h, s_lng=start['lng'], s_lat=start['lat'], e_lng=end['lng'], e_lat=end['lat'])

    ResultSet = ResultProxy.fetchall()
    # time.sleep(2)

    #directions_result = gmaps.directions('{' + str(start['lat']) + ',' + str(start['lng']) + '}', '{' + str(ResultSet[0][1]) + ',' + str(ResultSet[0][2]) + '}' ,mode="transit",arrival_time=ResultSet[0][5])

    #print(str(directions_result))
    return str(ResultSet[0])

if __name__ == "__main__":
    app.run(debug=True)
