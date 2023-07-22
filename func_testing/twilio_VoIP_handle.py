"""
Creates an endpoint that can be used in your TwiML App as the Voice Request Url.
In order to make an outgoing call using Twilio Voice SDK, you need to provide a
TwiML App SID in the Access Token. You can run your server, make it publicly
accessible and use `/makeCall` endpoint as the Voice Request Url in your TwiML App.
"""
@app.route('/makeCall', methods=['GET', 'POST'])
def makeCall():
   client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])
   print("## Making a call")
   resp = VoiceResponse()
   to_id = request.values['To']
   from_id = request.values['From']
   session_id = request.values['SessionID']  # name we use to uniquely identify conference


   # creates the call from the from_id to the to_id, adding the to_id to the conference
   call = client.calls.create(from_="client:"+from_id, to="client:"+to_id,
                           url=app.config['MY_URL']'/joinConf/'+str(session_id),
                              status_callback_event=['completed'],
                            status_callback=app.config['MY_URL']+'/completeCall/'+str(session_id))
   # updates global dictionary to handle edge case where caller leaves before callee picks up
   global sessionID_to_callsid
   sessionID_to_callsid[session_id] = call.sid

   # dials the caller (from_id) into the conference
   dial = Dial()
   dial.conference(session_id,
waitUrl='https://twimlets.com/holdmusic?Bucket=my-static-music',
                   status_callback=app.config['MY_URL']+'/leave',
                   status_callback_event="leave join")
   resp.append(dial)

   return str(resp)

# this is an endpoint to add the callee into the conference call
@app.route('/joinConf/<string:call_session_id>', methods=['GET', 'POST'])
def conferenceCall(call_session_id):
   print("## Making a conference call")
   resp = VoiceResponse()
   dial = Dial()
   dial.conference(call_session_id,
                   waitUrl='',
                   status_callback=app.config['MY_URL']+'/leave',
                   status_callback_event="leave")
   resp.append(dial)
   return str(resp)
