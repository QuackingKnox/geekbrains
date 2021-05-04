import pandas as pd
import os
import dill
import json
from flask import Flask, request, jsonify

path = os.path.dirname(os.path.abspath(__file__))+'\\models\\'

with open(path+'logreg_pipeline.dill', 'rb') as in_strm:
    model = dill.load(in_strm)

app = Flask(__name__)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    data = {"success": False}
    # ensure an image was properly uploaded to our endpoint
    if request.method == "POST":
        my_json = request.get_json()
        json_load = json.loads(my_json)
        list_of_values = list(json_load.values())
        list_of_features = list(json_load.keys())
        my_sample = pd.DataFrame(data=[list_of_values], columns=list_of_features)
        preds = model.predict(my_sample)

    if request.method == "GET":
        print('Отправте запрос, чтобы узнать ценовую категорию смартфона!')

    data["predictions"] = [int(_) for _ in preds]
    data["success"] = True

    # return the data dictionary as a JSON response
    return jsonify(data)


if __name__ == '__main__':
    app.run()
