#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_moonphase(response):
    if 'daily' in response.keys():
        phase = response['daily']['data'][0]['moonPhase']
        return calculate_moonphase(phase)
    else:
        return 'unavailable moonphase', -1


def calculate_moonphase(numeric_moonphase):
    if numeric_moonphase == 0:
        moonphase = 'new moon'
    elif numeric_moonphase < .25:
        moonphase = 'waxing crescent'
    elif numeric_moonphase == .25:
        moonphase = 'first quarter moon'
    elif numeric_moonphase < .5:
        moonphase = 'waxing gibbous'
    elif numeric_moonphase == .5:
        moonphase = 'full moon'
    elif numeric_moonphase < .75:
        moonphase = 'last quarter moon'
    elif numeric_moonphase == .75:
        moonphase = 'waning gibbous'
    elif numeric_moonphase < 1:
        moonphase = 'waning crescent'
    return (moonphase, numeric_moonphase)
