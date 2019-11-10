//Load HTTP module
const http = require("http");
const hostname = '127.0.0.1';
const port = 3000;

//Create HTTP server and listen on port 3000 for requests
const server = http.createServer((req, res) => {

  let buffers = [];

  req.on('data', chunk => {
    buffers.push(chunk);
  });

  req.on('end', () => {
    //Set the response HTTP header with HTTP status and Content type
    let obj = new Object();
    // console.log('this is the req', req);
    let body = JSON.parse(Buffer.concat(buffers).toString());
    console.log(body);

    let phone = body.phone;
    let message = body.message.split(";");
    let start_time = message[3];
    obj.end_loc = message[2];
    obj.start_loc = message[1];
    let isDriver = message[0] == "D" ? true : false;

    // TODO
    obj.end_loc = getCordinates(obj.end_loc);
    obj.start_loc = getCordinates(obj.start_loc);

    res.status(200).json(JSON.stringify(obj));

  });


});

//listen for request on port 3000, and as a callback function have the port listened on logged
server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});


/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */
exports.readSMS = (req, res) => {

};

function getCordinates(loc){
  
  const https = require('https');

https.get('https://maps.googleapis.com/maps/api/geocode?key=AIzaSyD255iu19fCeI7Tzsz-cWWTmkmXdfmpfOI', (resp) => {
  let data = '';

  // A chunk of data has been recieved.
  resp.on('data', (loc) => {
    data += loc;
  });

  // The whole response has been received. Print out the result.
  resp.on('end', () => {
    console.log(JSON.parse(data).explanation);
    return data;
  });

}).on("error", (err) => {
  console.log("Error: " + err.message);
});

}

exports.ConfirmationRide = (req, res) => {
  // Add Rider and Driver to Pairing
  // Increase Booked Spots +1
  // Send SMS Booked Ride
};
