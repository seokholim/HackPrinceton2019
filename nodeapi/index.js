/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */
exports.readSMS = (req, res) => {
  let obj = new Object();

  let phone = req.body.phone;
  let message = req.body.message.split(";");
  let start_time = message.pop();
  obj.end_loc = message.pop();
  obj.start_loc = message.pop();
  let isDriver = message.pop() == "D" ? true : false;

  // TODO
  obj.end_loc = getCordinates(end_loc);
  obj.start_loc = getCordinates(start_loc);

  res.status(200).json(JSON.stringify(obj));
};

function getCordinates(loc){

  var request = new XMLHttpRequest()

  // Open a new connection, using the GET request on the URL endpoint
  request.open('POST', 'https://maps.googleapis.com/maps/api/geocode', true)

  request.onload = function() {
    // Begin accessing JSON data here
    address : loc
    key : 'AIzaSyD255iu19fCeI7Tzsz-cWWTmkmXdfmpfOI'
  }

  // Send request
  request.send()
  return request;
}

exports.ConfirmationRide = (req, res) => {
  // Add Rider and Driver to Pairing
  // Increase Booked Spots +1
  // Send SMS Booked Ride
};
