import json
import requests
import pandas

urls = ['http://schneiderapihack-env.eba-3ais9akk.us-east-2.elasticbeanstalk.com/first',
        'http://schneiderapihack-env.eba-3ais9akk.us-east-2.elasticbeanstalk.com/second',
        'http://schneiderapihack-env.eba-3ais9akk.us-east-2.elasticbeanstalk.com/third']


def json_to_dataframe(url):
    print(url)
    resp = requests.get(url=url)
    data = resp.json()
    json = pandas.DataFrame()
    for count, row in enumerate(data):
        print(" " + str(count))
        currentrow = pandas.DataFrame(data[count], index=[count])
        json = pandas.concat([json, currentrow], axis='rows')
    return json


final_frame = pandas.DataFrame()
for url in urls:
    temp = json_to_dataframe(url)
    final_frame = pandas.concat([final_frame, temp], axis='rows')

final_frame.to_csv('jsons.csv', index=False)
