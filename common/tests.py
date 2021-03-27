import json
from unittest import TestCase

from common import conf
from common.db import dal
from dynatrace import dynatrace_db
from dynatrace.dynatrace_db import DynatraceProblem
from nagios import nagios_db
from nagios.nagios_db import NagiosProblem


class BotTestCase(TestCase):
    def setUp(self):
        print("Switch to unit test database")
        dal.db_init(unit_testing=True)
        dal.session.query(NagiosProblem).delete()
        dal.session.commit()
        dal.session.query(DynatraceProblem).delete()
        dal.session.commit()
        problems = self.load_nagios_problems_from_file("nagios_problems.json")
        nagios_db.save_problems(problems)
        problems = self.load_dynatrace_problems_from_file("dynatrace_problems.json")
        dynatrace_db.save_problems(problems)

    def load_nagios_problems_from_file(self, file_name):
        with open(conf.app_base_path + "/unit_test_data/" + file_name) as f:
            data = json.load(f)
        final = []
        for d in data:
            problem = NagiosProblem(**d)
            final.append(problem)
        return final

    def load_dynatrace_problems_from_file(self, file_name):
        with open(conf.app_base_path + "/unit_test_data/" + file_name) as f:
            data = json.load(f)
        final = []
        for d in data:
            problem = DynatraceProblem(**d)
            final.append(problem)
        return final
