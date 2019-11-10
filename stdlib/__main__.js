const lib = require('lib')({token: process.env.STDLIB_SECRET_TOKEN});
const twilio = require('twilio')
const accountSid = process.env.TWILIO_SID
const authToken = process.env.TWILIO_TOKEN
require('request')
const request = require('request-promise')


/**
* A simple "hello world" function
* @returns {object.http}
*/
module.exports = async (context) => {
  let body = context.params
  let from_number =  body['From']
  let to_number =  body['To']
  let twiml = new twilio.twiml.MessagingResponse();
  if(body['Body'].trim() == 'Okay, will do' || body['Body'].trim() == 'will do') {
    twiml.message(`Your ride is confirmed.`)
  } else {
    await lib({bg: true})[`${context.service.identifier}.processor`]({body: body['Body'], from: to_number, to: from_number})
    twiml.message(`We're processing your request...`)
  }
  
  return {
    headers: {'Content-Type': 'text/xml'},
    statusCode: 200,
    body: twiml.toString()
  };
};
