import requests

def ReadSMS(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    phone = request_json['phone']
    message = request_json['message']
    message = body.message.split(";")
    start_time = message[3]
    end_loc = message[2]
    start_loc = message[1]

    isDriver = 'true' if message[0] == "D" else 'false'

    start_loc = getCordinates(start_loc)
    end_loc = getCordinates(end_loc)


def getCordinates(loc):
    url = 'https://maps.googleapis.com/maps/api/geocode?key=AIzaSyD255iu19fCeI7Tzsz-cWWTmkmXdfmpfOI'
    params = dict(
    address=loc
    )
    resp = requests.get(url=url, params=params)
    return resp.json()


def hello_world(request):
  # Add Rider and Driver to Pairing
  # Increase Booked Spots +1
  # Send SMS Booked Ride
