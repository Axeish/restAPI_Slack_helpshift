from secret import  api_key, url, domain, game

#Python Library
import requests
import json
import base64
import sys
import time


#data

category_list =["Crashing", "Freezing", "Loading", "Bought Currency/Got Kicked Out","Bought Currency/Items Did Not Receive","Bought Currency/Wrong Amount","Charged without Purchase","Missing Items","Game engine not working","Event Issues","Event Questions","Feedback" ,"Game Question","Finished All Levels" ,"Partial Progress Loss","Progress Not saving","Unlocking Next Level","Reset to 1",
"Multiple Device Sync","Connect to FB","Chat Report","Video Ads","Other"]



now = int(round(time.time() * 1000))
yesterday = now - 86400000
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

def retrieve_count():
    
    for each_game in game:
      print ("Last 24 hours...")
      response_json = api_call(api_key,each_game,None,yesterday,now)
      print ("%s : Total %d"%(each_game,response_json['total-hits']))
      for each_category in category_list:
          
          response_json = api_call(api_key,each_game,each_category,yesterday,now)
          count = response_json['total-hits']
          if count > 0:
            print ('%s : %d'%(each_category,response_json['total-hits']))    
      print('-------------------')

def action():
	retrieve_count()    

if __name__ == "__main__":

	so = endpoint()
	print(endpoint)
	print(url)
	action()
