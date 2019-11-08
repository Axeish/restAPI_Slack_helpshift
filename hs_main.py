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



def midnight():
    midnight = datetime.combine(datetime.today(), time.min)
    today = int(midnight.timestamp() *1000)
    return today


today = midnight()
yesterday = today - 86400000    
yester2= yesterday - 86400000 


def endpoint():
    endpoint = url + 'issues/' 
    return endpoint

def slack_bolder(data):
    return "*" + data + "*"

#--------------------------------------------------------------
#fucntionalities


def api_call_request(game,category,start,end):
    '''
    defines relevant headers and params for api call and then 
    makes that api call
    '''
    
    url = endpoint()    
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

        response = requests.get(url, headers=headers, params=params)
    except requests.exceptions.RequestException as e:  
        print (e)
        sys.exit(1)    
    return response.json()


def retrieve_count(my_game = None):
    '''
    Game_data is a dictionary that will be  get filled after each api call. 
    returning game_data

    '''
    game_data = {}
    game_data["game"] = my_game
    game_data["date"] = (datetime.today() - timedelta(1)).strftime("%B %d, %Y")
    

    response_json = api_call_request(my_game,None,yesterday,today)
    
    game_data["total"] = response_json['total-hits']
    
    game_data["category"] = []

    for each_category in category_list:
          highlight = ""   #highlight data for anything more than 10 in count
          response_json = api_call_request(my_game,each_category,yesterday,today)
          
          if response_json == None:             
            game_data["category"].append(each_category)
            
          else:  
            count = response_json['total-hits']
            if count > 0:
              if count >10:
                each_category = slack_bolder(each_category)
                highlight="*"
              cat_data = '>%s : %d%s'%(each_category,response_json['total-hits'],highlight)
              game_data["category"].append(cat_data)    

    
    return game_data 



