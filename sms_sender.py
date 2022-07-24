# importing twilio
from twilio.rest import Client
  
# Your Account Sid and Auth Token from twilio.com / console
account_sid = 'ACd1447c2bbb0a951536d92ebc648a05b5'
auth_token = 'c7915cb23a5806a5b7707460b98887e2'
  
client = Client(account_sid, auth_token)

message = client.messages.create(
                              from_='+13257701598',
                              body ='1st python code for testing',
                              to ='+919319206402'
                          )
  
print(message.sid)