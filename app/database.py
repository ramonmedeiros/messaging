from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable.row_filters import TimestampRange, TimestampRangeFilter, PassAllFilter

from flask import current_app
from datetime import datetime

import json
import os
import logging
import sys

def get_conn():
    dbId = os.environ.get("DB_ID")
    table = os.environ.get("DB_TABLE")

    if dbId is None:
        logging.error("Cannot found Instance ID for DB")
        sys.exit(1)

    if table is None:
        logging.error("Cannot found table for DB")
        sys.exit(1)

    client = bigtable.Client()
    instance = client.instance(dbId)
    return instance.table(table)

def add_row(data):
    table = current_app.config.db

    # format YearMonthDayHourMinuteSecond
    timestamp = datetime.utcnow()
    ts = timestamp.isoformat()

    # key will be ts and fetched flag
    key = f'{ts}'.encode()

    logging.info(f"Adding message {data} with key {key}")
    try:
        row = table.direct_row(key)
        row.set_cell('message',
                     'c1'.encode(),
                     data,
                     timestamp=timestamp)
        row.set_cell("read",
                     "c2".encode(),
                     "0",
                     timestamp=timestamp)
        row.commit()

    except Exception as e:
        logging.error("Cannot add row to DB: {e}")
        return False

    return True

def get_all_rows(callback):
    table = current_app.config.db
    timefilter = PassAllFilter(True)
    partial_rows = table.read_rows(filter_=timefilter)
    rows = {}
    counter = 0
    for row in partial_rows:
        key = row.row_key.decode()
        msg = json.loads(row.cells["message"][b"c1"][0].value.decode())
        read = bool(int(row.cells["read"][b"c2"][0].value.decode()))

        if callback(key, msg, read, counter) is True:
            rows[key] = {"message": msg,
                         "read": read}
            counter+=1
    return rows

def get_rows_by_range(start, end):
    def callback(key, msg, read, counter, start=start, end=end):
        if counter >= start and counter <= end:
            return True

    rows = get_all_rows(callback)
    for row in rows:
        set_as_fetched(row)
    return rows

def get_not_fetched_rows():
    def callback(key, msg, read, counter):
        if read is True:
            return False
        return True

    rows = get_all_rows(callback)
    for row in rows:
        set_as_fetched(row)
    return rows

def set_as_fetched(key):
    timestamp = datetime.utcnow()
    table = current_app.config.db
    row = table.row(key)
    row.set_cell("read",
                 "c2".encode(),
                 "1",
                 timestamp=timestamp)
    row.commit()
