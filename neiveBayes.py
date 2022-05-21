import pandas
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from numpy import mean
from numpy import std

data = pandas.read_csv('dataset.csv')
le = LabelEncoder()
data['pollutant'] = le.fit_transform(data['pollutant'])
data['countryName'] = le.fit_transform(data['countryName'])
data['eprtrSectorName'] = le.fit_transform(data['eprtrSectorName'])
data['City'] = le.fit_transform(data['City'])
data['EPRTRAnnexIMainActivityCode'] = le.fit_transform(data['EPRTRAnnexIMainActivityCode'])
features = data.columns.tolist()
features.remove('pollutant')
X = data[features]
y = data['pollutant']
print(features)

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
gnb = GaussianNB()
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)
conf_mat = metrics.confusion_matrix(y_test, y_pred)
print(conf_mat)
print(metrics.accuracy_score(y_test, y_pred))
print(metrics.precision_score(y_test, y_pred, average='micro'))
print(metrics.recall_score(y_test, y_pred, average='micro'))
print(metrics.f1_score(y_test, y_pred, average='micro'))
