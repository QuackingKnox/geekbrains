import requests
import os
import pandas as pd
import json
import numpy as np

path = os.path.dirname(os.path.abspath(__file__))
sample_number = np.random.randint(10000)
train = pd.read_csv(path+'\\models\\train.csv')
data = json.loads(train.iloc[sample_number, :-1].to_json())


def send_json(x):
    myurl = 'http://f4d644870a9a.ngrok.io/'+'predict'
    headers = {'content-type': 'application/json; charset=utf-8'}
    response = requests.post(myurl, json=json.dumps(x), headers=headers)
    print(response)
    return response.json()['predictions']

# обращение к серверу с запросом из одного набора (его построили руками выше - data)

if __name__ == '__main__':
    response = send_json(data)
    print('предсказание', response)