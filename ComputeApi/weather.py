# Usage: python weather.py
#
import requests
import json
import csv

API_KEY = 'b977b78f21d77e2ce42bcf8a8bb4d7ac'  # replace with your api key
API_SERVER_URL = 'https://api.darksky.net/forecast/' + API_KEY + '/'
API_REQUEST_TIMEOUT = 10

COUNTY_CSV = 'USAcounties.csv'  # modify this to '/PATH/TO/CSV/UsaCounties.csv'


# Load counties from CSV
def loadCounties():
    counties = {}

    with open(COUNTY_CSV, 'rU') as f:
        reader = csv.reader(f)
        next(reader)  # ignore heading

        for line in reader:
            # counties keyed by sticking together the state abbreviation and county name
            key = "%s_%s" % (line[0], line[1].upper())
            latitude = float(line[2])
            longitude = float(line[3])
            counties[key] = (latitude, longitude)  # counties[AL_ATAUGA] = (latitude, longitude)

    return counties


# To handle 'OTHER' county in soy data
# add a 'STATE_OTHER' field with any lat/long from the STATE
def fixOther(cll):
    with open(COUNTY_CSV, 'rU') as f:
        reader = csv.reader(f)
        next(reader)  # ignore heading

        for line in reader:
            key = "%s_%s" % (line[0], 'OTHER')
            latitude = float(line[2])
            longitude = float(line[3])
            cll[key] = (latitude, longitude)

    return cll


# Take the previously made dict, state, county
# Return latitude, longitude
def countyLatLon(countieslatlon, state, county):
    if 'OTHER' in county:
        county = 'OTHER'
    key = "%s_%s" % (state, county)
    try:
        latitude, longitude = countieslatlon[key]
    except KeyError:
        # expected exception handling if needed
        raise KeyError('No such state/county pair in the csv')

    return latitude, longitude


"""  This is an outline of you I would likely handle the Rain caching
def getRain(latitude, longitude):
    rkey = str(year) + '_' + str(latitude) + '_' + str(longitude)
    rain = r.get_rain(rkey)

    if not rain:
        rain = getRainApi(latitude, longitude)
        r.cache_rain(rkey, rain)

    # format rainfall
    return rain
"""


# Get Rain from API
def getRainApi(latitude, longitude):
    url = API_SERVER_URL + "%s,%s" % (latitude, longitude)

    # Exclude everything except daily report 
    params = {'exclude': 'currently,minutely,hourly'}

    r = requests.get(url, params=params, timeout=API_REQUEST_TIMEOUT)

    # Get forecast for current day
    try:
        daily_forecast = json.loads(r.text)['daily']['data'][0]
    except KeyError:
        raise KeyError('Malformed response')

    # Rain detection, base scenario
    rain = False
    rain_intensity = 0

    # Docs: https://darksky.net/dev/docs/response
    # first check if there is any rain
    if 'icon' in daily_forecast:
        # icon optional: A machine-readable text summary of this data point
        rain = daily_forecast['icon'] == 'rain'

    elif 'precipType' in daily_forecast:
        rain = daily_forecast['precipType'] == 'rain'

    if rain and 'precipIntensity' in daily_forecast:
        rain_intensity = daily_forecast['precipIntensity']

    # Docs:
    # precipIntensity - The intensity (in inches of liquid water per hour) of precipitation occurring at the given time.
    # To get precip_accumulation we multiply rain_intensity * 24 hour in day
    rain_accumulation = rain_intensity * 24
    return rain_accumulation


if __name__ == '__main__':
    print '* Testing: load CSV'
    cll = loadCounties()
    print cll
    cllo = fixOther(cll)
    print cllo
    print cllo['AL_OTHER']

    """
    print '* Testing: latitude, longitude'
    latitude, longitude = countyLatLon(cll, 'AL', 'COFFEE')
    print 'AL, COFFEE: '
    print latitude
    print longitude

    latitude, longitude = countyLatLon(cll, 'AZ', 'SANTA CRUZ')
    print 'AZ, SANTA CRUZ: '
    print latitude
    print longitude

    latitude, longitude = countyLatLon(cll, 'CA', 'ALAMEDA')
    print 'CA, ALAMEDA: '
    print latitude
    print longitude

    print '* Testing: getRain'
    print getRainApi(latitude, longitude)

    # TODO remove me
    # print '* Somewhere in california, it rains (actual on 15 december 2016)'
    print getRainApi(37.702923, -122.389893)
    # Somewhere in moscow there is snow (precip intensity exists but it's actually snow) 
    print getRainApi(55, 37)
    """
