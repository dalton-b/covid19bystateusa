import pandas as pd
import csv
import urllib.request as request
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.tree import DecisionTreeClassifier

def adjust_header(df):
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    return df


def get_confirmed_us():
    r = request.urlopen('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv').read().decode('utf8').split("\n")
    reader = csv.reader(r)
    df = pd.DataFrame(reader)
    df = adjust_header(df)
    df.to_csv('confirmed_us.csv')
    return df


def get_deaths_us():
    r = request.urlopen('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv').read().decode('utf8').split("\n")
    reader = csv.reader(r)
    df = pd.DataFrame(reader)
    df = adjust_header(df)
    df.to_csv('deaths_us.csv')
    return df


# confirmed_us = get_confirmed_us()
# deaths_us = get_deaths_us()
deaths_us = pd.read_csv('deaths_us.csv')
confirmed_us = pd.read_csv('confirmed_us.csv')
confirmed_us.drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State', 'Country_Region'], axis=1, inplace=True)

confirmed_us.drop(confirmed_us.tail(1).index, inplace=True)  # Drop last row, which contains all 'nan'
deaths_us.drop(deaths_us.tail(1).index, inplace=True)

cols = confirmed_us.columns.tolist()
cols.pop(0)
y = confirmed_us[cols.pop(-1)]
cols.pop(cols.index('Combined_Key'))
confirmed_us = confirmed_us[cols]
confirmed_us['Population'] = deaths_us['Population']

cols = confirmed_us.columns.tolist()
cols.insert(0, cols.pop(cols.index('Population')))
confirmed_us = confirmed_us[cols]


# x = confirmed_us
x = confirmed_us.iloc[:, 100:]
# x['Lat'] = confirmed_us['Lat']
# x['Long_'] = confirmed_us['Long_']
# x['Population'] = confirmed_us['Population']
#
# cols = x.columns.tolist()
# cols.insert(0, cols.pop(cols.index('Population')))
# cols.insert(0, cols.pop(cols.index('Long_')))
# cols.insert(0, cols.pop(cols.index('Lat')))
# x = x[cols]

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
# clf = MLPClassifier(hidden_layer_sizes=(50,),
#                     max_iter=300,
#                     activation='relu',
#                     solver='adam',
#                     alpha=0.0001,
#                     random_state=1)
clf = DecisionTreeClassifier(criterion='entropy',
                             splitter='best',
                             max_depth=None,
                             min_samples_split=2,
                             min_samples_leaf=11,
                             max_features=None,
                             random_state=0,
                             max_leaf_nodes=None)
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)
score = clf.score(x_test, y_test)
accuracy_score = accuracy_score(y_test, y_pred)
y_results = np.concatenate((np.expand_dims(y_pred, axis=0), np.expand_dims(y_test.to_numpy(), axis=0)), axis=0)
print(accuracy_score)
