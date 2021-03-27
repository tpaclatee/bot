from datetime import datetime, timezone

from webexteamsbot.models import Response

from common import conf
from common import webex
from nagios import nagios_db
from nagios import nagios_webex


def handle_card_action_nagios(action, person):
    """Posts card to IOC monitoring chat"""

    r = Response()
    p = nagios_db.get_problem_by_key(action['ProblemKey'])
    if not p:
        r.text = "Problem is no longer active {}. Cannot post to main IOC chat. ".format(person.displayName)
        return r
    if p.PostedToIocChatBy:
        r.text = "{} already posted to chat by {}. Cannot post to main IOC chat.".format(p.ProblemKey,
                                                                                         p.PostedToIocChatBy)
        # r.attributes["parentId"] = p.WebexMessageID
        return r

    card = nagios_webex.create_nagios_card(p, post_to_ioc_chat_button=False, posted_by=person.displayName)
    c = webex.webex_send_card(card, "Problem posted from Nagios", conf.bot_room_id_ioc_monitoring)
    p.PostedToIocChatBy = person.displayName
    nagios_db.save_problem(p)
    r.text = "Posted to IOC monitoring chat by {} at {}".format(person.displayName, datetime.now(timezone.utc))
    # r.attributes["parentId"] = p.WebexMessageID
    return r
