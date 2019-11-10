const twilio = require('twilio')
const accountSid = process.env.TWILIO_SID
const authToken = process.env.TWILIO_TOKEN
const client = twilio(accountSid, authToken)
const request = require('request')

module.exports = (to, from, body, context, callback) => {
  request.post({
    url: "https://us-central1-hackprinceton2019f.cloudfunctions.net/language-processing",
    headers: {
      "content-type": "application/json"
    },
    json: {order: body},
    timeout: 10000
  }, function (error, response, body){
    var message
    if(response.statusCode >= 400) {
      message = `We're sorry, we couldn't parse your request`
    } else {
      message = `From ${body.location_from} to ${body.location_to} at ${body.timestamp}, ${body.spot} seats are needed.`
    }
    client.messages
      .create({body: message, from: from, to: to})
      .then( (_) => callback(null, 'Sent'))
  })
};
