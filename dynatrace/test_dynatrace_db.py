from common import tests
from dynatrace import dynatrace_db


class Test(tests.BotTestCase):
    def test_create_delete_save_problem(self):
        try:
            problem = dynatrace_db.get_problem_by_pid("-6505945424145176375")
            self.assertTrue(problem.State == 'RESOLVED')
        except:
            self.fail()
