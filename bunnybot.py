
from secret import ch_public, ch_private
import json
import requests

from main import retrieve_count



def compile_slack(data):
   message =  "Daily Summary for %s\n"%mydata["game"]
   message = message + "*%s*\n"%mydata["total"]
   message = message + "*Category*\n"
   for each in mydata["category"]:
     message = message + ">" +each + '\n'
   return message


mydata = retrieve_count("Cookie Jam")
message = compile_slack(mydata)

slack_data = {'text': message}

response = requests.post(
    ch_private, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
)
if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )

