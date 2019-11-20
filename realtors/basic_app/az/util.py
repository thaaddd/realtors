import re
import datetime
import io
import re
import zipfile
import csv
import json
from flask import jsonify

import requests

camel_reg = re.compile(r"(?!^)(?<!_)([A-Z])")


def to_json(inst, cls, dump_json=True):
    """
    Jsonify the sql alchemy query result.
    """

    if isinstance(inst, list):
        return jsonify([to_json(x, cls, dump_json=False) for x in inst])

    convert = {datetime.datetime: (lambda x: x.isoformat())}

    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type.python_type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type.python_type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    if dump_json:
        return jsonify(d)
    else:
        return d


def camelToSnake(s):

    """"""

    if s == "DBAName":
        return "dba_name"

    if s == "EmployerDBAName":
        return "employer_dba_name"

    return camel_reg.sub(r"_\1", s).lower()


def download_extract_zip(event_target):

    url = "https://services.azre.gov/publicdatabase/DownloadLists.aspx"

    data = {"__EVENTTARGET": event_target}
    response = requests.post(url, data=data, stream=True)
    with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
        for zipinfo in thezip.infolist():
            with thezip.open(zipinfo) as thefile:
                yield zipinfo.filename, thefile


def get_objects(event_target, target_file):
    for filename, file in download_extract_zip(event_target=event_target):
        if filename != target_file:
            continue
        for row in csv.DictReader(io.TextIOWrapper(file)):
            yield row
