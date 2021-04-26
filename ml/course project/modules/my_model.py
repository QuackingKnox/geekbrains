import pandas as pd
import os
import dill

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


path = os.path.dirname(os.path.abspath(__file__))
target = 'price_range'
numerical_columns = ['battery_power', 'clock_speed', 'fc', 'int_memory', 'm_dep', 'mobile_wt',
                     'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time']

train = pd.read_csv(path+'\\train.csv')

X_train, X_test, y_train, y_test = train_test_split(train.drop(target, 1),
                                                    train[target], test_size=0.33, random_state=15)

steps = [('scaler', StandardScaler()), ('classifier', LogisticRegression())]

model = Pipeline(steps)

model.fit(X_train, y_train)
predictions = model.predict(X_test)
report = classification_report(y_test, predictions)
print(report)

with open(path+"\\logreg_pipeline.dill", "wb") as f:
    dill.dump(model, f)




