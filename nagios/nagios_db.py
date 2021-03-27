import datetime
from dateutil import tz
from time import time
from pprint import pformat

from durations_nlp import Duration
from sqlalchemy import Column, String

from common.db import dal, Base

import traceback


def save_problem(nagios_problem):
    """Save new NagiosProblem to database or merge with existing"""
    if not nagios_problem.Created:
        nagios_problem.Created = int(time())
    if get_problem_by_key(nagios_problem.ProblemKey):
        dal.session.merge(nagios_problem)
    else:
        dal.session.add(nagios_problem)
    dal.session.commit()


def save_problems(problems):
    for p in problems:
        save_problem(p)


def get_all_problems():
    q = dal.session.query(NagiosProblem)
    problems = q.all()
    return problems


def get_problems_by_keys(problem_keys):
    result = []
    for k in problem_keys:
        result.append(get_problem_by_key(k))
    return result


def get_problem_by_key(problem_key):
    """Get NagiosProblem by  pid"""
    p = ''
    try:
        p = dal.session.query(NagiosProblem).filter_by(ProblemKey=problem_key).first()
    except:
        traceback.print_exc()
        print("error")
    return p


def delete_problem(problem_key):
    """Delete a problem from the database"""
    p = get_problem_by_key(problem_key)
    if p:
        dal.session.delete(p)
        dal.session.commit()


def delete_problems(problems):
    for p in problems:
        delete_problem(p.ProblemKey)


def delete_all_problems():
    problems = get_all_problems()
    for p in problems:
        delete_problem(p.ProblemKey)


class NagiosProblem(Base):
    __tablename__ = 'nagios_problem'
    ProblemKey = Column(String, primary_key=True)  # HostName + ServiceName
    HostName = Column(String)
    ServiceName = Column(String)
    AcknowledgedHost = Column(String)
    AcknowledgedService = Column(String)
    NotificationDisabledHost = Column(String)
    NotificationDisabledService = Column(String)
    ScheduledDowntimeHost = Column(String)
    ScheduledDowntimeService = Column(String)
    PassiveChecksOnlyHost = Column(String)
    PassiveChecksOnlyService = Column(String)
    HostIP = Column(String)
    Status = Column(String)
    LastCheck = Column(String)
    Duration = Column(String)
    Attempt = Column(String)
    StatusInformation = Column(String)
    Created = Column(String)
    WebexMessageID = Column(String)
    PostedToIocChatBy = Column(String)

    def duration_parsed(self):
        return Duration(self.Duration)

    def created_from_unix_gmt(self):
        local_zone = tz.tzlocal()
        dt = datetime.datetime.fromtimestamp(int(self.Created))
        dt.replace(tzinfo=local_zone)

        return dt

    def to_string(self):
        return pformat(vars(self), indent=4, width=1)
