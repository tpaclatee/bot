from unittest import TestCase
from nagios import nagios_job
from nagios.nagios_db import NagiosProblem
from common import tests


class Test(tests.BotTestCase):
    def test_sync_nagios(self):
        nagios_job.sync_nagios()

    def test_removed_problems(self):
        p1 = NagiosProblem()
        p1.ProblemKey = "1"
        p2 = NagiosProblem()
        p2.ProblemKey = "2"
        p3 = NagiosProblem()
        p3.ProblemKey = "3"
        orig = [p1, p2, p3]
        latest = [p1, p2]
        result = nagios_job.removed_problems(orig, latest)
        self.assertTrue(result[0] == "3", "3 should have been removed")
        self.assertTrue(len(result) == 1, "Only 1 removed")
        latest = [p1]
        result = nagios_job.removed_problems(orig, latest)
        self.assertTrue(len(result) == 2, "Two should have been removed")
        latest = [p1, p2, p3]
        result = nagios_job.removed_problems(orig, latest)
        self.assertTrue(len(result) == 0, "None removed")
