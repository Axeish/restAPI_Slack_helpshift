#----------------------------------------------------------------------
#----------------------------------------------------------------------
#  hs_main : Mostly responsible for making API calls to HelpShift and 
#  Obtaining/Creating relevant data to be used by Slack

#  Author: Ashish Kumar ( Github: Axeish) 

#  Project entry point : Bunny.py | job
#----------------------------------------------------------------------

#My Library
from secret import  api_key, url, domain, game, category_list

#Python Library
from datetime import datetime, time, timedelta
import requests
import json
import base64
import sys
import logging
#--------------------------------------------------------------
#fucntionalities


def midnight():
    midnight = datetime.combine(datetime.today(), time.min)
    today = int(midnight.timestamp() *1000)
    return today


def game_data_request(logger,game,category,start,end):
    '''
    defines relevant headers and params for api call and then 
    makes that api call
    '''

    my_url = url + 'issues/'    
    encode = base64.b64encode(api_key.encode("UTF-8"))
    cif_type = '"dropdown":'
    category_param = '"category":{"is_set":true, "is": "%s"}'%category
    game_param = '"game":{"is_set":true, "is":"%s"}'%game

    # formating different types of api call dynamically. 
    if category is None:
      category_param = ""

    elif category[0] == "_":
      return None

    else:
      category_param = ',' + category_param

    cif = '{%s {"and": {%s%s}}}'%(cif_type, game_param,category_param)  

    headers = {
        'Accept': 'application/json',
        'Authorization': b'Basic '+encode,
    }

    params = (
    ('created-since', str(start)),
    ('state', 'new,resolved,new-for-agent,agent-replied,waiting-for-agent,pending-reassignment'),
    ('custom_fields', cif),
    ('created-until', str(end)),
    ('page-size', '100'))
    
    try:

        response = requests.get(my_url, headers=headers, params=params)
        return response.json()

    except requests.exceptions.RequestException as e:  
        logger.exception("Webhook post failed")
        return {'error': str(e)[:80] + "..."}   
    


def retrieve_count(logger, my_game, days = None):
    '''
    Game_data is a dictionary that will be  get filled after each api call. 
    returning game_data

    '''
    day_milisecond = 86400000
    today_epoch = midnight()
    if days:
      days = int(days)
    else:
      days = 1   
    yesterday = today_epoch - (day_milisecond *int(days))    
    yesterday2 = yesterday - day_milisecond

    game_data = {}
    game_data["game"] = my_game
    game_data["date"] = (datetime.today() - timedelta(1)).strftime("%B %d, %Y")
    game_data["error"] = None

    response_json = game_data_request(logger,my_game,None,yesterday,today_epoch)
    if response_json==None:
      game_data['error'] = "*Error*:"
      return game_data
    if 'error' in response_json:
      game_data['error'] = "*Error*: %s"%json.dumps(response_json['error'])
      return game_data
    game_data["total"] = response_json['total-hits']

    
    game_data["category"] = []
    
    for each_category in category_list:
          highlight = ""   #highlight data for anything more than 10 in count
          response_json = game_data_request(logger,my_game,each_category,yesterday,today_epoch)
          
          if response_json == None:             
            game_data["category"].append(each_category)
            
          else:  
            count = response_json['total-hits']
            if count > 0:
              if count >10:
                each_category = "*" + each_category + "*"
                highlight="*"
              cat_data = '>%s : %d%s'%(each_category,response_json['total-hits'],highlight)
              game_data["category"].append(cat_data)    

    return game_data 



