import requests
import json

token = ""
key = ""

if __name__=="__main__":
        url = "https://api.trello.com/1/boards/<id>/lists"
        data = {
            "key": key,
            "token": token,
        }
        response = requests.request("GET", url, params=data).text
        response_json = json.loads(response)
        print(json.dumps(response,indent=4, sort_keys=True))
        print(response)
