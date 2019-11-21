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
import logging

#--------------------------------------------------------------
#fucntionalities

def slack_format(data):
  '''
  code to just use leftover slack formating
  '''

  total = "Total %d"%(data.total)
  message =  "Hello, %s Team \n Daily Summary for %s\n"%(data.name,data.date)
  message = message + "*%s*\n"%total
  message = message + "*Category:*\n"
  
  for each in data.category:
    message = message + each + '\n'
  return message


def webhook_call(logger, data=None):
  '''
  This function is just a capsule for the scheduler 
  '''

  for each_game,token in game.items():
    mydata = retrieve_count(logger,each_game)
    
    if mydata.error:
      message = mydata.error
      
     
    else: 
      message = slack_format(mydata)
    slack_data = {'text': message}
    

    try:
      response = requests.post(
          token, data = json.dumps(slack_data),
        headers = {'Content-Type': 'application/json'})

      logger.info('SUCCESS: Posted to %s'%each_game)
    
    except requests.exceptions.RequestException as e:  
        logger.exception("Webhook post failed")
        pass  

def job(t):
  '''
  More function will be added to this. 
  Keeping it separate function

  '''  
  log_filename = "app.log"
  logging.basicConfig(filename=log_filename, 
                    format='%(asctime)s %(message)s', 
                    filemode='a') 
  logger=logging.getLogger() 
  webhook_call(logger)

if __name__ == "__main__":



  schedule.every().day.at("05:30").do(job,'')

  while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute


