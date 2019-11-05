from secret import  api_key, url, domain, game
from issue_format import display_request
#Python Library
from datetime import datetime, time, timedelta
import requests
import json
import base64
import sys



#data

category_list =["Crashing", "Freezing", "Loading", "Bought Currency/Got Kicked Out","Bought Currency/Items Did Not Receive","Bought Currency/Wrong Amount","Charged without Purchase","Missing Items","Game engine not working","Event Issues","Event Questions","Feedback" ,"Game Question","Finished All Levels" ,"Partial Progress Loss","Progress Not saving","Unlocking Next Level","Reset to 1",
"Multiple Device Sync","Connect to FB","Chat Report","Video Ads","Other"]



#now = int(round(time.time() * 1000))
#yesterday = now - 86400000
#yester2= yesterday - 86400000


def midnight():
    midnight = datetime.combine(datetime.today(), time.min)
    today = int(midnight.timestamp() *1000)
    return today


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

def api_call_b(api_key,game,end):

    url = endpoint()    
    encode = base64.b64encode(api_key.encode("UTF-8"))
    headers = {
        'Accept': 'application/json',
        'Authorization': b'Basic '+encode,
    }
   
     
    cif = '{"dropdown": {"and": {"game":{"is_set":true, "is":"%s"} }}}'%(game)
   
    
    params = (


    
    ('state', 'new,pending-reassignment'),
    ('custom_fields', cif),
    ('state_until', str(end)),
    ('page-size', '100'))
    

     
    response = requests.get(url, headers=headers, params=params)
    return response.json()       



def api_call_id(api_key,url):
    
    encode = base64.b64encode(api_key.encode("UTF-8"))
    headers = {
        'Accept': 'application/json',
        'Authorization': b'Basic '+encode,
    }

    response = requests.get(url, headers=headers)
    return response.json()


def retrieve_count(my_game = None):
    my_game_list = []
    if my_game:
    	my_game_list.append(my_game)
    else:
    	my_game_list.extend(game)

    for each_game in my_game_list:
      print ("Last 24 hours...")
      response_json = api_call(api_key,each_game,None,yesterday,today)
      print ("%s : Total %d"%(each_game,response_json['total-hits']))
      for each_category in category_list:
          
          response_json = api_call(api_key,each_game,each_category,yesterday,today)
          count = response_json['total-hits']
          if count > 0:
            print ('%s : %d'%(each_category,response_json['total-hits']))    
      print('-------------------')


def retrieve_back(my_game= None):
  if my_game:
    response_json = api_call_b(api_key,my_game,yesterday)
    print ("%s : Total %d"%(my_game,response_json['total-hits']))
    return 1
  print ("last 48 hours")
  for each_game in game:
    response_json = api_call_b(api_key,each_game,yesterday)
    print ("%s : Total %d"%(each_game,response_json['total-hits']))
 

def retrieve_id(my_id):
  url = endpoint()
  url = url + my_id	
  response_json = api_call_id(api_key, url)
  message = display_request(response_json)
  print (message)


if __name__ == "__main__":


    today = midnight()
    yesterday = today - 86400000
    yester2= yesterday - 86400000

    if len(sys.argv)>1:
        print (sys.argv[1])
        if sys.argv[1] == "backlog":
          if len(sys.argv)>2:	
            retrieve_back(sys.argv[2])
          else:
            retrieve_back()  
        elif sys.argv[1] == "daily_count":
          if len(sys.argv)>2:	
            retrieve_count(sys.argv[2])
          else:
            retrieve_count()
        elif sys.argv[1][:2]== 'ID':
            retrieve_id(sys.argv[1][2:])    
        else:
          print ("choose 'backlog', 'daily_count', 'ID' ")    
    else:
        print ("choose 'backlog', 'daily_count', 'ID' ")          	
    #action()

