from flask import Flask
from flask import request
from flask import make_response
import datetime
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "hello world"

@app.route("/alexa_end_point",methods=['POST'])
def alexa():
    event= request.get_json
    req = event['request']

    if req['type'] == 'LaunchRequest':
        return handle_launch_request()
        
    elif req['type'] == 'IntentRequest':

        if req['intent'] == 'Hello Intent':
            return handle_hello_intent(req)
        else:
            return "",400 

    elif req['type'] == 'SessionEndedRequest':
        pass

def handle_hello_intent(req):
    name = req['intent']['slots']['FirstName']['value']
    res = Response()
    res.speech_text = 'Hello <say-as interpret-as="spell-out">{0}.'.format(name)
    res.speech_text += get_wish()
    return res.build_response()

def get_wish():
    'return good morning/afternoon/evening depending on time of the day'
    current_time = datetime.datetime.utc()
    hours = current_time.hour-1
    if hours < 0:
        hours = 24+hours
    if hours < 12:
        return 'Good morning'
    elif hours < 18:
         return 'good afertnoon.'
    else:
        return 'good evening.'

def handle_launch_request():
    'Hendles lanch request and generates response'
    res = Response()
    res.speech_text = "Welcome to greetings skill. Using our skill you can greet your guests."
    res.reprompt_text = 'Whom you want to greet? you can say for example, say hello to john'
    return res.build_response()


class Response(object):
    'Alexa skill response object with helper functions'

    def __init__(self):
        self.speech_text = None
        self.reprompt_text = None
        self.end_session = True
    
    def build_response(self):
        'Builds alexa response and returns'

        fnl_response = {
            'version':'1.0',
            'response': {
                'outputSeech' : {
                    'type': 'SSML',
                    'ssml': '<speak>'+self.speech_text+'</speak>'
                },
                'shouldEndSession': self.end_session
                }
            }

        if self.reprompt_text:
            fnl_response['response']['repromt.text'] = {
                'outputSeech': {
                    'type': 'SSML',
                    'ssml': '<speak>'+self.reprompt_text+'</speak>'

        }
    }

        http_response = make_response(json.dumps(fnl_response))
        http_response.headers['Content_Type'] = 'application/json'
        return http_response

if __name__ == "__main__":
    app.run()