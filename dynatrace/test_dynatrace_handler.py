from common import tests
from dynatrace import dynatrace_handler


class Person:
    displayName = "Christopher David Mann"


class Test(tests.BotTestCase):
    def test_handle_card_action_dynatrace(self):
        action = {'PID': '-6505945424145176375', 'System': 'Dynatrace'}
        person = Person()
        dynatrace_handler.handle_card_action_dynatrace(action, person)

        # self.assertTrue(problem.State == 'RESOLVED')
