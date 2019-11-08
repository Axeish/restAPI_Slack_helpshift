#----------------------------------------------------------------------
#----------------------------------------------------------------------
#  bunny : responsible for webhooks to CS channels on slack. It calls 
#  hs_main to get all the relvant data

#  Author: Ashish Kumar ( Github: Axeish) 

#  Project entry point : Bunny.py | job
#----------------------------------------------------------------------

#My Library
from secret import game
from hs_main import retrieve_count

#Python Library
import json
import requests
import schedule
import time

#--------------------------------------------------------------
#fucntionalities

def slack_format(data):
  '''
  code to just use leftover slack formating
  '''

  total = "Total %d"%(data["total"])
  message =  "Hello, %s Team \n Daily Summary for %s\n"%(data["game"],data["date"])
  message = message + "*%s*\n"%total
  message = message + "*Category:*\n"
  
  for each in data["category"]:
    message = message + each + '\n'
  return message


def webhook_call(data=None):
  '''
  This function is just a capsule for the scheduler 
  '''

  for each_game,token in game.items():
    mydata = retrieve_count(each_game)
    if mydata['error']:
      message = mydata['error']
      print("---------------")
      print(message)
    else: 
      message = slack_format(mydata)
    slack_data = {'text': message}
    

    try:

      response = requests.post(
          token, data = json.dumps(slack_data),
        headers = {'Content-Type': 'application/json'})

      print('SUCCESS: Posted to %s'%each_game)
    
    except requests.exceptions.RequestException as e:  
        print ("ERROR: <bunny line 64> :")
        print(str(e)[:80] + '...')
        pass  
  


def job(t):
  '''
  More function will be added to this. 
  Keeping it separate function
  '''  
  webhook_call()

if __name__ == "__main__":

  schedule.every().day.at("05:30").do(job,'')

  while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute

'''
webhook_call()
'''
