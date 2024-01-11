#!/usr/bin/env python3
"""
This module provides a function for obfuscating
log messages by replacing specified field values.
"""

import re
from typing import List
import logging


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: list[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obscures specified fields in a log message.

    Args:
        fields (List[str]): A list of strings
        representing fields to obscure in the log message.
        redaction (str): A string representing
        the value by which the field will be obscured.
        message (str): A string representing the log line.
        separator (str): A string representing the
        character separating all fields in the log line.

    Returns:
        str: The obscured log message.
    """
    for field in fields:
        message = re.sub(field + '=.*?' + separator,
                         field + '=' + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class.

    This class extends the logging.Formatter class
    and provides a custom log formatting
    with obscured sensitive information in log records.

    Attributes:
        redaction (str): The string used for obscuring sensitive information.
        format_str (str): The log record format.
        separator (str): The character separating fields in log messages.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize RedactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format a log message"""
        message = super(RedactingFormatter, self).format(record)
        obscured = filter_datum(self.fields, self.REDACTION,
                                message, self.SEPARATOR)
        return obscured


def get_logger():
    """
    Get a logger named "user_data" with a StreamHandler and RedactingFormatter.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a StreamHandler
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


if __name__ == "__main__":
    pass
