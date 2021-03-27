from dynatrace import dynatrace_handler
from common import tests


class Test(tests.BotTestCase):

    def test_update_dynatrace_problem_comment(self):
        dynatrace_handler.update_problem_comment("-6333242050298929991_1613054691029V2",
                                                 "Test comment")
