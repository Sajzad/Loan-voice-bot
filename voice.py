import json
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio import twiml
from twilio.rest import Client
# from gmail import send_mail
import pandas as pd



print("call initiated")
n = 0
q_repeat = 0
repeat = False
recheck_repeat = 0
payable = True
texts = [   "Excuse me? i didn't get you. Could you say one more time please?",
            "Beg your pardon?, Would you mind repeating that?",
            "Sorry?, Could you say that again, please?",
            "I can’t hear your voice… Can you say it in another way, please?"
    ]

# Importing json data
try:
    with open("conversation.json", "r") as f:
        use_case = json.load(f)
    bot_resp = use_case['intro']

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


@app.route("/hello", methods=['GET', 'POST'])
def hello():
    # Start a TwiML response
    try:
        resp = VoiceResponse()
    except Exception as e:
        print(e)
    try:
        gather = Gather(input='speech', timeout=1 , action='/voice')
        resp.redirect('/voice')
        resp.append(gather)
    except Exception as e:
        print(e)
    return str(resp)

@app.route("/voice", methods=['GET', 'POST'])
def voice():

    global bot_resp
    global n
    global names

    try:
        with open("count.txt", 'r') as f:
            count = int(f.read(f.read()).strip())
            print(count)
    except Exception as e:
        print(e)

    try:
        resp = VoiceResponse()
    except Exception as e:
        print(e)
    try:
        name = names[count]
    except:
        resp.hangup()   
    try:
        gather = Gather(input='speech', speech_timeout=2, action='/check_usecase')
    except Exception as e:
        print(e)
    if n==0:
        bot_resp = bot_resp[n]+"{}".format(name)
    elif n == 1:
        bot_resp = bot_resp[n] + "Dated {}, For your personal load from us. Yes?".format(due)
    b_resp = bot_resp[n]
    gather.say(b_resp, voice="man", language="en")
    resp.append(gather)
    resp.redirect('/recheck')
    return str(resp)

@app.route('/check_usecase', methods=['GET', 'POST'])
def check_usecase():
    """To check which use case is going to be initiated. Processes results from the <Gather> prompt in /voice"""
    global n
    global data
    global bot_resp
    global q_repeat
    global conv_1_1
    global conv_1_2
    global conv_1_3
    global conv_1_4
    global conv_2_1
    global conv_2_2
    global conv_3_1

    global texts
    global recheck_repeat
    # To check whether 'no' is replied twice
    global repeat

    recheck_repeat = 0
    resp = VoiceResponse()
    resp.hangup()
    # print(request.values)
    if 'SpeechResult' in request.values:
        choice = request.values['SpeechResult']
        choice = choice.lower()
        print(choice)
        if choice:
            if n==0:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/voice')
                    return str(resp)

                for i in conv_1_1:
                    if str(i) in choice:
                        for i in conv_1_6:
                            if str(i) in choice:
                                n+=1
                                text = "I am doing great! Thank you for asking."
                                print(text)
                                resp.say(text, voice='woman', language='en')
                                resp.redirect("/voice")
                                return str(resp)  
                            else:
                                continue
                    else:
                        continue                             
                for i in conv_1_2:
                    if str(i) in choice:
                        text = "My name is Neha from No Cost"
                        resp.say(text, voice='woman', language='en')
                        resp.redirect("/test")
                        return str(resp)  
                    else:
                        continue                
                for i in conv_1_3:
                    if str(i) in choice:
                        text = "I am doing great! Thank you for asking."
                        resp.say(text, voice='woman', language='en')
                        resp.redirect("/voice")
                        return str(resp)  
                    else:
                        continue                
                for i in conv_1_4:
                    if str(i) in choice:
                        bot_resp = use_case["use_case_5"]
                        resp.redirect("/use_case_5")
                        return str(resp)  
                    else:
                        continue
                # If no match found  
                text = texts[q_repeat]
                q_repeat += 1
                if q_repeat == 4:
                    q_repeat = 0
                resp.say(text, voice='woman', language='en')
                resp.redirect("/test")
                return str(resp)
            elif n==1:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/voice')
                    return str(resp)
                for i in conv_2_1:
                    if str(i) in choice:
                        n+=1
                        text = "Thank you"
                        resp.say(text, voice='woman', language='en')
                        resp.redirect('/voice')
                        return str(resp)
                    else:
                        continue                  
                for i in conv_2_2:
                    if str(i) in choice:
                        n = 0
                        bot_resp = use_case["use_case_3"]
                        resp.redirect('/use_case_3')
                        return str(resp)
                    else:
                        continue                  
                for i in conv_2_3:
                    if str(i) in choice:
                        n = 0
                        bot_resp = use_case["use_case_4"]
                        resp.redirect('/use_case_4')
                        return str(resp)
                    else:
                        continue                  

                text = texts[q_repeat]
                q_repeat += 1
                if q_repeat == 4:
                    q_repeat = 0
                resp.say(text, voice='woman', language='en')
                resp.redirect("/test")
                return str(resp)
            elif n==2:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/voice')
                    return str(resp)
                for i in conv_3_1:
                    if str(i) in choice:
                        n = 0
                        bot_resp = use_case["use_case_1"]
                        resp.redirect('/use_case_1')
                        return str(resp)
                    else:
                        continue                   
                for i in conv_3_2:
                    if str(i) in choice:
                        n = 0
                        bot_resp = use_case["use_case_2"]
                        resp.redirect('/use_case_2')
                        return str(resp)
                    else:
                        continue                                 

                text = texts[q_repeat]
                q_repeat += 1
                if q_repeat == 4:
                    q_repeat = 0
                resp.say(text, voice='woman', language='en')
                resp.redirect("/test")
                return str(resp)
@app.route("/use_case", methods=['GET', 'POST'])
def use_case():
    """ prompted right after check_usecase function 
        bot_resp will be chunked as per use_case from conversation.json
    """
    # Start a TwiML response
    global bot_resp
    global due_charges
    global bounce_charges
    global dues
    global emis
    global n
    global payable

    bounce = bounce_charges[n]
    due_charge = due_charges[n]
    due = dues[n]
    emi = emis[n]
    if payable:
        text = "You total payable is {} rupees. E.M.I. {} with Bounce charge {} with over due charge of {}. The amount \
        you pay, you will be getting an e-receipt.".format(due, emi, bounce, due_charge)
        payable = False
    else:
        text = bot_resp[n]
    try:
        resp = VoiceResponse()
    except Exception as e:
        print(e)
    text = bot_resp[n]
    try:
        gather = Gather(input='speech', timeout=2 , action='/check_usecase')
        gather.say(text, voice="man", language="en")
        resp.append(gather)
    except Exception as e:
        print(e)
    return str(resp)

@app.route('/use_case_5', methods=['GET', 'POST'])
def use_case_5():
    """Processes results from the <Gather> prompt in /voice"""
    global n
    global data
    global bot_resp
    global q_repeat   
    global conv_8_1
    global conv_8_2
    global conv_8_3
    global conv_8_4
    global texts
    global recheck_repeat
    global payable
    # To check whether 'no' is replied twice
    global repeat

    recheck_repeat = 0
    resp = VoiceResponse()
    resp.hangup()
    # print(request.values)
    if 'SpeechResult' in request.values:
        choice = request.values['SpeechResult']
        choice = choice.lower()
        print(choice)
        if choice:
            if n == 0:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/use_case')
                    return str(resp)
                for i in conv_8_1:
                    if str(i) in choice:
                        n +=1
                        resp.redirect("/use_case")
                        return str(resp)
                    else:
                        continue
            elif n ==1:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/use_case')
                    return str(resp)                
                for i in conv_8_2:
                    if str(i) in choice:
                        n +=1
                        resp.redirect("/use_case")
                        return str(resp)
                    else:
                        continue            
            elif n ==2:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/use_case')
                    return str(resp)                
                for i in conv_8_3:
                    if str(i) in choice:
                        n = 0
                        text = "ok, i will call back. Thank you for your time. Have a nice day"
                        resp.say(text, voice='woman', language='en')
                        resp.hangup()
                        return str(resp)
                    else:
                        continue                
                for i in conv_8_4:
                    if str(i) in choice:
                        n +=1
                        resp.redirect("/use_case")
                        return str(resp)
                    else:
                        continue            
            elif n ==3:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/use_case')
                    return str(resp)                
                for i in conv_8_3:
                    if str(i) in choice:
                        n = 0
                        text = "ok, i will call back. Thank you for your time. Have a nice day"
                        resp.say(text, voice='woman', language='en')
                        resp.hangup()
                        return str(resp)
                    else:
                        continue                

            # to be saved in database
            issue = choice
            print(issue)
            text = "Okay. Let me inform bank again on this so that, someone from our end gets this addressed."
            resp.say(text, voice='woman', language='en')
            resp.hangup()
            return str(resp)@app.route('/use_case_4', methods=['GET', 'POST'])
def use_case_4():
    """Processes results from the <Gather> prompt in /voice"""
    global n
    global data
    global bot_resp
    global q_repeat   
    global conv_7_1
    global texts
    global recheck_repeat
    global payable
    # To check whether 'no' is replied twice
    global repeat

    recheck_repeat = 0
    resp = VoiceResponse()
    resp.hangup()
    # print(request.values)
    if 'SpeechResult' in request.values:
        choice = request.values['SpeechResult']
        choice = choice.lower()
        print(choice)
        if choice:
            if n == 0:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/use_case')
                    return str(resp)
                for i in conv_7_1:
                    if str(i) in choice:
                        n = 0
                        text = "Okay. Let me inform bank again on this, so that someone from our end gets this addressed."
                        resp.say(text, voice='woman', language='en')
                        resp.hangup()
                        return str(resp)
                    else:
                        continue

            # to be saved in database
            issue = choice
            print(issue)
            text = "Okay. Let me inform bank again on this, so that someone from our end gets this addressed."
            resp.say(text, voice='woman', language='en')
            resp.hangup()
            return str(resp)

@app.route('/use_case_3', methods=['GET', 'POST'])
def use_case_3():
    """Processes results from the <Gather> prompt in /voice"""
    global n
    global data
    global bot_resp
    global q_repeat   
    global conv_6_1
    global conv_6_2
    global texts
    global recheck_repeat
    global payable
    # To check whether 'no' is replied twice
    global repeat

    recheck_repeat = 0
    resp = VoiceResponse()
    resp.hangup()
    # print(request.values)
    if 'SpeechResult' in request.values:
        choice = request.values['SpeechResult']
        choice = choice.lower()
        print(choice)
        if choice:
            if n == 0:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/use_case')
                    return str(resp)
                for i in conv_6_1:
                    if str(i) in choice:
                        n+=1
                        text = "Ok, let me send the details to our officers."
                        resp.say(text, voice='woman', language='en')
                        resp.redirect("/use_case")
                        return str(resp)
                    else:
                        continue
            elif n == 1:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/use_case')
                    return str(resp)
                for i in conv_6_2:
                    if str(i) in choice:       
                        n = 0
                        text = "Okay.I’m sending this for further scrutiny, Thank you for your time.Have a nice day"
                        resp.say(text, voice='woman', language='en')
                        resp.hangup()
                        return str(resp)

            text = texts[q_repeat]
            q_repeat += 1
            if q_repeat == 4:
                q_repeat = 0
            resp.say(text, voice='woman', language='en')
            resp.redirect("/test")
            return str(resp)@app.route('/use_case_2', methods=['GET', 'POST'])
def use_case_2():
    """Processes results from the <Gather> prompt in /voice"""
    global n
    global data
    global bot_resp
    global q_repeat   
    global conv_5_1
    global conv_5_2
    global texts
    global recheck_repeat
    global payable
    # To check whether 'no' is replied twice
    global repeat

    recheck_repeat = 0
    resp = VoiceResponse()
    resp.hangup()
    # print(request.values)
    if 'SpeechResult' in request.values:
        choice = request.values['SpeechResult']
        choice = choice.lower()
        print(choice)
        if choice:
            if n == 0:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/use_case')
                    return str(resp)
                for i in conv_5_1:
                    if str(i) in choice:
                        n+=1
                        text = "Ok, let me send the details to our officers."
                        resp.say(text, voice='woman', language='en')
                        resp.redirect('/use_case')
                        return str(resp)
                    else:
                        continue
            elif n == 1:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/use_case')
                    return str(resp)
                else:            
                    n=0
                    text = "Request You to kindly try to clear the due as soon as possible and before month-end. \
                    Thank you for your time. Have a nice day."
                    resp.say(text, voice='woman', language='en')
                    resp.hangup()
                    return str(resp)

            text = texts[q_repeat]
            q_repeat += 1
            if q_repeat == 4:
                q_repeat = 0
            resp.say(text, voice='woman', language='en')
            resp.redirect("/test")
            return str(resp)
@app.route('/use_case_1', methods=['GET', 'POST'])
def use_case_1():
    """Processes results from the <Gather> prompt in /voice"""
    global n
    global data
    global bot_resp
    global q_repeat  
    global conv_4_1
    global texts
    global recheck_repeat
    # To check whether 'no' is replied twice
    global repeat

    recheck_repeat = 0
    resp = VoiceResponse()
    resp.hangup()
    # print(request.values)
    if 'SpeechResult' in request.values:
        choice = request.values['SpeechResult']
        choice = choice.lower()
        print(choice)
        if choice:
            if n == 0:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/use_case')
                    return str(resp)
                for i in conv_4_1:
                    if str(i) in choice:
                        n+=1
                        text = "Let me confirm your amount details."
                        resp.say(text, voice='woman', language='en')
                        resp.hangup()
                        return str(resp)
                    else:
                        continue
            elif n == 1:
                if "repeat" in choice or "once more" in choice or "again" in choice:
                    text = "well"
                    resp.say(text, voice='woman', language='en')
                    resp.redirect('/use_case')
                    return str(resp)          
                else:
                    n=0
                    text = "Thank you for your time. Have a nice day."
                    resp.say(text, voice='woman', language='en')
                    resp.hangup()
                    return str(resp)

            text = texts[q_repeat]
            q_repeat += 1
            if q_repeat == 4:
                q_repeat = 0
            resp.say(text, voice='woman', language='en')
            resp.redirect("/test")
            return str(resp)

@app.route("/recheck", methods=['GET', 'POST'])
def recheck():
    """ To recheck input from client in voice """
    global recheck_repeat
    try:
        resp = VoiceResponse()
    except Exception as e:
        print(e)
    try:
        gather = Gather(input='speech', timeout=2 , action='/gather')
        if recheck_repeat == 2:
            resp.hangup()
            return str(resp)
        text = "It seems voice is not clear to me. can you please repeat it once more?"
        recheck_repeat += 1
        gather.say(text, voice="man", language="en")
        resp.append(gather)
    except Exception as e:
        print(e)
    resp.redirect("/recheck")
    return str(resp)

@app.route("/test", methods=['GET', 'POST'])
def test():
    # Start a TwiML response
    try:
        resp = VoiceResponse()
    except Exception as e:
        print(e)
    try:
        gather = Gather(input='speech', speech_timeout='auto', action='/gather')
        resp.append(gather)
    except Exception as e:
        print(e)
    return str(resp)


    # resp.redirect('/')
with open("keywords.json", "r") as f:
        data = json.load(f)
        
conv_1_1 = data["conv_1"]["conv_1_1"]
conv_1_2 = data["conv_1"]["conv_1_2"]
conv_1_3 = data["conv_1"]["conv_1_3"]
conv_1_4 = data["conv_1"]["conv_1_4"]

conv_2_1 = data["conv_2"]["conv_2_1"]
conv_2_2 = data["conv_2"]["conv_2_2"]

conv_3_1 = data["conv_3"]["conv_3_1"]
conv_3_2 = data["conv_3"]["conv_3_2"]

conv_4_1 = data["conv_4"]["conv_4_1"]
conv_4_2 = data["conv_4"]["conv_4_2"]

conv_5_1 = data["conv_5"]["conv_5_1"]
conv_5_2 = data["conv_5"]["conv_5_2"]

conv_6_1 = data["conv_6"]["conv_6_1"]
conv_6_2 = data["conv_6"]["conv_6_2"]

conv_7_1 = data["conv_7"]["conv_7_1"]

conv_8_1 = data["conv_8"]["conv_8_1"]
conv_8_2 = data["conv_8"]["conv_8_2"]
conv_8_3 = data["conv_8"]["conv_8_3"]
conv_8_4 = data["conv_8"]["conv_8_4"]

def outgoing_call(to_, from_,ngrok_url):
    # try:
    #     number = numbers[count]
    #     to_ = "+"+str(number)
    #     print(to_)
    # except:
    #     print("No number left to call")
    # print(to_, ngrok_url, from_)
    try:
        client = Client(sid, auth_token)
        try:
            call = client.calls.create(
                url =  ngrok_url+"/hello",
                to = to_.strip(),
                from_ = from_
            )
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
    except KeyboardInterrupt as e:
        print(e)
if __name__ == '__main__':
        
    try:
        read_csv = pd.read_csv("numbers.csv")
        names = read_csv["Name"]
        numbers = read_csv["Numbers"]
        dues = read_csv["Due"]
        bounce_charges = read_csv["Bounce Charge"]
        due_charges = read_csv["Due Charge"]
        emis = read_csv["EMI"]
    except Exception as e:
        print(e)

    for number in numbers:
        to_ = "+"+str(number)
        print(to_)



    # outgoing_call(to_=to_, from_=from_,ngrok_url=ngrok_url)

    app.run(debug=True)