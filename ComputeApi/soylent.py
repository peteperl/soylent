# Server to get soy and weather data
#

import json
import getsoy
import weather
import mock_soyres
import lat_long
from operator import itemgetter
import time
from timeit import Timer
from multiprocessing import Pool

__author__ = 'peteperl'

CPUS = 8

LATLONG = None

STATESAB = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


# These are checks to validate the inputs
def validateCounty(state, county):
    if len(state) < 2 or len(county) < 1:
        return False
    latlong = lat_long.lat_long
    key = "%s_%s" % (state.upper(), county.upper())
    try:
        latitude, longitude = latlong[key]
    except KeyError:
        return False
    return True


# These are checks to validate the inputs
def validateState(state):
    if state.upper() in STATESAB:
        return True
    else:
        return False


# Returns top soybean producing counties & today's rainfall
def getSoyRainAll(num):
    allsoy = mock_soyres.soyres["data"]
    sortedSoy = sortSoyProduction(allsoy)
    topSoy = getTopSoy(sortedSoy, 'ALL', num)
    topSoyRes = []

    for tsoy in topSoy:
        state = tsoy["state_alpha"]
        county = tsoy["county_name"]
        rain = '0'  # Rain is slow to get, get in parallel
        tsr = [county, state, tsoy["Value"], rain, tsoy["ValueInt"]]
        topSoyRes.append(tsr)

    topSoyRain = getRainPar(topSoyRes)
    return topSoyRain


# Returns top soybean producing counties & today's rainfall
def getSoyRainState(num, state):
    allsoy = mock_soyres.soyres["data"]
    sortedSoy = sortSoyProduction(allsoy)
    topSoy = getTopSoy(sortedSoy, state, num)
    topSoyRes = []

    for tsoy in topSoy:
        state = tsoy["state_alpha"]
        county = tsoy["county_name"]
        rain = '0'  # Rain is slow to get, get in parallel
        tsr = [county, state, tsoy["Value"], rain, tsoy["ValueInt"]]
        topSoyRes.append(tsr)

    topSoyRain = getRainPar(topSoyRes)
    return topSoyRain


def getRainPar(work):
    p = Pool(CPUS)
    results = p.map(rain_worker, work)
    return results


def rain_worker(tsr):
    try:
        # Get Rainfall: Here I have no cache and just get from API
        # Try cache first, else:
        latitude, longitude = getLatLon(tsr[1], tsr[0])
        rain = str(weather.getRainApi(latitude, longitude))
        # Write result to cache
        tsr[3] = rain
    except KeyError:
        pass
    return tsr


def get_soyrain(state, county):
    # logResponse([state, county])
    if len(state) < 2:
        state = "AL"
    if len(county) < 1:
        county = "AUTAUGA"
    # return soyrain_mock()
    return soyrain(state.upper(), county.upper())


def soyrain_mock():
    return [str(12345), str(11)]


# Takes sorted soyList from: sortSoyProduction(soyList)
# Gets top soy producing counties filtered by state
def getTopSoy(soyList, state, maxnum):
    stateu = state.upper()
    if stateu == 'ALL':
        return soyList[:maxnum]
    filteredSoy = []
    if stateu in STATESAB:
        for s in soyList:
            if s["state_alpha"] == stateu:
                filteredSoy.append(s)
        return filteredSoy[:maxnum]
    else:
        return filteredSoy


# Adds an integer soybean production value for sorting by soybean production
def valueInt(soyItem):
    soyValue = soyItem["Value"]
    soyInt = int(soyValue.replace(',', ''))
    soyItem["ValueInt"] = soyInt
    return soyItem


# Sorts a list of soybean production items from most to least
def sortSoyProduction(soyList):
    # newlist = sorted(l, key=itemgetter('name'), reverse=True)
    for s in soyList: valueInt(s)
    sortedSoyProd = sorted(soyList, key=itemgetter("ValueInt"), reverse=True)
    return sortedSoyProd


# Takes a county
# Return (soy, rain)
def soyrain(state, county):
    # Get soy production
    # This is a mock cache
    allsoy = mock_soyres.soyres["data"]
    sortedsoy = {}
    for st in getsoy.STATESAB:
        sortedsoy[st] = {}
    for sy in allsoy:
        sortedsoy[sy["state_alpha"]][sy["county_name"]] = sy
    try:
        soy = sortedsoy[state][county]["Value"]
    except KeyError:
        soy = "0"
        # If there is a cache miss: getsoy.getSoy(year, state), write to cache

    # Get Rainfall: Here I have no cache and just get from API
    # Try cache first, else:
    latitude, longitude = getLatLon(state, county)
    rain = str(weather.getRainApi(latitude, longitude))
    # Write result to cache

    return [soy, rain]


# Takes a county
# Return latitude, longitude
def getLatLon(state, county):
    # latlong = weather.loadCounties()
    latlong = lat_long.lat_long
    latitude, longitude = weather.countyLatLon(latlong, state.upper(), county.upper())
    return latitude, longitude


def logResponse(r):
    filen = "response_log.txt"
    filepath = "/var/www/flaskserver/log/"
    filepn = filepath + filen
    rlog = json.dumps(r)
    with open(filepn, "a+") as f:
        f.write(rlog)
        f.write('\n')


def get_soyrain_(form):
    # logResponse(form)
    return soyrain_mock()


def fooi():
    allsoy = mock_soyres.soyres["data"]
    for s in allsoy: valueInt(s)


def foos():
    allsoy = mock_soyres.soyres["data"]
    ssoy = sortSoyProduction(allsoy)


if __name__ == '__main__':
    print '* Testing: Soy & Rain'
    ts = time.time()
    # print soyrain_mock()
    # print get_soyrain('CA', 'Alameda')
    # print get_soyrain('AL', 'COLBERT')

    # print validateCounty('CA', 'Alameda')
    # print validateCounty('AL', 'COLBERT')
    # print validateCounty('CA', 'Asasa')
    # print validateCounty('A', 'Asasa')
    # print validateCounty('CA', '')

    # allsoy = mock_soyres.soyres["data"]
    # for s in allsoy: valueInt(s)
    # ssoy = sortSoyProduction(allsoy)
    # for s in ssoy: print s["Value"]

    # t1 = Timer("""fooi()""", """from __main__ import fooi""")
    # print t1.timeit(1000)

    # t2 = Timer("""foos()""", """from __main__ import foos""")
    # print t2.timeit(1000)

    # print valueInt(allsoy[0])
    # for s in allsoy: valueInt(s)
    # for si in allsoy: print si

    print getSoyRainAll(8)
    print getSoyRainState(8, 'AL')
    tf = time.time()
    print tf - ts
