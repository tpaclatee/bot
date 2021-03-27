import traceback
from time import time

from sqlalchemy import Column, String

from common import webex
from common.db import dal, Base
import time


def save_beep(beep):
    if not beep.Created:
        beep.Created = int(time.time())
    if get_beep_by_person_email(beep.PersonEmail):
        dal.session.merge(beep)
    else:
        dal.session.add(beep)
    dal.session.commit()


def get_all_beeps():
    q = dal.session.query(Beep)
    beeps = q.all()
    return beeps


def get_beep_by_person_email(person_email):
    p = ''
    try:
        p = dal.session.query(Beep).filter_by(PersonEmail=person_email).first()
    except:
        traceback.print_exc()
        print("error")
    return p


def delete_beep(person_email):
    p = get_beep_by_person_email(person_email)
    if p:
        dal.session.delete(p)
        dal.session.commit()


class Beep(Base):
    __tablename__ = 'beep'
    PersonEmail = Column(String, primary_key=True)
    PersonID = Column(String)
    Created = Column(String)


def beep_on(incoming_msg):
    if get_beep_by_person_email(incoming_msg.personEmail):
        return "Beep on error is already on for user {}".format(incoming_msg.personEmail)
    else:
        b = Beep()
        b.PersonID = incoming_msg.personId
        b.PersonEmail = incoming_msg.personEmail
        save_beep(b)
        return "Beep on error is on for user {}".format(b.PersonEmail)


def beep_off(incoming_msg):
    b = Beep()
    b.PersonID = incoming_msg.personId
    b.PersonEmail = incoming_msg.personEmail
    if get_beep_by_person_email(incoming_msg.personEmail):
        delete_beep(incoming_msg.personEmail)
        return "Beep is now off for user {}".format(b.PersonEmail)
    else:
        return "Beep was not on for user {}, so no need to turn it off.".format(b.PersonEmail)


def beep_test(incoming_msg):

    print("person id:" + incoming_msg.personId)
    webex.create_message_to_person(incoming_msg.personId, "Testing beep")

    return "Testing beep volume for {}".format(incoming_msg.personEmail)


def do_beeps(message):
    """Beep all registered users"""
    beeps = get_all_beeps()
    for b in beeps:
        webex.create_message_to_person(b.PersonID, message)
