import json
import request
import time
from crawler import Crawler

def json_print(arg):
    arg['reply'] = True
    arg['time'] = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
    print(json.dumps(arg))

def start():
    
    crawler = Crawler()

    while True:
        try:
            arg = input()
            json_data = json.loads(arg)
            function = getattr(crawler, str(json_data['function']))
            result = function(json_data)
            json_print(result)

        except AttributeError:
            json_bag = {
                "error" : True,
                "message" : f"Method {json_data['function']} does not exist"
            }
            json_print(json_bag)
        except KeyError:
            json_bag = {
                'error' : True,
                'message': f'Key does not exist'
            }
            json_print(json_bag)

        except Exception:
            json_bag = {
                'error' : True,
                'message': 'Some unexpected thing happened',
                'function' : json_data['function']
            }
            json_print(json_bag)
            
    exit(0)

if __name__ == "__main__":
    start()