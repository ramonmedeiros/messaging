from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters

from flask import current_app
from datetime import datetime
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
    conn = current_app.config.db

    # format YearMonthDayHourMinuteSecond
    ts = datetime.now().strftime("%Y%m%d%H%M%S")

    # key will be ts and fetched flag
    key = f'{ts},0'.encode()

    logging.info(f"Adding message {data} with key {key}")
    try:
        row = conn.direct_row(key)
        row.set_cell('message',
                     'c1'.encode(),
                     data,
                     timestamp=datetime.utcnow())
        row.commit()

    except Exception as e:
        logging.error("Cannot add row to DB: {e}")
        return False

    return True
