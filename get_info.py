import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import dateparser
import dateutil
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

stop_words = set(stopwords.words('english')) 
  
stop_words.remove('at')
stop_words.remove('to')
stop_words.remove('from')

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    
    filtered_sentence = [w for w in sent if not w in stop_words] 
    filtered_sentence = [] 
    for w in sent: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
    sent = nltk.pos_tag(filtered_sentence)
    return sent

def parse_date(word):
    hiyo = dateparser.parse(word)
    return hiyo

def get_info(sent):
    loc_from = []
    loc_to = []
    loc_from_recorded = False
    loc_to_recorded = False
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
        if (pair[0] != 'from' or pair[1] != 'TO') and (pair[1] != 'NNP'):
            current_loc = False
            
        if (pair[0] == 'from'):
            loc_from_recorded = True
            loc_to_recorded = False
            current_loc = True
            time_done = True
            print('from word')
            
        if (pair[1] == 'TO'):
            loc_to_recorded = True
            loc_from_recorded = False
            current_loc = True
            time_done = True
            print('to word')
            
        if (pair[1] == 'NNP') and current_loc == True and time_done == True:
            time_done = True
            if loc_from_recorded == False and loc_to_recorded == True:
                loc_to.append(pair[0])
                print('from')
                print(loc_from_recorded,loc_to_recorded)
                
            elif loc_to_recorded == False and loc_from_recorded == True:            
                loc_from.append(pair[0])
                print('to')
                print(loc_from_recorded,loc_to_recorded)            
            
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
            

    time_str = ''
    for eachtok in time:
        time_str = time_str + ' ' + eachtok

    print(time_str)
    
    this_time = parse_date(time_str)
    if not (this_time):
        timestampStr = None
    else:
        timestampStr = this_time.strftime("%m-%d,%H:%M")

    for each_tok in loc_from:
        location_from = location_from + each_tok + ' ' 

    for each_tok in loc_to:
        location_to = location_to + each_tok + ' ' 

    return location_to, location_from, timestampStr, spot





