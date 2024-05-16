#!/usr/bin/env python3
import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates specified fields in a log message using regex.
    
    Args:
    fields (list): A list of strings representing all fields to obfuscate.
    redaction (str): The string by which the field will be obfuscated.
    message (str): The log line.
    separator (str): The character separating all fields in the log line.
    
    Returns:
    str: The obfuscated log message.
    """
    pattern = '|'.join(f'({field})' for field in fields)
    return re.sub(pattern, redaction, message, flags=re.IGNORECASE)