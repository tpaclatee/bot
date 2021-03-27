import nagios.nagios_filter
from common import conf
from common import tests
from common import webex
from nagios import nagios_test_util
from nagios import nagios_webex


class Test(tests.BotTestCase):
    def test_post_to_chat(self):
        problems = nagios.nagios_filter.get_alerts()
        if len(problems) > 10:
            self.fail("Should not be more than 10 active problems")

        # if we happen to have more than two active problems try to post 2 of them
        if len(problems) > 1:
            subset = [problems[0], problems[1]]
            problems = nagios_webex.post_to_chat(subset)
            self.assertTrue(problems[0].WebexMessageID,
                            "Problem 0 should have a message ID set")
            self.assertTrue(problems[1].WebexMessageID,
                            "Problem 1 should have a message ID set")

    def test_webex_send_nagios_card(self):
        card = nagios_webex.create_nagios_card(nagios_test_util.get_test_nagios_problem())
        c = webex.webex_send_card(card, "Backup No Msg", conf.bot_room_id)
        self.assertTrue(not c.get('message'), "Must not return an error message")
        self.assertTrue(c['id'] is not None, "Must return a message ID")
