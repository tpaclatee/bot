import jsons

from common import conf
from common import tests
from common import webex
from common.db import row2dict
from dynatrace import dynatrace_db
from dynatrace import dynatrace_webex


class Test(tests.BotTestCase):
    def test_create_dynatrace_card(self):
        problem = dynatrace_db.get_problem_by_pid("-6505945424145176375")
        s = row2dict(problem)
        c = dynatrace_webex.create_dynatrace_card(s)
        self.assertTrue(c['content']['type'] == 'AdaptiveCard', "Must return type of AdaptiveCard")

    def test_webex_send_dynatrace_card(self):
        problem = dynatrace_db.get_problem_by_pid("-6505945424145176375")
        card = dynatrace_webex.create_dynatrace_card(jsons.dump(problem))
        c = webex.webex_send_card(card, "Backup No Msg", conf.bot_room_id)
        self.assertTrue(not c.get('message'), "Must not return an error message")
        self.assertTrue(c['id'] is not None, "Must return a message ID")
