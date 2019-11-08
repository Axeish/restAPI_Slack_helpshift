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

def compile_slack(data):
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
    message = compile_slack(mydata)
    slack_data = {'text': message}
    

    try:

      response = requests.post(
        token, data = json.dumps(slack_data),
        headers = {'Content-Type': 'application/json'})

      print('-------successfully posed to ------%s'%each_game)
    
    except requests.exceptions.RequestException as e:  
        print (e)
        sys.exit(1)  
  


def job(t):
  '''
  # The main Scheduler function start from here . This is also the Entry point for this entire project
  '''  
  webhook_call()


schedule.every().day.at("05:30").do(job,'')

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute

'''
webhook_call()
'''
