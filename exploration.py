import matplotlib.pyplot as plt
import pandas

data = pandas.read_csv('jsons.csv')
cities = data.groupby('CITY ID')['pollutant'].value_counts()
#print(cities.to_string())
#print(data['CITY ID'].value_counts().to_string())
#print(data.loc[data['CITY ID'] == 'cfab1ba8c67c7c838db98d666f02a132'].to_string())

fogs = data.groupby('DAY WITH FOGS')['pollutant'].value_counts()
# seems relevant

avg_wind = data.groupby('pollutant')['avg_wind_speed'].mean()
#print(avg_wind)

min_wind = data.groupby('pollutant')['min_wind_speed'].mean()
#print(min_wind)

max_wind = data.groupby('pollutant')['max_wind_speed'].mean()
#print(max_wind)
# maybe swap

sector = data.groupby('eprtrSectorName')['pollutant'].value_counts()
#print(sector)

reporter = data.groupby('REPORTER NAME')['pollutant'].value_counts()
#print(reporter.to_string())
# useless

continent = data.groupby('CONTINENT')['pollutant'].value_counts()
#print(continent)
# useless

month = data.groupby('MONTH')['pollutant'].value_counts()
#print(month)

year = data.groupby('reportingYear')['pollutant'].value_counts()
#print(year)

NOX_by_year = data.loc[data['pollutant'] == 'Nitrogen oxides (NOX)'].groupby('reportingYear')['pollutant'].value_counts().tolist()
METHANE_by_year = data.loc[data['pollutant'] == 'Methane (CH4)'].groupby('reportingYear')['pollutant'].value_counts().tolist()
CO2_by_year = data.loc[data['pollutant'] == 'Carbon dioxide (CO2)'].groupby('reportingYear')['pollutant'].value_counts().tolist()
years = list(range(2007, 2021))
plt.plot(years, NOX_by_year)
plt.plot(years, METHANE_by_year)
plt.plot(years, CO2_by_year)
plt.title('NOX counts by year')
plt.xlabel('Year')
plt.ylabel('NOX counts')
plt.show()
