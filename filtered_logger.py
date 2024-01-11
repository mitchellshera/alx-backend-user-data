#!/usr/bin/env python3
"""
filtered_logger.py
"""

import re

def filter_datum(fields, redaction, message, separator):
    for field in fields:
        pattern = re.compile(r'{}=([^{}]+)'.format(field, separator))
        message = pattern.sub('{}={}'.format(field, redaction), message)
    return message
