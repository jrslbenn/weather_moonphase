import weather_moonphase as wm
import moonphase_utils as mu
SEATTLE_LAT = 47.6062
SEATTLE_LONG = -122.3321
VALID_MOONPHASES = ['new moon', 'waxing crescent',
                    'first quarter moon', 'waxing gibbous',
                    'full moon', 'last quarter moon', 'waning gibbous',
                    'waning crescent', 'unavailable moonphase']

def test_get_weather_and_moonphase():
    timestamp = '2018-02-10 12:30:32'
    data_for_the_hour = wm.get_weather_and_moonphase(timestamp, SEATTLE_LAT,
                                                     SEATTLE_LONG)
    assert(type(data_for_the_hour) == dict)
    assert(len(data_for_the_hour.keys()) == 6)
