import configparser
import json
import os

def json_print(arg):
    arg['reply'] = True
    print(json.dumps(arg))

def start():
    while True:
        config = configparser.ConfigParser()
        # get path of the python script        
        path = input()
        path = json.loads(path)
        path = os.path.join(path["path"], os.pardir)
        config.read_file(open(os.path.join(path,"config.ini")))

        response = {
            'api_key' : config['DEFAULT']['api_key'],
            'save_path' : config['DEFAULT']['save_path'],
            'error' : False
        }
        json_print(response)

if __name__ == "__main__":
    start()