import pandas

# this function will get a EPRTRAnnexIMainActivityCode from a EPRTRAnnexIMainActivityLabel

data = pandas.read_csv('jsons.csv')
dictionary = dict(zip(data['EPRTRAnnexIMainActivityLabel'], data['EPRTRAnnexIMainActivityCode']))


def getcode(label, dictionary):
    return dictionary[label]
