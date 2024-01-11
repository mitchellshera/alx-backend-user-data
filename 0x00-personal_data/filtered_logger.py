#!/usr/bin/env python3
"""
This module provides a function for obfuscating
log messages by replacing specified field values.
"""

import re
from typing import List
import logging
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from filtered_logger import get_db, PII_FIELDS


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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
        message = re.sub(field + '=.*?' + separator,
                         field + '=' + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class.

    This class extends the logging.Formatter class
    and provides a custom log formatting
    with redacted sensitive information in log records.

    Attributes:
        redaction (str): The string used for redacting sensitive information.
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
        redacted = filter_datum(self.fields, self.REDACTION,
                                message, self.SEPARATOR)
        return redacted


def get_logger() -> logging.Logger:
    """
    Get a logger named "user_data" with a StreamHandler and RedactingFormatter.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a StreamHandler
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to the MySQL database and returns a connection object.
    Uses environment variables for credentials.
    """
    try:
        username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
        password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
        host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
        db_name = os.getenv("PERSONAL_DATA_DB_NAME")

        connection = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=db_name
        )

        return connection

    except Error as e:
        print(f"Error connecting to the database: {e}")
        raise


def main():
    # Set up logging
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a StreamHandler
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("[HOLBERTON] user_data INFO %(asctime)-15s: %(message)s", "%Y-%m-%d %H:%M:%S")
    stream_handler.setFormatter(formatter)

    # Add the StreamHandler to the logger
    logger.addHandler(stream_handler)

    # Connect to the database
    db = get_db()
    cursor = db.cursor()

    # Retrieve all rows in the users table
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    # Display each row under a filtered format
    for row in rows:
        filtered_row = filter_data(row)
        logger.info(filtered_row)

    # Close cursor and database connection
    cursor.close()
    db.close()

def filter_data(row):
    """
    Filters sensitive fields in a database row.

    Args:
        row: A tuple representing a row from the users table.

    Returns:
        str: A filtered string representation of the row.
    """
    filtered_row = []
    for index, value in enumerate(row):
        field_name = cursor.description[index][0]
        if field_name in PII_FIELDS:
            value = "***"
        filtered_row.append(f"{field_name}={value}")
    
    return "; ".join(filtered_row)

if __name__ == "__main__":
    main()
