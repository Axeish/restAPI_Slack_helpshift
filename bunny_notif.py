from secret import jc_games, agents, ch_public
from hs_main import retrieve_count



#Python Library
import json
import requests
import schedule
import time
import logging

def slack_format(data):
  '''
  code to just use leftover slack formating
  '''

  total = "Total %d"%(data["total"])
  message =  "Hello, %s Team \n Daily Summary for %s\n"%(data["game"],data["date"])
  message = message + "*%s*\n"%total
  #message = message + "*Category:*\n"
  
  #for each in data["category"]:
   # message = message + each + '\n'
  #return message


def webhook_call():
    for each in jc_games:
        mydata = retrieve_count(each,30)
        print(mydata["total"])
        if mydata['error']:
          message = mydata['error']
          print("---------------")
          print(message)
        else: 
          message = ("%s : %s "%(each, mydata["total"]))
          print (message)
          print("---------------")
 #         message = "hello" 
        slack_data = {'text': message}
        try:

          response = requests.post(
            ch_public, data = json.dumps(slack_data),
            headers = {'Content-Type': 'application/json'})

          print('SUCCESS: Posted to %s'%each)
    
        except requests.exceptions.RequestException as e:  
          print ("ERROR: <bunny line 64> :")
          print(str(e)[:80] + '...')
          pass  
webhook_call()          