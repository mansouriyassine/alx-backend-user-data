#!/usr/bin/env python3
"""
Module for handling Personal Data
"""
import mysql.connector
import logging
import os
import re


def filter_datum(fields, redaction, message, separator):
    """
    Replace sensitive data with a redacted version in the message.

    :param fields: List of sensitive fields to redact.
    :param redaction: Redacted value to replace sensitive data.
    :param message: Original message containing sensitive data.
    :param separator: Separator used to split fields in the message.
    :return: Message with sensitive data redacted.
    """
    pattern = '|'.join(re.escape(field) for field in fields)
    return re.sub(pattern, redaction, message)


class RedactingFormatter(logging.Formatter):
    """
    Custom logging formatter to redact sensitive information.

    :param fields: List of sensitive fields to redact.
    """
    def __init__(self, fields):
        super().__init__()
        self.fields = fields

    def format(self, record):
        message = record.getMessage()
        for field in self.fields:
            message = filter_datum([field], '***', message, ';')
        return message


def get_logger():
    """
    Get a logger configured to redact sensitive information.

    :return: Configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(["email", "ssn", "password"])
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db():
    """
    Connect to the database using environment variables.

    :return: Database connection object.
    """
    cnx = mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        database=os.getenv('PERSONAL_DATA_DB_NAME', '')
    )
    return cnx


def main():
    """
    Main function to fetch and print user data from the database.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        formatted_row = ";".join(
            filter_datum(["name", "email", "phone", "ssn", "password"], '***',
                         f"{field}={value}", ';')
            for field, value in zip(['name', 'email', 'phone',
                                     'ssn', 'password'], row))
        print(formatted_row)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
