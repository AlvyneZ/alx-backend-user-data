#!/usr/bin/env python3
"""
This "filtered-logger.py" module provides one function:
    filter_datum(fields, redaction, message, separator)
 and one class:
    RedactingFormatter(logging.Formatter)
"""


from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Searches for specific fields in a given message
     and redacts them

    Args:
        fields (List[str]): the sensitive fields to be redacted
         from the message
        redaction (str): the text to replace the sensitive data
        message (str): the original message with sensitive data
        separator (str): the separator between fields of the
         message

    Returns:
        str: the message with sensitive data redacted
    """
    pattern: str = r"(?<={})({})=.*?{}".format(
        separator, ("|".join(fields)), separator)
    match: str = r"\1={}{}".format(redaction, separator)
    return re.sub(pattern, match, message)



class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError