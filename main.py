import pdfquery as pq
import pandas as pd
import requests
import os


def scrapePdf(pdfPath):
    pdf = pq.PDFQuery(pdfPath)
    pdf.load()
    pdfData = pd.DataFrame({
        "countryName": pdf.pq('LTTextLineHorizontal:overlaps_bbox("138.98, 686.86, 211.513, 697.9")').text(),
        "EPRETRSectorCode": pdf.pq('LTTextLineHorizontal:overlaps_bbox("180.26, 643.3, 185.857, 654.34")').text(),
        "eptrSectorName":
            pdf.pq('LTTextLineHorizontal:overlaps_bbox("210.29, 643.3, 471.936, 654.34")').text().split(" ", 1)[1],
        "EPRTRAnnexIMainActivityCode":
            pdf.pq('LTTextLineHorizontal:overlaps_bbox("52.8, 614.26, 157.097, 625.3")').text().split(" ", 1)[1],
        "EPRTRAnnexIMainActivityLabel": "",
        "FacilityInspireID":
            pdf.pq('LTTextLineHorizontal:overlaps_bbox("52.8, 715.9, 266.172, 726.94")').text().split(" ", 1)[1],
        "facilityName":
            pdf.pq('LTTextLineHorizontal:overlaps_bbox("52.8, 730.42, 343.076, 741.46")').text().split(" ", 2)[2],
        "City": pdf.pq('LTTextLineHorizontal:overlaps_bbox("138.98, 672.34, 221.195, 683.38")').text(),
        "CITY ID": pdf.pq('LTTextLineHorizontal:overlaps_bbox("138.98, 175.7, 312.518, 186.74")').text(),
        "targetRelease": pdf.pq('LTTextLineHorizontal:overlaps_bbox("138.98, 570.67, 154.094, 581.71")').text(),
        "pollutant": pdf.pq('LTTextLineHorizontal:overlaps_bbox("306.17, 570.67, 406.325, 581.71")').text(),
        "DAY": pdf.pq('LTTextLineHorizontal:overlaps_bbox("174.62, 527.11, 185.857, 538.15")').text(),
        "MONTH": pdf.pq('LTTextLineHorizontal:overlaps_bbox("347.47, 527.11, 384.086, 538.15")').text().split(" ", 1)[
            0],
        "reportingYear": pdf.pq('LTTextLineHorizontal:overlaps_bbox("461.38, 527.11, 483.897, 538.15")').text(),
        "CONTINENT": pdf.pq('LTTextLineHorizontal:overlaps_bbox("437.02, 686.86, 473.96, 697.9")').text(),
        "max_wind_speed":
            pdf.pq('LTTextLineHorizontal:overlaps_bbox("52.8, 452.11, 185.806, 463.15")').text().split(" ", 1)[1],
        "avg_wind_speed":
            pdf.pq('LTTextLineHorizontal:overlaps_bbox("316.87, 452.11, 483.846, 463.15")').text().split(" ", 2)[2],
        "min_wind_speed":
            pdf.pq('LTTextLineHorizontal:overlaps_bbox("316.87, 452.11, 483.846, 463.15")').text().split(" ", 1)[0],
        "max_temp": pdf.pq('LTTextLineHorizontal:overlaps_bbox("144.02, 388.01, 185.806, 399.05")').text(),
        "avg_temp": pdf.pq('LTTextLineHorizontal:overlaps_bbox("442.06, 388.01, 483.846, 399.05")').text(),
        "min_temp":
            pdf.pq('LTTextLineHorizontal:overlaps_bbox("311.23, 388.01, 405.714, 399.05")').text().split(" ", 1)[0],
        "DAYS WITH FOG": pdf.pq('LTTextLineHorizontal:overlaps_bbox("174.62, 323.93, 185.857, 334.97")').text(),
        "REPORTER NAME":
            pdf.pq('LTTextLineHorizontal:overlaps_bbox("356.95, 233.81, 504.706, 244.85")').text().split(":", 1)[1]
    }, index=[0])

    pdfData.rename(columns={'DAYS WITH FOG': 'DAY WITH FOGS'}, inplace=True)
    pdfData.rename(columns={'eptrSectorName': 'eprtrSectorName'}, inplace=True)
    return pdfData


def getPdfNames():
    pdfsPath = './pdfs/'
    files = [f for f in os.listdir(pdfsPath) if os.path.isfile(os.path.join(pdfsPath, f))]
    for file in files:
        if file.split(".")[1] != 'pdf':
            files.remove(file)
    files = map(lambda file: pdfsPath + file, files)
    return files


pdfData = pd.DataFrame()
files = getPdfNames()
for file in files:
    pdfData = pd.concat([pdfData, scrapePdf(file)], axis=0)


def jsonToDataframe(url):
    print(url)
    resp = requests.get(url=url)
    data = resp.json()
    df = pd.DataFrame()
    for count, row in enumerate(data):
        entry = pd.DataFrame(data[count], index=[count])
        df = pd.concat([df, entry], axis='rows')
    return df


urls = ['http://schneiderapihack-env.eba-3ais9akk.us-east-2.elasticbeanstalk.com/first',
        'http://schneiderapihack-env.eba-3ais9akk.us-east-2.elasticbeanstalk.com/second',
        'http://schneiderapihack-env.eba-3ais9akk.us-east-2.elasticbeanstalk.com/third']
jsonData = pd.DataFrame()
for url in urls:
    temp = jsonToDataframe(url)
    jsonData = pd.concat([jsonData, temp], axis='rows')
#jsonData.drop(columns=['EPRTRAnnexIMainActivityLabel'], inplace=True)
jsonData.drop(columns=['EPRTRSectorCode'], inplace=True)
jsonData.drop(columns=[''], inplace=True)


def getcode(label, dictionary):
    # based on data from here: https://iir.umweltbundesamt.de/2021/general/point_sources/start
    if label == 'Chemical installations for the production on an industrial scale of basic organic chemicals: Organometallic compounds':
        return '4(a)(vii)'
    return dictionary[label]

df1 = pd.read_csv("./csvs/train1.csv")
df2 = pd.read_csv("./csvs/train2.csv", sep=';')
frames = [df1,df2]
csvData = pd.concat(frames)

names_list = csvData.columns.to_list()

aux = 0
for element in names_list:
    if csvData[element].isnull().values.any():
        aux = aux + 1
        print(csvData[element].isnull().values.any())
if aux > 0:
    print('existing nulls')
else:
    print('no existing nulls')
csvData['EPRTRAnnexIMainActivityCode'] = csvData.apply(lambda row: getcode(row['EPRTRAnnexIMainActivityLabel'], dict(zip(jsonData['EPRTRAnnexIMainActivityLabel'], jsonData['EPRTRAnnexIMainActivityCode']))), axis=1)
csvData.drop(columns=['EPRTRAnnexIMainActivityLabel'], inplace=True)
jsonData.drop(columns=['EPRTRAnnexIMainActivityLabel'], inplace=True)



data = pd.concat([jsonData, csvData, pdfData], axis='rows')

data.drop(columns=['FacilityInspireID'], inplace=True)
data.drop(columns=['facilityName'], inplace=True)
data.drop(columns=['targetRelease'], inplace=True)
data.drop(columns=['CONTINENT'], inplace=True)
data.drop(columns=['REPORTER NAME'], inplace=True)
data.drop(columns=['CITY ID'], inplace=True)


for idx, row in enumerate(data.iterrows(), 1):
    print(row)
    if(row['min_wind_speed'] > row['max_wind_speed']):
        data.loc[idx,['min_wind_speed','max_wind_speed']] = data.loc[idx,['max_wind_speed','min_wind_speed']].values

for idx, row in enumerate(data.iterrows(), 1):
    if(row['min_temp'] > row['max_temp']):
        data.loc[idx,['min_temp','max_temp']] = data.loc[idx,['max_temp','min_temp']].values

head = data.head(-82)
uk = head.loc[head['countryName'] == 'United Kingdom']
uk_max_wind = uk['max_wind_speed'].astype(float).mean()
uk_min_wind = uk['min_wind_speed'].astype(float).mean()
uk_avg_wind = uk['avg_wind_speed'].astype(float).mean()
uk_max_temp = uk['max_temp'].astype(float).mean()
uk_min_temp = uk['min_temp'].astype(float).mean()
uk_avg_temp = uk['avg_temp'].astype(float).mean()
tail = data.tail(82)
tail = tail.assign(max_wind_speed=uk_max_wind)
tail = tail.assign(min_wind_speed=uk_min_wind)
tail = tail.assign(avg_wind_speed=uk_avg_wind)
tail = tail.assign(max_temp=uk_max_temp)
tail = tail.assign(min_temp=uk_min_temp)
tail = tail.assign(avg_temp=uk_avg_temp)

data = pd.concat([head, tail], axis='rows')