#!/usr/bin/python
# -*- coding: utf-8 -*-

import timetools as tt


def test_parse_timestamp():
    timestamp = '12th december 1982 4:00PM'
    parsed_timestamp = tt.parse_timestamp(timestamp)
    assert parsed_timestamp == '1982-12-12 16:00:00'

def test_get_time_for_request():
    timestamp = '1982-12-12 16:00:00'
    request_time = tt.get_time_for_request(timestamp)
    assert request_time == '1982-12-12T16:00:00'
