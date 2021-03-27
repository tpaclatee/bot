from datetime import datetime, timezone, timedelta

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from common import conf


# TODO:  check_same_thread - need to see if it corrupts data on new sqllite3 file based
# TODO: may need to switch to pool to work with oracle properly


Base = declarative_base()


class DataAccessLayer:
    connection = None
    Session = None
    session = None
    engine = None
    conn_string = None
    metadata = None

    def db_init(self, unit_testing=False):
        if conf.sqlalchemy_debug_sql == 1:
            dbg = True
        else:
            dbg = False
        if unit_testing:
            self.engine = create_engine('sqlite:///' + conf.sql_lite_unit_db, echo=dbg,
                                        connect_args={'check_same_thread': False})
        else:
            self.engine = create_engine('sqlite:///' + conf.sql_lite_db, echo=dbg,
                                        connect_args={'check_same_thread': False})
        self.Session = sessionmaker(bind=self.engine, autoflush=False)
        self.session = self.Session()
        self.metadata = MetaData()
        self.metadata.create_all(self.engine)

        self.connection = self.engine.connect()
        Base.metadata.create_all(self.engine)


dal = DataAccessLayer()


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


def time_delta_minutes(stamp, minutes):
    """Has more than x minutes past since stamp (stored in Unix epoch)"""
    created = datetime.fromtimestamp(int(stamp), timezone.utc)
    now = datetime.now(timezone.utc)
    min_30 = created + timedelta(minutes=int(minutes))
    if now > min_30:
        return True
