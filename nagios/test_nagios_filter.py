from unittest import TestCase

from nagios import nagios_filter
from nagios.nagios_db import NagiosProblem

from common import tests


class Test(tests.BotTestCase):
    def test_nagios_problems(self):
        problems = nagios_filter.get_alerts()
        self.assertTrue("qa" not in problems[0].ServiceName, "Should not report QA systems")
        self.assertTrue(len(problems) == 1, "Should be 1 active critical problem")
        self.assertTrue(problems[0].ProblemKey == 'ACTIVE',
                        "Should be air temp problem")

    def test_filter_problem_kfs_maint(self):
        p = NagiosProblem()
        p.ServiceName = "kfs heartbeat prod"
        # See https://unixtime.guru/
        p.Created = 1614469687
        f = nagios_filter.filter_problem_kfs_maint([p])
        self.assertTrue(len(f) == 1, "Should not filter 18:48 outside maint window")
        p.Created = 1614480487
        f = nagios_filter.filter_problem_kfs_maint([p])
        self.assertTrue(len(f) == 0, "Should  filter 21:48 inside maint window")
        p2 = NagiosProblem()
        f = nagios_filter.filter_problem_kfs_maint([p, p2])
        self.assertTrue(len(f) == 1, "Should keep problem")

    def test_filter_morning_maint(self):
        p = NagiosProblem()
        p.ServiceName = "advise Detailed Health Check"
        # See https://unixtime.guru/
        p.Created = 1614423487
        f = nagios_filter.filter_problem_morning_maint([p])
        self.assertTrue(len(f) == 1, "Should not filter 5:58 outside maint window")
        p.Created = 1614425467
        f = nagios_filter.filter_problem_morning_maint([p])
        self.assertTrue(len(f) == 0, "Should  filter 6:31 inside maint window")
        p.Created = 1614426067
        f = nagios_filter.filter_problem_morning_maint([p])
        self.assertTrue(len(f) == 1, "Should  not filter 6:41 outside maint window")
        p2 = NagiosProblem()
        f = nagios_filter.filter_problem_morning_maint([p, p2])
        self.assertTrue(len(f) == 2, "Should keep both problems / not filter either")

    def test_filter_problem_minutes(self):
        p1 = NagiosProblem()
        p2 = NagiosProblem()
        p3 = NagiosProblem()
        p1.Duration = "0d 0h 2m 45s"
        p2.Duration = "0d 0h 6m 45s"
        p3.Duration = "0d 0h 20m 45s"
        problems = [p1, p2, p3]
        filtered = nagios_filter.filter_problem_minutes(problems, minutes_to_wait=10)
        self.assertTrue(len(filtered) == 1, "Should have filtered all but 20m problem")
