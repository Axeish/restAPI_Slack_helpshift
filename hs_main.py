from secret import  api_key, url, domain, game
from issue_format import display_request
#Python Library
from datetime import datetime, time, timedelta
import requests
import json
import base64
import sys



#data

category_list =["_stability_","Crashing", "Freezing", "Loading","_purchase_","Bought Currency/Got Kicked Out","Bought Currency/Items Did Not Receive","Bought Currency/Wrong Amount","Charged without Purchase","_game issues_", "Missing Items","Game engine not working","Event Issues","Event Questions","Finished All Levels" ,"Partial Progress Loss","Progress Not saving","Unlocking Next Level","Reset to 1",
"_other_","Feedback" ,"Game Question", "Multiple Device Sync","Connect to FB","Chat Report","Video Ads","Other"]



#now = int(round(time.time() * 1000))
#yesterday = now - 86400000
#yester2= yesterday - 86400000


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


def api_call(api_key,game,category,start,end):

    url = endpoint()    
    encode = base64.b64encode(api_key.encode("UTF-8"))
    headers = {
        'Accept': 'application/json',
        'Authorization': b'Basic '+encode,
    }

    cif_type = '"dropdown":'
    category_param = '"category":{"is_set":true, "is": "%s"}'%category
    game_param = '"game":{"is_set":true, "is":"%s"}'%game

    if category is None:
      category_param =""
    elif category[0] == "_":
      return None    
    else:
      category_param = ',' + category_param
    # cif = '{"dropdown": {"and": {"game":{"is_set":true, "is":"%s"}%s }}}'%(game,category_param)
    cif ='{%s {"and": {%s%s}}}'%(cif_type, game_param,category_param)  

    params = (


    ('created-since', str(start)),
    ('state', 'new,resolved,new-for-agent,agent-replied,waiting-for-agent,pending-reassignment'),
    ('custom_fields', cif),
    ('created-until', str(end)),
    ('page-size', '100'))
    
     
    response = requests.get(url, headers=headers, params=params)
    return response.json()   



def retrieve_count(my_game = None):
    my_game_list = []   
    game_data = {}
    game_data["game"]= my_game
    game_data["date"]= (datetime.today()-timedelta(1)).strftime("%B %d, %Y")
    if my_game:
    	my_game_list.append(my_game)
   

    for each_game in my_game_list:
      response_json = api_call(api_key,each_game,None,yesterday,today)
      total = " Total %d"%(response_json['total-hits'])
      game_data["total"]=total
      game_data["category"] = []	
      for each_category in category_list:

          highlight = ""
          response_json = api_call(api_key,each_game,each_category,yesterday,today)
          if response_json == None:
            cat_data = each_category
            game_data["category"].append(cat_data)
            
          else:  
            count = response_json['total-hits']
            if count > 0:
              if count >10:
                each_category = "*"+each_category+"*"
                highlight="*"
              cat_data = '>%s : %d%s'%(each_category,response_json['total-hits'],highlight)
              game_data["category"].append(cat_data)    
      print('-------------------')
      return game_data 



