#Python libraries that we need to import for our bot
import random
import os
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

#VERIFY_TOKEN='random_demo_token_123'
#ACCESS_TOKEN='EAAd0fYx51rcBANxZB9zdKQIYxuR3GEPqK60TAefCJ7TiZCsF14pYz4kcaSQgflqum3p5qhdv9qMG2XZAxxec8fCbJ3i7wWq1CbqWBqkz3H2u7cXcUTqtvSZAIdzkFqmAkogiefCgZCAEPxxcqaUkr7hZCZCtGrPOAZCYlCkZCi6vvHgZDZD'
bot = Bot(ACCESS_TOKEN)

#'''
@app.route("/", methods=['GET', 'POST'])
def receive_message_check():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        #return verify_fb_token(token_sent)
        return "your app is succesfully deployed"

    else:
        data = request.json
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']
        send_message(sender_id, "your app is succesfully deployed")
    return "Message Processed"
#'''

##We will receive messages that Facebook sends our bot at this endpoint
@app.route("/webhook", methods=['GET', 'POST'])
#@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
       # get whatever message a user sent the bot
       output = request.get_json()
       data = request.json

       recipient_id = data['entry'][0]['messaging'][0]['recipient']['id']
       sender_id = data['entry'][0]['messaging'][0]['sender']['id']
       #send_message(sender_id, "PHARMACY? yes/no")
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                if message['message'].get('text'):

                    text=data['entry'][0]['messaging'][0]['message']['text']
                    #out_text=get_message2(text)
                    print(text)
                    #response_sent_text = get_message()
                    #send_message(sender_id, response_sent_text)
                    send_message(sender_id, text)

                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

'''
def get_message2(text):
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)
'''
#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()