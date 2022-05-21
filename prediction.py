import numpy as np
import pandas
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

np.set_printoptions(threshold=np.inf)

data = pandas.read_csv('dataset.csv')
le_general = LabelEncoder()
le_pollutant = LabelEncoder()
data['pollutant'] = le_pollutant.fit_transform(data['pollutant'])
data['countryName'] = le_general.fit_transform(data['countryName'])
data['eprtrSectorName'] = le_general.fit_transform(data['eprtrSectorName'])
data['City'] = le_general.fit_transform(data['City'])
data['EPRTRAnnexIMainActivityCode'] = le_general.fit_transform(data['EPRTRAnnexIMainActivityCode'])
features = data.columns.tolist()
features.remove('pollutant')
X = data[features]
y = data['pollutant']

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = RandomForestClassifier(n_estimators=200)
clf.fit(X_train, y_train)

# read test data
test = pandas.read_csv('test_x.csv')
#test.rename(columns={'EPRTRSectorCode': 'eprtrSectorName'}, inplace=True)
test_index = test['test_index']
for col in test.columns:
    if col not in data.columns:
        test.drop(columns=[col], inplace=True)
        #print('Dropped ' + str(col))
test = test[features]
test['countryName'] = le_general.fit_transform(test['countryName'])
test['eprtrSectorName'] = le_general.fit_transform(test['eprtrSectorName'])
test['City'] = le_general.fit_transform(test['City'])
test['EPRTRAnnexIMainActivityCode'] = le_general.fit_transform(test['EPRTRAnnexIMainActivityCode'])

predictions = clf.predict(test)
predictions = le_pollutant.inverse_transform(predictions)
final_answer = pandas.DataFrame()
final_answer['test_index'] = test_index
final_answer['prediction'] = pandas.Series(predictions)


def getPollutantCode(row):
    match row['prediction']:
        case 'Nitrogen oxides (NOX)':
            pollutant = '0'
        case 'Carbon dioxide (CO2)':
            pollutant = '1'
        case 'Methane (CH4)':
            pollutant = '2'
        case _:
            pollutant = '-1'
    return pollutant


final_answer['pollutant'] = final_answer.apply(lambda row: getPollutantCode(row), axis=1)
final_answer.to_csv('predictions.csv', index=False)
final_answer.to_json('predictions.json', orient='records')
