#!/usr/bin/env python3
"""
This module provides a function for obfuscating log messages by replacing specified field values.
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (List[str]): A list of strings representing fields to obfuscate in the log message.
        redaction (str): A string representing the value by which the field will be obfuscated.
        message (str): A string representing the log line.
        separator (str): A string representing the character separating all fields in the log line.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(f"(?<={field})=.+?{separator}",
                         f"={redaction}{separator}", message)
    return f'{separator} '.join(re.split(separator, message)).strip()


if __name__ == "__main__":
    pass
