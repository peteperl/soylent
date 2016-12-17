# Usage: python getsoy.py
# pip install pyopenssl ndg-httpsclient pyasn1
#

import requests
import json

SERVER_URL = 'https://quickstats.nass.usda.gov/api/api_GET/'

REQUEST_PARAMS = {
    'key': '657A7402-DF3A-3C12-A7D6-FFCC1DDE180D',
    'format': 'json',
    'commodity_desc': 'SOYBEANS',
    'statisticcat_desc': 'PRODUCTION',
    'agg_level_desc': 'COUNTY',
    'unit_desc': 'BU',
    'prodn_practice_desc': 'ALL PRODUCTION PRACTICES',
    'reference_period_desc': 'YEAR'
}

STATES = ['ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO', 'CONNECTICUT', 'DELAWARE', 'FLORIDA',
          'GEORGIA', 'HAWAII', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 'KENTUCKY', 'LOUISIANA',
          'MAINEMARYLAND', 'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA', 'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA',
          'NEVADA', 'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK', 'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO',
          'OKLAHOMA', 'OREGON', 'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH  CAROLINA', 'SOUTH DAKOTA', 'TENNESSEE', 'TEXAS',
          'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON', 'WEST VIRGINIA', 'WISCONSIN', 'WYOMING']


STATESAB = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


# Base getSoy function
def getSoy(year, state=None, return_json=True):
    if not isinstance(year, int):
        raise ValueError('getSoy year param should be int')

    params = dict(REQUEST_PARAMS)
    params.update({'year': year})
    if state:
        if not state in STATES:
            raise ValueError('getSoy state param should be in STATES list')
        params.update({'state_name': state})

    r = requests.get(SERVER_URL, params=params)
    if return_json:
        return json.loads(r.text)
    else:
        return r.text


# Returns Soy for 2015
def getSoy2015():
    return getSoy(2015)


if __name__ == '__main__':
    print '* Testing: Get Soy 2015'
    soy = getSoy2015()["data"]
    for item in soy:
        print item

    print '* Testing: Get Soy for 2011-2015'
    years = [2011, 2012, 2013, 2014, 2015]
    for year in years:
        print year
        # print getSoy(year)
