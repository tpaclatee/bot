from loguru import logger

from common import beep
from common import conf
from common import webex
from common.db import dal, time_delta_minutes
from dynatrace import dynatrace_db
from dynatrace import dynatrace_webex
from dynatrace.dynatrace_db import DynatraceProblem


def sync_dynatrace():
    problems = dal.session.query(DynatraceProblem).filter_by(State='OPEN').all()
    logger.info("Will wait to post " + conf.wait_to_post_minutes + " since creation")
    for p in problems:
        if time_delta_minutes(p.Created, minutes=conf.wait_to_post_minutes):
            if not p.WebexMessageID:
                create_new_chat_card(p)
                beep.do_beeps(
                    "{} new problem posted to chat. To turn of beeps message @IOCBot /beepoff".format(p.ProblemTitle))


def create_new_chat_card(p):
    """Create new chat card and save message ID so we can update the card later"""
    card = dynatrace_webex.create_dynatrace_card(vars(p))
    c = webex.webex_send_card(card, "Problem posted from Dynatrace", conf.bot_room_id)
    p.WebexMessageID = c['id']
    dynatrace_db.save_problem(p)
