import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from flask import jsonify
import dateparser
import dateutil

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def parse_date(word):
    hiyo = dateparser.parse(word)
    return hiyo

def get_info(sent):
    loc_from = []
    loc_to = []
    loc_from_recorded = False
    time = []
    prev = ''
    spot = 0
    pre_val = 0
    time_done = True
    location_from = ''
    location_to = ''
    current_loc = False

    sent = preprocess(sent)
    
    for pair in sent:

        if (pair[1] == 'NNP') and loc_from_recorded == False:
            current_loc = True
            loc_from.append(pair[0])
            print(pair[0])

        if pair[0] == ',':
            time_done = True
            print(pair[0])

        if pair[1] == 'CD' and time_done == True:
            spot = pair[0]
            print(pair[0])
            
        if pair[0] == 'at' or pair[0] == 'on' or pair[0] == 'around':
            time.append(pair[0])
            time_done = False
            print(pair[0])
            
        elif len(time) != 0 and time_done == False:
            time.append(pair[0])
            print(pair[0])
            
        elif (pair[1] == 'IN' or pair[1] == 'TO') and current_loc == True:
            loc_from_recorded = True
            current_loc = False
            print('here')

        elif (pair[1] == 'NNP' or pair[1] == 'NN') and loc_from_recorded == True:
            loc_to.append(pair[0])
            print(pair[0])

    time_str = ''
    for eachtok in time:
        time_str = time_str + ' ' + eachtok

    this_time = parse_date(time_str)
    timestampStr = this_time.strftime("%m-%d,%H:%M")

    for each_tok in loc_from:
        location_from = location_from + each_tok + ' ' 

    for each_tok in loc_to:
        location_to = location_to + each_tok + ' ' 

    return location_to, location_from, timestampStr, spot

def main(request):
    request_json = request.get_json()
    order_sent = request_json['order']
    location_to, location_from, timestampStr, spot = get_info(order_sent)
    return jsonify({
        'location_to': location_to,
        'location_from': location_from,
        'timestamp': timestampStr,
        'spot': spot
    })



