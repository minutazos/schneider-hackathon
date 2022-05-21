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
data.rename(columns={'min_wind_speed': 'max_wind_speed', 'max_wind_speed': 'min_wind_speed',
                     'min_temp': 'max_temp', 'max_temp': 'min_temp'}, inplace=True)
data.drop(columns=['FacilityInspireID'], inplace=True)
data.drop(columns=['facilityName'], inplace=True)
data.drop(columns=['targetRelease'], inplace=True)
data.drop(columns=['CONTINENT'], inplace=True)
data.drop(columns=['REPORTER NAME'], inplace=True)
data.drop(columns=['CITY ID'], inplace=True)
head = data.head(-82)
uk = head.loc[head['countryName'] == 'United Kingdom']
uk_max_wind = uk['max_wind_speed'].mean()
uk_min_wind = uk['min_wind_speed'].mean()
uk_avg_wind = uk['avg_wind_speed'].mean()
uk_max_temp = uk['max_temp'].mean()
uk_min_temp = uk['min_temp'].mean()
uk_avg_temp = uk['avg_temp'].mean()
tail = data.tail(82)
tail = tail.assign(max_wind_speed=uk_max_wind)
tail = tail.assign(min_wind_speed=uk_min_wind)
tail = tail.assign(avg_wind_speed=uk_avg_wind)
tail = tail.assign(max_temp=uk_max_temp)
tail = tail.assign(min_temp=uk_min_temp)
tail = tail.assign(avg_temp=uk_avg_temp)

data = pandas.concat([head, tail], axis='rows')
data.to_csv('dataset.csv', index=False)
