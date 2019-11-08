
from secret import ch_public, ch_private, game
import json
import requests
import schedule
import time

from hs_main import retrieve_count



def compile_slack(data):
  # code to just use slack formating 
   message =  "Hello, %s Team \n Daily Summary for %s\n"%(data["game"],data["date"])
   message = message + "*%s*\n"%data["total"]
   message = message + "*Category:*\n"
   for each in data["category"]:
     message = message  +each + '\n'
   return message


def webhook_call(data=None):
  for each_game,token in game.items():
    mydata = retrieve_count(each_game)
    message = compile_slack(mydata)
    slack_data = {'text': message}
    
    response = requests.post(
      token, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
  )
  if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )



def job(t):
    webhook_call()

schedule.every().day.at("17:51").do(job,'')

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
'''


webhook_call()
'''