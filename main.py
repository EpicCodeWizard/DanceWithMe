from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask import *
import wikipediaapi
import requests
import os

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

app = Flask(__name__)

def onmsg(msg):
  search = msg.split(": ")[-1]
  params = {'action': 'query', 'format': 'json', 'list': 'search', 'utf8': 1, 'srsearch': search}
  resp = requests.get('https://en.wikipedia.org/w/api.php', params=params)
  return wikipediaapi.Wikipedia('en').page(resp.json()['query']['search'][0]['title']).summary

@app.route("/sms", methods=['POST'])
def sms_reply():
  resp = MessagingResponse()
  resp.message(body=onmsg(str(dict(request.form)['Body'])))
  return str(resp)

app.run(host="0.0.0.0")
