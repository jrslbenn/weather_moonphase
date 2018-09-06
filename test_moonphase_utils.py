#!/usr/bin/python
# -*- coding: utf-8 -*-

import moonphase_utils as mu
import weather_moonphase as wm
SEATTLE_LAT = 47.6062
SEATTLE_LONG = -122.3321
VALID_MOONPHASES = ['new moon', 'waxing crescent',
                    'first quarter moon', 'waxing gibbous',
                    'full moon', 'last quarter moon', 'waning gibbous',
                    'waning crescent', 'unavailable moonphase']

def test_get_moonphase():
    request_time = '2018-02-10 12:00:00'
    response = wm.make_weather_request(request_time, SEATTLE_LAT,
                                    SEATTLE_LONG)
    moonphase, numeric_moonphase = mu.get_moonphase(response)
    assert(type(moonphase) == str)
    assert(type(numeric_moonphase) in [float, int])
    assert((numeric_moonphase <= 1 and numeric_moonphase >= 0)
           or numeric_moonphase == -1)
    assert(moonphase in VALID_MOONPHASES)
    # This location doesn't have daily data therefore moonphase missing
    bad_response = wm.make_weather_request(request_time, SEATTLE_LAT,
                                       -1 * SEATTLE_LONG)
    moonphase, numeric_moonphase = mu.get_moonphase(bad_response)
    assert(type(moonphase) == str)
    assert(type(numeric_moonphase) in [int, float])
    assert((numeric_moonphase <= 1 and numeric_moonphase >= 0)
           or numeric_moonphase == -1)
    assert(moonphase in VALID_MOONPHASES)

def test_calculate_moonphase():
    numeric_moonphase = .73
    assert mu.calculate_moonphase(numeric_moonphase) == ('last quarter moon', numeric_moonphase)
    numeric_moonphase = 0
    assert mu.calculate_moonphase(numeric_moonphase) == ('new moon', numeric_moonphase)