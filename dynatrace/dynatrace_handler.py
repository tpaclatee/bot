import json
from datetime import datetime, timezone

import jsons
import pystache
import requests
from flask import request, jsonify
from webexteamsbot.models import Response

from common import conf
from common import webex
from dynatrace import dynatrace_db
from dynatrace import dynatrace_webex
from dynatrace.dynatrace_db import DynatraceProblem


def handle_problem():
    """Dynatrace webhook will post to the method when a problem is opened or resolved"""
    if request.headers.get('AUTHORIZATION') != "Bearer " + conf.dt_bearer_token:
        print('''Missing authorization token from dynatrace or token not defined in .env file.  Review README.md.''')
        return jsonify({"message": "ERROR: Unauthorized"}), 401

    problem = request.json
    problem['ImpactedEntities'] = jsons.dumps(problem['ImpactedEntities'])
    problem['ProblemDetailsJSON'] = jsons.dumps(problem['ProblemDetailsJSON'])
    p = DynatraceProblem(**problem)
    dynatrace_db.save_problem(p)
    return problem


def get_problems():
    r = requests.get(
        conf.dt_api_url + '/api/v2/problems/',
        headers={'Authorization': "Api-Token " + conf.dt_api_token}

    );
    return r.json()


def update_problem_comment(pid, comment):
    """TODO: dead code, may come back and play with it, it works"""
    comment_json = """
    {
     "message": "{{Comment}}",
     "context": "Webex"
    }
    """
    comment_json = pystache.render(comment_json, {'Comment': comment})
    comment_json = json.loads(comment_json)
    r = requests.post(
        conf.dt_api_url + '/api/v2/problems/' + pid + '/comments',
        headers={'Authorization': "Api-Token " + conf.dt_api_token},
        json=comment_json
    );
    return r


def handle_card_action_dynatrace(action, person):
    """Posts card to IOC monitoring chat"""

    r = Response()
    p = dynatrace_db.get_problem_by_pid(action['PID'])
    if not p:
        r.text = "Problem is no longer active {}. Cannot post to main IOC chat. ".format(person.displayName)
        return r
    if p.PostedToIocChatBy:
        r.text = "{} already posted to chat by {}. Cannot post to main IOC chat again.".format(p.ProblemID, p.PostedToIocChatBy)
        return r

    card = dynatrace_webex.create_dynatrace_card(vars(p), post_to_ioc_chat_button=False, posted_by=person.displayName)
    c = webex.webex_send_card(card, "Problem posted from Dynatrace", conf.bot_room_id_ioc_monitoring)
    p.PostedToIocChatBy = person.displayName
    dynatrace_db.save_problem(p)
    r.text = "{} posted to IOC monitoring chat by {} at {}".format(p.ProblemID, person.displayName,
                                                                   datetime.now(timezone.utc))
    return r
