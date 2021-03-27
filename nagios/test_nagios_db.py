from unittest import TestCase

import nagios.nagios_filter
from nagios.nagios_db import NagiosProblem

from nagios import nagios_db

from common import tests


class Test(tests.BotTestCase):



    def test_get_problem_by_key(self):
        p = nagios_db.get_problem_by_key('ACTIVE')
        self.assertTrue(p.ProblemKey == 'ACTIVE',
                        "Should be active problem")

    def test_get_all_problems(self):
        problems = nagios_db.get_all_problems()
        self.assertTrue(len(problems) > 1,
                        "Should be more than one problem in DB")

    def test_get_problems_by_keys(self):
        p = nagios_db.get_problems_by_keys(['ACTIVE'])
        self.assertTrue(p[0].ProblemKey == 'ACTIVE',
                        "Should have found active problem")

    def test_delete_problem(self):
        nagios_db.delete_problem('ACTIVE')
        p = nagios_db.get_problem_by_key('ACTIVE')
        self.assertTrue(p is None,
                        "Should have deleted active problem")

    def test_delete_all_problems(self):
        nagios_db.delete_all_problems()
        p = nagios_db.get_all_problems()
        self.assertTrue(len(p) == 0,
                        "Should have deleted active problems")
