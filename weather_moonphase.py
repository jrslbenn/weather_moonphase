#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import json
import requests
import os
import sqlite3

import moonphase_utils
import timetools


CONN = sqlite3.connect('example.db', check_same_thread=False)
CURSOR = CONN.cursor()
# Should probably store this elsewhere, but for simpilicity's sake here it is.
API_KEY = 'cf1272d922e1345d4e32f6ac7085fdd7'
SEATTLE_LAT = 47.6062
SEATTLE_LONG = -122.3321
BASE_URL = 'https://api.darksky.net/forecast'


def get_weather_and_moonphase(timestamp, lat=SEATTLE_LAT,
                              long=SEATTLE_LONG):
    """Get temperature and moonphase for a given time and location.

       args:
            timestamp: Timestamp-like string such as 'yyyy-mm-dd hh:mm:ss' or '12 dec 1980 11 am'.
            lat: Latitude of the location of interest, defaults to Seattle.
            long: Longitude of location of interest, defaults to Seattle.
    """
    timestamp = timetools.parse_timestamp(timestamp)
    query_result = get_weather_from_db(timestamp, lat, long)
    if len(query_result) > 0:
        result = result_as_dict(query_result[0])
    else:
        request_time = timetools.get_time_for_request(timestamp)
        response = make_weather_request(request_time, lat, long)
        hourly_data = parse_response_for_hourly_weather(timestamp, response,
                                                        lat, long)
        upload_rows = format_data_for_upload(hourly_data)
        upload_data(upload_rows)
        result = hourly_data[timestamp]
        result['timestamp'] = timestamp
    return result


def result_as_dict(result):
    """Converts SQL query result (list) to dict with desired keys.

       args:
            result: Result of SQL query for the requested location, latitude, and longitude.
    """
    print("Data was cached!")
    result_dict = {
        'temperature_f': result[1],
        'moonphase': result[2],
        'numeric_moonphase': result[3],
        'latitude': result[4],
        'longitude': result[5],
        'timestamp': result[0]
    }
    return result_dict

def get_weather_from_db(ts, lat, long):
    """Queries our weather and moonphase database
       for your requested time and location.

       args:
            ts: Timestamp to query for in the weather database.
            lat: Latitude to query for in the weather database.
            long: Longitude to query for in the weather database.
    """
    ensure_table()
    query = """ SELECT *
                  FROM weather_conditions
                 WHERE weather_dt = '{}'
                   AND latitude = {}
                   AND longitude = {}
            """.format(ts, lat, long)
    CURSOR.execute(query)
    results = CURSOR.fetchall()
    return results


def make_weather_request(timestamp, lat=SEATTLE_LAT, long=SEATTLE_LONG):
    """Submits API request and returns JSON.
    
       args:
            timestamp: Timestamp to request weather for from API.
            lat: Latitude of location of weather request.
            long: Longitude of location of weather request.
    """
    request_url = \
        '{base}/{key}/{lat},{long},{time}'.format(base=BASE_URL,
            key=API_KEY, lat=lat, long=long,
            time=timestamp)
    response = requests.get(request_url)
    response_json = json.loads(response.text)
    return response_json


def parse_response_for_hourly_weather(timestamp, response, lat, long):
    """Extracts hourly temperature and moonphase from api response
    
       args:
            timestamp: Timestamp to request weather for from API.
            response: JSON response from weather API.
            lat: Latitude of location of weather request.
            long: Longitude of location of weather request.
    """
    hourly_temperature = {}
    moonphase, numeric_moonphase = moonphase_utils.get_moonphase(response)
    if 'hourly' in response.keys():
        for entry in response['hourly']['data']:
            ts = str(datetime.fromtimestamp(entry['time']))
            temp_f = entry['temperature']
            hourly_temperature[ts] = {
                'temperature_f': temp_f,
                'moonphase': moonphase,
                'numeric_moonphase': numeric_moonphase,
                'latitude': lat,
                'longitude': long
            }
    else:
        raise ValueError("Temperature data not available for this location, "
                         "try making sure this isn't a remote location")
    return hourly_temperature


def format_data_for_upload(hourly_data):
    """Converts hourly data from a dictionary to a list of tuples to upload.

       args:
            hourly_data: Dictionary containing data from the
                         response of the weather api.
    """
    rows = []
    for hour in hourly_data:
        row = []
        row.append(hour)
        hour_dict = hourly_data[hour]
        for key in hourly_data[hour]:
            row.append(hour_dict[key])
        rows.append(tuple(row))
    return rows


def upload_data(rows):
    """When we are forced to make a request,
       this uploads our newly recieved rows to our database.

       args:
            rows: List of tuple records of weather data to be uploaded to db.
    """
    CURSOR.executemany("""INSERT INTO weather_conditions
                          ('weather_dt', 'temperature_f', 'moonphase',
                           'moonphase_decimal', 'latitude', 'longitude'
                          )
                          VALUES (?,?,?,?,?,?);
                       """, rows)
    CONN.commit()


def ensure_table():
    create_statement = """ CREATE TABLE IF NOT EXISTS weather_conditions
                           (
                                weather_dt datetime,
                                temperature_f float,
                                moonphase tinytext,
                                moonphase_decimal float,
                                latitude float,
                                longitude float,
                                PRIMARY KEY(weather_dt, latitude, longitude)
                            );
                       """
    CURSOR.execute(create_statement)
    CONN.commit()
