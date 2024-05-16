#!/usr/bin/env python3
"""
Module for handling Personal Data
"""
from typing import List
import re
import logging
from os import environ
import mysql.connector


SENSITIVE_FIELDS = ("name", "email", "phone", "ssn", "password")


def obfuscate_data(fields: List[str], redaction: str,
                   message: str, separator: str) -> str:
    """ Returns a log message obfuscated """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def setup_logger() -> logging.Logger:
    """ Returns a Logger Object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(DataRedactingFormatter(list(SENSITIVE_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def connect_to_database() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connector to a MySQL database """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connection.MySQLConnection(user=username,
                                                            password=password,
                                                            host=host,
                                                            database=db_name)
    return connection


def main():
    """
    Obtain a database connection using connect_to_database and retrieves all rows
    in the users table and display each row under a filtered format
    """
    db_connection = connect_to_database()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = setup_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db_connection.close()


class DataRedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(DataRedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records using obfuscate_data """
        record.msg = obfuscate_data(self.fields, self.REDACTION,
                                     record.getMessage(), self.SEPARATOR)
        return super(DataRedactingFormatter, self).format(record)


if __name__ == '__main__':
    main()
