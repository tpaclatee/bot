import time

from sqlalchemy import Column, String

from common.db import Base, dal


class DynatraceProblem(Base):
    __tablename__ = 'dynatrace_problem'
    ProblemID = Column(String, primary_key=True)
    PID = Column(String)
    ProblemTitle = Column(String)
    Created = Column(String)
    AcknowledgeUser = Column(String)
    AcknowledgeDate = Column(String)
    State = Column(String)
    ProblemDetailsText = Column(String)
    ProblemDetailsMarkdown = Column(String)
    ProblemDetailsJSON = Column(String)
    ProblemSeverity = Column(String)
    ImpactedEntities = Column(String)
    ImpactedEntity = Column(String)
    ProblemURL = Column(String)
    Tags = Column(String)
    WebexMessageID = Column(String)
    PostedToIocChatBy = Column(String)

def save_problem(problem):
    """Save new problem to database or merge with existing"""
    problem.Created = int(time.time())
    if get_problem_by_id(problem.ProblemID):
        dal.session.merge(problem)
    else:
        dal.session.add(problem)
    dal.session.commit()


def save_problems(problems):
    for p in problems:
        save_problem(p)


def get_problem_by_id(problem_id):
    """Get problem by problem id"""
    p = dal.session.query(DynatraceProblem).filter_by(ProblemID=problem_id).first()
    return p


def get_problem_by_pid(pid):
    """Get problem by  pid"""
    p = dal.session.query(DynatraceProblem).filter_by(PID=pid).first()
    return p


def delete_problem(problem_id):
    """Delete a problem from the database"""
    p = get_problem_by_id(problem_id)
    if p:
        dal.session.delete(p)
        dal.session.commit()
