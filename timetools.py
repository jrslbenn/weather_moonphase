#!/usr/bin/python
# -*- coding: utf-8 -*-

from dateutil import parser

def parse_timestamp(timestamp):
    try:
        timestamp = parser.parse(timestamp)
        timestamp = timestamp.replace(minute=0, second=0)
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    except:
        raise ValueError("Timestamp parser couldn't parse your input.\n"
                         "Try using a timestamp like this: [YYYY-MM-DD HH:MM:SS]")
    return timestamp


def get_time_for_request(timestamp):
    request_time = ''
    for i in range(0, len(timestamp)):
        if timestamp[i] == ' ':
            request_time += 'T'
        else:
            request_time += timestamp[i]
    return request_time
