import pandas

json_data = pandas.read_csv('jsons.csv')
pdf_data = pandas.read_csv('pdfs\\pdfs.csv')
csv_data = pandas.read_csv('train_part_csv.csv')

dictionary = dict(zip(json_data['EPRTRAnnexIMainActivityLabel'], json_data['EPRTRAnnexIMainActivityCode']))


def getcode(label, dictionary):
    # based on data from here: https://iir.umweltbundesamt.de/2021/general/point_sources/start
    if label == 'Chemical installations for the production on an industrial scale of basic organic chemicals: Organometallic compounds':
        return '4(a)(vii)'
    return dictionary[label]


def getsectorcode(string):
    return string[0]


def


# in order to concatenate all datasets we need to make some adjustments
pdf_data.drop(columns=['emission'], inplace=True)
csv_data['EPRTRAnnexIMainActivityCode'] = csv_data.apply(lambda row: getcode(row['EPRTRAnnexIMainActivityLabel'], dictionary), axis=1)
pdf_data.rename(columns={'DAYS WITH FOG': 'DAY WITH FOGS'}, inplace=True)
pdf_data.drop(columns=['EPRETRSectorCode'], inplace=True)
csv_data.drop(columns=['EPRTRAnnexIMainActivityLabel'], inplace=True)
json_data.drop(columns=['EPRTRAnnexIMainActivityLabel'], inplace=True)
json_data.drop(columns=['EPRTRSectorCode'], inplace=True)
pdf_data.drop(columns=['EPRTRAnnexIMainActivityLabel'], inplace=True)
json_data.drop(columns=['Unnamed: 0'], inplace=True)
pdf_data.rename(columns={'eptrSectorName': 'eprtrSectorName'}, inplace=True)


data = pandas.concat([csv_data, json_data, pdf_data], axis='rows')
data.drop(columns=['FacilityInspireID'], inplace=True)
data.drop(columns=['facilityName'], inplace=True)
data.drop(columns=['targetRelease'], inplace=True)
data.drop(columns=['CONTINENT'], inplace=True)
data.drop(columns=['REPORTER NAME'], inplace=True)
data.drop(columns=['CITY ID'], inplace=True)
data.to_csv('dataset.csv', index=False)
