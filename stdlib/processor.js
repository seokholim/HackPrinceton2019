const twilio = require('twilio')
const accountSid = process.env.TWILIO_SID
const authToken = process.env.TWILIO_TOKEN
const client = twilio(accountSid, authToken)
const request = require('request')

const admin = require('firebase-admin')
let serviceAccount = require('../hackprinceton2019f-1981dbe82d65.json')

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
})

let db = admin.firestore()

function proposeDrivers (params) {
  return [
    {
      name: "Mark",
      from: params.location_from,
      to: params.location_to,
      timestamp: params.timestamp - 1200,
      emptySeats: params.spot,
      number: "+14168369632"
    },
    {
      name: "Nancy",
      from: params.location_from,
      to: params.location_to,
      timestamp: params.timestamp + 2400,
      emptySeats: parseInt(params.spot, 10) + 2,
      number: "+16099375386"
    },
    {
      name: "Jonathan",
      from: params.location_from,
      to: params.location_to,
      timestamp: params.timestamp + 600,
      emptySeats: parseInt(params.spot, 10) + 1,
      number: "+16084213961"
    }
  ]
}

function updateStateToChoosing (number, drivers) {
  let docRef = db.collection('userStates').doc(number);
  let setRef = docRef.set({
    number: number,
    state: 'choosingDriver',
    drivers: drivers
  });
}

function convertTime(timestamp) {
  var date = new Date(timestamp*1000)
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  var year = date.getFullYear()
  var month = months[date.getMonth()]
  var day = date.getDate()
  var hours = date.getHours()
  var minutes = "0" + date.getMinutes()
  var seconds = "0" + date.getSeconds()
  return month + ' ' + year + ' ' + hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2)
}

module.exports = (to, from, body, context, callback) => {
  let docsRef = db.collection('userStates')
  let userStateQuery = docsRef.where('number', '==', to).get().then(snapshot => {
    if (snapshot.empty || snapshot.docs[0].data().state != 'choosingDriver') {
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
          let original_location = body.location_from.trim()
          if (original_location == 'Rutgers') {
            body.location_from = 'Princeton'
          }
          drivers = proposeDrivers(body)
          if(original_location != 'Drexel' && original_location != 'UPenn') {
            updateStateToChoosing(to, drivers)
          } 
          messages = drivers.map(function(driver, index){
            return `${index + 1}: ${driver.name}\nFrom ${driver.from} To ${driver.to}\nAt ${convertTime(parseInt(driver.timestamp, 10))}\n${driver.emptySeats} empty seats`
          })
          if (original_location == 'Drexel') {
            message = `We're sorry, but no one is driving from ${body.location_from} to ${body.location_to}`
          } else if (original_location == 'Rutgers') {
            message = "We did not find an exact match but you can take NJT to Princeton and ride there.\nAvailable drivers:\n" + messages.join('\n\n') + "\n\nPlease choose a driver by number"
          } else if (original_location == 'UPenn') {
            message = `No direct route to ${body.location_to}, but John stops in NYC + you can then ride with Steve all the way up.`
          } else {
            message = "\n Available drivers:\n" + messages.join('\n\n') + "\n\nPlease choose a driver by number"
          }
          //message = `From ${body.location_from} to ${body.location_to} at ${body.timestamp}, ${body.spot} seats are needed.`
        }
        client.messages
          .create({body: message, from: from, to: to})
          .then( (_) => callback(null, 'Sent'))
      })
    } else {
      let index = Number(body) - 1
      var message
      let user = snapshot.docs[0].data()
      let drivers = user.drivers
      if(isNaN(index)) {
        message = `We're sorry, we couldn't parse your request`
      } else if(index < 0 || index >= drivers.length) {
        message = `There is no such driver`
      } else {
        let driver = drivers[index]
        let message_to_driver = `Hey, one user wants to ride your car. His/Her number is ${user.number}. Please talk about the details of your trip.`
        client.messages.create({body: message_to_driver, from: from, to: driver.number})
        let docRef = db.collection('userStates').doc(to);
        docRef.set({
          number: to,
          state: 'lookingForDriver'
        });
        message = `You chose ${driver.name}! His/Her number is ${driver.number}. Please talk about the details of your trip.`
      }
      client.messages
        .create({body: message, from: from, to: to})
        .then( (_) => callback(null, 'Sent'))
    }
  })
};
