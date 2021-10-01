import json
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather, Dial
from twilio import twiml
from twilio.rest import Client



# Importing json data
try:
    with open("creds.json", "r") as f:
        json_data = json.load(f)
        data = json_data[0]
    from_ = data["From"]
    to_ = data["To"]
    ngrok_url = data["ngrok_url"]
    auth_token = data["auth_token"]
    sid = data["Account SID"]
except Exception as e:
    print(e)
    print("A problem occured in exporting json data")
    import sys
    sys.exit()



app = Flask(__name__)



@app.route("/dial", methods=['GET', 'POST'])
def dial():
    """Return TwiML for a moderated conference call."""
    # Start our TwiML response
    resp = VoiceResponse()
    resp.say("I am going to transfer you call now.")
    resp.dial("+919833171351")
    resp.say("Sorry, we will try to reach you later")
    
    # resp.append(dial)
    return str(resp)

@app.route("/hello", methods=['GET', 'POST'])
def hello():
    # Start a TwiML response
    try:
        resp = VoiceResponse()
    except Exception as e:
        print(e)
    try:
        gather = Gather(input='speech', timeout=2 , action='/voice')
        gather.say("Hi This is Sajzad, How are you today?")
        resp.append(gather)
    except Exception as e:
        print(e)
    resp.redirect("/voice")
    return str(resp)
    
client = Client(sid, auth_token)
print(ngrok_url+"/voice")
try:
    call = client.calls.create(
        url =  ngrok_url+"/dial",
        to = to_,
        from_ = from_
    )
except Exception as e:
    print(e)


if __name__ == '__main__':
   app.run(debug=True)