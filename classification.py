import pandas
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

data = pandas.read_csv('jsons.csv')

# encoding some features

one_hot = pandas.get_dummies(data['eprtrSectorName'])
data = data.drop('eprtrSectorName', axis=1)
data = data.join(one_hot)

one_hot = pandas.get_dummies(data['countryName'])
data = data.drop('countryName', axis=1)
data = data.join(one_hot)


features = data.columns.tolist()
features.remove('Unnamed: 0')
features.remove('pollutant')
features.remove('CITY ID')
features.remove('CONTINENT')
features.remove('City')
features.remove('EPRTRAnnexIMainActivityLabel')
features.remove('EPRTRAnnexIMainActivityCode')
features.remove('REPORTER NAME')
features.remove('EPRTRSectorCode')
features.remove('FacilityInspireID')
features.remove('targetRelease')
features.remove('facilityName')
X = data[features]
y = data['pollutant']

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = RandomForestClassifier(n_estimators=10)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
conf_mat = metrics.confusion_matrix(y_test, y_pred)
print(conf_mat)
print(metrics.accuracy_score(y_test, y_pred))
print(metrics.precision_score(y_test, y_pred, average='micro'))
print(metrics.recall_score(y_test, y_pred, average='micro'))
print(metrics.f1_score(y_test, y_pred, average='micro'))

feature_imp = pandas.Series(clf.feature_importances_, index=features).sort_values(ascending=False)
print(feature_imp)
