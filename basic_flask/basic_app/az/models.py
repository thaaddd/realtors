from sqlalchemy.sql import expression
from basic_app import db

from .util import get_objects, camelToSnake, to_json
import datetime
import re
import sqlalchemy


class IDModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @property
    def json(self):
        return to_json(self, self.__class__)

    @classmethod
    def cache(cls):
        cls.query.delete()
        for row in get_objects(cls.event_target, cls.target_file):
            if row["LicCategory"] != "Real Estate":
                continue
            row_dict = cls.clean_data(row)
            obj = cls(**row_dict)
            db.session.add(obj)
            try:
                db.session.commit()
            except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.DataError) as e:
                db.session.rollback()

    @classmethod
    def clean_methods(cls):
        methods = {
            func[6:]: func
            for func in dir(cls)
            if callable(getattr(cls, func)) and func.startswith("clean")
        }
        methods.pop("data")
        methods.pop("methods")
        return methods

    @classmethod
    def clean_data(cls, row):
        data = {}

        clean_methods = cls.clean_methods()
        columns = set(x.name for x in cls.__table__.columns)

        for key, value in row.items():
            new_key = camelToSnake(key)
            if new_key not in columns:
                continue
            if new_key in clean_methods:
                func = getattr(cls, clean_methods[new_key])
                data[new_key] = func(value)
            else:
                data[new_key] = value.title()
        return data


class Realtor(IDModel):

    event_target = "ctl00$DefaultContent$RadGridLists$ctl00$ctl04$ctl00"
    target_file = "Individuals.txt"

    last_name = db.Column(db.String(100), nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False, index=True)

    # @classmethod
    # def cache(cls):
    #     for realtor in get_objects(cls.event_target, cls.target_file):
    #         print(realtor)
    #


class Broker(IDModel):

    event_target = "ctl00$DefaultContent$RadGridLists$ctl00$ctl06$ctl00"
    target_file = "Entities.txt"

    # id = db.Column(db.Integer, primary_key=True)

    lic_status = db.Column(
        db.Boolean, nullable=False, default=False, server_default=expression.true()
    )

    lic_number = db.Column(db.String(11), unique=True, nullable=False)

    legal_name = db.Column(db.String(100), nullable=True)
    expire_date = db.Column(db.DateTime)

    phone = db.Column(db.String(14), nullable=False)  # increase lengths
    fax = db.Column(db.String(14), nullable=False)  # increase lengths , make nullable
    # probably could clean these up later, ok for now

    address1 = db.Column(db.String(75), nullable=False)
    address1 = db.Column(db.String(75), nullable=True)

    city = db.Column(db.String(50), nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(2), nullable=False)

    @classmethod
    def clean_state(cls, value):

        if len(value) == 2:
            return value.upper()

    @classmethod
    def clean_zip(cls, value):

        match = re.search("\d+|$", value).group()
        if match:
            return int(match)

    @classmethod
    def clean_expire_date(cls, value):
        if value:
            return datetime.datetime.strptime(value, "%m/%d/%Y")

    @classmethod
    def clean_lic_status(cls, value):
        if value == "Active":
            return True
        return False


def get_uniques(brokers, key):

    values = set()
    max_val = 0
    for x in brokers:
        values.add(x[key])
        max_val = max(len(x[key]), max_val)
    return values, max_val
