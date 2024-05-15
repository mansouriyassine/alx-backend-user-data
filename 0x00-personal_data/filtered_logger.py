#!/usr/bin/env python3

import logging
import re


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        log_message = super().format(record)
        for field in self.fields:
            log_message = self.filter_datum(
                [field], self.REDACTION, log_message, self.SEPARATOR
            )
        return log_message

    @staticmethod
    def filter_datum(fields, redaction, message, separator):
        regex = r"(?<=(?:^|{}))([^{}]+)(?=(?:{}|$))".format(
            separator, separator, separator
        )
        return re.sub(regex, redaction, message, flags=re.IGNORECASE)


fields = ["password", "date_of_birth"]
messages = [
    "name=egg;email=eggmin@eggsample.com;password=eggcellent;"
    "date_of_birth=12/12/1986;",
    "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;",
]

for message in messages:
    print(RedactingFormatter.filter_datum(fields, "xxx", message, ";"))

message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
log_record = logging.LogRecord(
    "my_logger", logging.INFO, None, None, message, None, None
)
formatter = RedactingFormatter(fields=("email", "ssn", "password"))
print(formatter.format(log_record))