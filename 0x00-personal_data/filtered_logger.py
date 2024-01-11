#!/usr/bin/env python3
"""
This module provides a function for obfuscating
log messages by replacing specified field values.
"""

import re
from typing import List
import logging


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')
FIELDS = ('name', 'email', 'phone', 'ssn', 'password',
          'ip', 'last_login', 'user_agent')


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class.

    This class extends the logging.Formatter class
    and provides a custom log formatting
    with redacted sensitive information in log records.

    Attributes:
        REDACTION (str): The string used for redacting sensitive information.
        FORMAT (str): The log record format.
        SEPARATOR (str): The character separating fields in log messages.
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
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (List[str]): A list of strings
        representing fields to obfuscate in the log message.
        redaction (str): A string representing
        the value by which the field will be obfuscated.
        message (str): A string representing the log line.
        separator (str): A string representing the
        character separating all fields in the log line.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(f"(?<={field})=.+?{separator}",
                         f"={redaction}{separator}", message)
    return ';'.join(re.split(separator, message)).strip() + ';'


def get_logger():
    """
    Get a logger named "user_data" with a StreamHandler and RedactingFormatter.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.Logger('user_data', level=logging.INFO)
    # logger.propagate = False
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(streamHandler)
    return logger

if __name__ == "__main__":
    pass
