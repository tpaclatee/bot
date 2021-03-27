from unittest import TestCase

from nagios import nagios_scraper

from common import tests


class Test(tests.BotTestCase):
    def test_scrape(self):
        rows = nagios_scraper.scrape()
        self.assertTrue(len(rows) > 10, "Should scrape more than 10 problems")
