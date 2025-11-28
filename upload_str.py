
import json, requests

def recordBotStructures(generation = 0, content = "", botName = ""):
    """Record bot strutures every generation.


    Keyword Arguments:
        generaion {int} -- [description] (default: {0})
        content {str} -- [description] (default: {""})

    """

    dataSend = {}
    dataSend["optimisation_id"] = "12345"
    dataSend["generation"] = generation
    dataSend["bot_name"] = botName
    dataSend["action"] = "update_structure"
    dataSend["structure"] = json.dumps(content)
    dataSend["market"] = "upload"

    dataSendJSON = json.dumps(dataSend)
    
    
    # print (dataSendJSON)
    
    

    # API_ENDPOINT = "https://www.vixencapital.com/api/optimisation/index.php"
    API_ENDPOINT = "https://marlin-network.hopto.org/api/v1/data/structure/"
    
    try:
        r = requests.post(url = API_ENDPOINT, data = dataSendJSON)
        print ("1")
        print (r)
        print ("2")
        response = r.text
        print ("3")
        
        print ("4")
        print("Str Sent")
        exit()
      
    except:
        print (f"Error sending ")
        
   


import glob

for file in list(glob.glob('bot_str/*.json')):            
    json_str = None
    f =  (file.split('.')[0])
    f1 = f.split('/')[1]
    f2 = '_'.join(f1.split('_')[:-1])
    print (f2)
    with open(f'{file}', 'r') as fp:            
        json_str = json.load(fp)   
        
    bot_id = f2
    if json_str is not None:
        recordBotStructures(content = json_str, botName=bot_id)
    # 