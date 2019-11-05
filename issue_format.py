def display_request(out):
    cif = out['issues'][0]['custom_fields']
    if cif.get('game'):
        c_game = cif['game']['value']
    else:
        c_game = "NA"
    if cif.get('client_id'):
        c_clientid = cif['client_id']['value']
    else: 
        c_clientid = "NA"
     
    if cif.get('facebook_id'):
        c_fb = cif['facebook_id']['value']
    else: 
        c_fb = "NA"
    if cif.get('game_version'):
        c_version = cif['game_version']['value']
    else: 
        c_version = "NA" 
    if cif.get('category'):
        c_category= cif['category']['value']
    else: 
        c_category = "NA"    

    message =  ">*game*:           %s \n>*client | fb id*:  %s| %s\n>*version*:        %s\n>*category*:      %s\n>*tags*:             %s\n>*message*:         \n>              %s"%(c_game,c_clientid, c_fb,c_version,c_category,out['issues'][0]['tags'],out['issues'][0]['messages'][0]['body'], )

    return message