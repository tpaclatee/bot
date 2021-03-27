from common import conf
from common.db import dal
from nagios.nagios_db import NagiosProblem


def get_alerts(filter_minutes=int(conf.wait_to_post_minutes), filter_posted=True, filter_off=False):
    """Get NagiosProblem by  pid"""

    q = dal.session.query(NagiosProblem)

    if filter_off:
        return q.all()

    q = filter_icons(q)

    if filter_posted:
        q = q.filter_by(WebexMessageID=None)

    q = q.filter_by(Status="CRITICAL")

    q = q.filter(~NagiosProblem.ServiceName.contains('%qa%'))

    q = q.filter(~NagiosProblem.HostName.contains('%qa%'))

    filtered = q.all()
    filtered = filter_problem_minutes(filtered, filter_minutes)
    filtered = filter_problem_kfs_maint(filtered)
    filtered = filter_problem_morning_maint(filtered)
    return filtered


def filter_icons(q):
    q = q.filter_by(NotificationDisabledHost=None)
    q = q.filter_by(NotificationDisabledService=None)
    q = q.filter_by(ScheduledDowntimeHost=None)
    q = q.filter_by(ScheduledDowntimeService=None)
    q = q.filter_by(AcknowledgedHost=None)
    q = q.filter_by(AcknowledgedService=None)
    return q;


def filter_problem_kfs_maint(problems):
    """Filter out KFS maintenance window running approx 21:00-23:00 daily"""
    final_problems = []
    for p in problems:
        if "kfs" in vars(p).get("ServiceName", ""):
            if "heartbeat" in vars(p).get("ServiceName", ""):
                # See https://unixtime.guru/
                created = p.created_from_unix_gmt().time()
                if not (20 <= created.hour <= 23):
                    final_problems.append(p)
        else:
            final_problems.append(p)

    return final_problems


def filter_problem_morning_maint(problems):
    """Filter out morning maint approx 06:15-06:30 daily"""
    final_problems = []
    for p in problems:
        if "Detailed" in vars(p).get("ServiceName", ""):
            # See https://unixtime.guru/
            created = p.created_from_unix_gmt().time()
            exclude = False
            if created.hour == 6:
                if 0 <= created.minute <= 40:
                    exclude = True
            if not exclude:
                final_problems.append(p)
        else:
            final_problems.append(p)

    return final_problems


def filter_problem_minutes(problems, minutes_to_wait):
    """Filter out problems with duration shorter than x mins"""
    final_problems = []
    for p in problems:
        duration = p.duration_parsed()
        minutes = duration.to_minutes()
        if minutes > minutes_to_wait:
            final_problems.append(p)
    return final_problems
