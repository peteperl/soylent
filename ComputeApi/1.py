# Usage: python weather.py
#
import requests
import json
import csv

API_KEY = 'b977b78f21d77e2ce42bcf8a8bb4d7ac'  # replace with your api key
API_SERVER_URL = 'https://api.darksky.net/forecast/' + API_KEY + '/'
API_REQUEST_TIMEOUT = 10

COUNTY_CSV = 'USAcounties.csv'  # modify this to '/PATH/TO/CSV/UsaCounties.csv'


def loadCounties():
    """
        Load counties from CSV
        counties keyed by sticking together the state abbreviation and county name
        State = AL, county = AUTAUGA
        counties[AL_ATAUGA] = (latitude, longitude)
    """
    counties = {}

    with open(COUNTY_CSV) as f:
        reader = csv.reader(f)
        # ignore heading
        next(reader)

        for line in reader:
            key = "%s_%s" % (line[1], line[3].upper())
            # print key
            latitude = float(line[-2])
            longitude = float(line[-1])
            counties[key] = (latitude, longitude)

    return counties


def countyLatLon(countieslatlon, state, county):
    """
        Take the previously made dict, state, county
        Return latitude, longitude
    """
    if 'OTHER' in county:
        county = 'OTHER'
    key = "%s_%s" % (state, county)
    try:
        latitude, longitude = countieslatlon[key]
    except KeyError:
        # expected exception handling if needed
        raise KeyError('No such state/county pair in the csv')

    return latitude, longitude


"""
def getRain(latitude, longitude):
    rkey = str(year) + '_' + str(latitude) + '_' + str(longitude)
    rain = r.get_rain(rkey)

    if not rain:
        rain = getRainApi(latitude, longitude)
        r.cache_rain(rkey, rain)

    # format rainfall
    return rain
"""


def getRainApi(latitude, longitude):
    """
        Get Rain from API
    """
    url = API_SERVER_URL + "%s,%s" % (latitude, longitude)

    # exclude everything except daily report 
    params = {'exclude': 'currently,minutely,hourly'}

    # request 
    r = requests.get(url, params=params, timeout=API_REQUEST_TIMEOUT)
    # print '* Rain Request:'

    # get forecast for current day
    try:
        daily_forecast = json.loads(r.text)['daily']['data'][0]
        # print daily_forecast
        # print daily_forecast['summary']
        # print daily_forecast['precipType']
        # print daily_forecast['precipIntensity']
    except KeyError:
        # expected exception handling if needed
        raise KeyError('Malformed response')

    # Rain detection
    # base scenario
    rain = False 
    rain_intensity = 0

    # check some keys
    # according to docs: https://darksky.net/dev/docs/response
    # first check if there is any rain
    if 'icon' in daily_forecast:
        # icon optional
        # A machine-readable text summary of this data point

        rain = daily_forecast['icon'] == 'rain'

    elif 'precipType' in daily_forecast:
        rain = daily_forecast['precipType'] == 'rain'

    if rain and 'precipIntensity' in daily_forecast:
        rain_intensity = daily_forecast['precipIntensity']

    # from docs:
    # precipIntensity - The intensity (in inches of liquid water per hour) of precipitation occurring at the given time.
    # So, to get precip_accumulation we should multiply rain_intensity * 24 hour in day
    rain_accumulation = rain_intensity * 24
    return rain_accumulation


if __name__ == '__main__':
    print '* Testing: load CSV'
    cll = loadCounties()
    print cll

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
