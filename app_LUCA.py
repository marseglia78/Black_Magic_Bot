#Python libraries that we need to import for our bot
import random
from typing import Dict, Any, Union
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
VERIFY_TOKEN='random_demo_token_123'
#ACCESS_TOKEN='EAADJ1Qu6z0ABAJTkKZCdlzxCPbqFFLATsyK968Qo36R7AWHKyn5UTTMnuEqZB1ZBOF8WQXjNMZCHkNE7lxaxm28TuuNHN4GUzugsWIW0ITQFAl82M4lIUo5HujzwwstaeXB05ECXVPOiTHqqppUHk9n2RGyO9CoqpGAY3TI2ZCmGyVWuBTZClZC'
ACCESS_TOKEN='EAAd0fYx51rcBANxZB9zdKQIYxuR3GEPqK60TAefCJ7TiZCsF14pYz4kcaSQgflqum3p5qhdv9qMG2XZAxxec8fCbJ3i7wWq1CbqWBqkz3H2u7cXcUTqtvSZAIdzkFqmAkogiefCgZCAEPxxcqaUkr7hZCZCtGrPOAZCYlCkZCi6vvHgZDZD'

bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/webhook", methods=['GET', 'POST'])
##def receive_message():
#@messenger_app.route('/webhook', methods=['GET', 'POST'])
def listen():

    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        print(request.json)
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        data = request.json
        #print(data)
        recipient_id=data['entry'][0]['messaging'][0]['recipient']['id']
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']
        TEXT = data['entry'][0]['messaging'][0]['message']['text']
        print()
        print('recipient_id ',recipient_id)
        print('sender_id', sender_id, 'wrote: ', TEXT)
        print()

        out_JSON: {"recipient": {"id": sender_id},"message": {"text": "W LA FIGA!"}}
        #print(out_JSON)
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    #print("recipient_id =", recipient_id)
                    if message['message'].get('text'):
                        #print('MESSAGE')
                        #response_sent_text = get_message()
                        response_sent_text = "W LA FIGA!"
                        #print(response_sent_text)
                        send_message(recipient_id, response_sent_text)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)

        #return out_JSON
        return "Message Processed"
    #return '0'


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!",
                        "We're proud of you.",
                        "Keep on being you!",
                        "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #print('send')
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    #out_JSON: {"recipient": {"id": recipient_id}, "message": {"text": "W LA FIGA!"}}
    #bot.send_generic_message(recipient_id,out_JSON)
    return "success"

if __name__ == "__main__":
    app.run()

    #{"object": "page", "entry": [{"messaging": [{"message": "W LA FIGA!"}]}]}