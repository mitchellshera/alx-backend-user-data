#!/usr/bin/env python3
"""
Main file
"""

import logging

get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS

logger = get_logger()
print(logger.__class__)
print("PII_FIELDS: {}".format(len(PII_FIELDS)))
