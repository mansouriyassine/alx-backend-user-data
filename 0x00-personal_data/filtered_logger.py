#!/usr/bin/env python3
"""
Filtered Logger Module
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (List[str]): List of strings representing fields to obfuscate.
        redaction (str): String representing the redaction value.
        message (str): String representing the log line.
        separator (str): String representing the character separating fields.

    Returns:
        str: Log message with specified fields obfuscated.
    """
    return separator.join(
        re.sub(
            r'(?<={}=).+?(?={})'.format(field, re.escape(separator)),
            redaction,
            part
        ) if field in fields else part
        for field, part in zip(fields, message.split(separator))
    )
