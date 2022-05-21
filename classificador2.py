import pandas
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

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
clf = RandomForestClassifier(n_estimators=200)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
conf_mat = metrics.confusion_matrix(y_test, y_pred)
print(conf_mat)
print(metrics.accuracy_score(y_test, y_pred))
print(metrics.precision_score(y_test, y_pred, average='micro'))
print(metrics.recall_score(y_test, y_pred, average='micro'))
print(metrics.f1_score(y_test, y_pred, average='micro'))

feature_imp = pandas.Series(clf.feature_importances_, index=features).sort_values(ascending=False)
print(feature_imp.to_string())

FP_0 = conf_mat[1][0] + conf_mat[2][0]
FN_0 = conf_mat[0][1] + conf_mat[0][2]
FP_1 = conf_mat[0][1] + conf_mat[2][1]
FN_1 = conf_mat[1][0] + conf_mat[1][2]
FP_2 = conf_mat[0][2] + conf_mat[1][2]
FN_2 = conf_mat[2][0] + conf_mat[2][1]

FP = FP_0 + FP_1 + FP_2
FN = FN_0 + FN_1 + FN_2
print(FP)
print(FN)
