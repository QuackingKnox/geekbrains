import requests
import json


main_link = 'https://api.vk.com/method/groups.get'
access_token = 'a7f5d7159cd15c4fb0ca0f691614f1cc65d58186ffcac6f009ef5d9ba04be45713cfb4ac15aa6425f7f9'

response = requests.get(f'{main_link}?v=5.52&access_token={access_token}')

with open('vkdata.json', 'w') as f:
    json.dump(response.json(), f)

j_data = response.json()
print(f"Список id сообществ: {j_data['response']['items']}")
