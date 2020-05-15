# If method return to outside class scope,
# Method return type should be 'dict'
# Make sure return dicttionary
# otherwise, it will cause exception

import json
import requests
from itertools import chain

class Crawler:
    def makeDict(self, result):
        resultArr = []
        for index, value in enumerate(result['items']):
            tempDict = {
                "authorDisplayName" : value['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                "likeCount" : value['snippet']['topLevelComment']['snippet']['likeCount'],
                "textOriginal" : value['snippet']['topLevelComment']['snippet']['textOriginal'],
                "publishedAt" : value['snippet']['topLevelComment']['snippet']['publishedAt']
            }
            resultArr.append(tempDict)
        return resultArr

    def generate_url(self, api_key, video_id, nextPageToken):
        return (f"https://www.googleapis.com/youtube/v3/commentThreads"
        f"?part=id%2Csnippet&order=time&"
        f"videoId={video_id}&key={api_key}&pageToken={nextPageToken}")

    def goto_next_page(self, api_key, video_id, nextPageToken):
        url = self.generate_url(api_key, video_id, nextPageToken)
        return requests.get(url).json()

    def api_request(self, api_key, video_id, amount):
        url = (f"https://www.googleapis.com/youtube/v3/commentThreads"
            f"?part=id%2Csnippet&order=time&"
                f"videoId={video_id}&key={api_key}")
        
        request_result = requests.get(url).json()
        result_arr = []

        for i in range(int(amount)):
            i = i + int(request_result['pageInfo']['totalResults'])
            result_arr.append(self.makeDict(request_result))
            if 'nextPageToken' in request_result:
                request_result = self.goto_next_page(api_key, video_id, request_result['nextPageToken'])
            else:
                return result_arr
        
        return result_arr

    def get_comments(self, json_data):

        if(json_data['api_key'] == '' or json_data['video_id'] == ''
        or json_data['order_by'] == '' or json_data['save_path'] == ''
        or json_data['amount'] == ''):
            return_value = {'message': "Please check your input",
                        'error' : True,
                        'data_received' : {
                            "api_key" : json_data.get("api_key"),
                            "video_id" : json_data.get("video_id"),
                            "order_by" : json_data.get("order_by"),
                            "save_path" : json_data.get("save_path"),
                            "amount" : json_data.get("amount") 
                        }
            }
            return return_value
        
        result = self.api_request(json_data.get("api_key"),
                      json_data.get("video_id"), json_data.get('amount'))
        result = {'comments': list(chain(*result)), 'error' : False}
        return result 

          