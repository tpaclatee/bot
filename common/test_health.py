from datetime import datetime

import common.health
from common import tests


class Test(tests.BotTestCase):
    def test_canary(self):
        b = datetime(2017, 11, 28, 23, 00, 1, 342380)
        self.assertTrue(common.health.canary(b) is True, "Must be true when minute is 00")
        b = datetime(2017, 11, 28, 23, 30, 1, 342380)
        self.assertTrue(common.health.canary(b) is True, "Must be true when minute is 30")
        b = datetime(2017, 11, 28, 23, 31, 1, 342380)
        self.assertTrue(common.health.canary(b) is False, "Must be false otherwise")

    def test_active_problems_printout(self):
        print_out = common.health.active_problems_printout()
        self.assertTrue(len(print_out) > 1, "Should have a printout")

    def test_check_bot_up(self):
        common.health.check_bot_up()
