from common import tests
from nagios import nagios_handler


class Person:
    displayName = "Christopher David Mann"


class Test(tests.BotTestCase):
    def test_handle_card_action_dynatrace(self):
        action = {'ProblemKey': 'ACTIVE', 'System': 'Nagios'}
        person = Person()
        nagios_handler.handle_card_action_nagios(action, person)

        # self.assertTrue(problem.State == 'RESOLVED')
