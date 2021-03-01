import requests
import json


main_link = 'https://api.github.com'
user = 'quackingknox'

response = requests.get(f'{main_link}/users/{user}/repos')

with open('data.json', 'w') as f:
    json.dump(response.json(), f)

for i in response.json():
    print(i['name'])
    
