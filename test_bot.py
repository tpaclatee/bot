import bot
import jsons

import bot
from common import conf
from common import tests
from common.db import row2dict
from dynatrace import dynatrace_db


class Test(tests.BotTestCase):

    def test_handle_dynatrace_problem_missing_auth_header(self):
        problem = dynatrace_db.get_problem_by_pid("-6505945424145176375")
        p = row2dict(problem)
        client = bot.bot.test_client()
        response = client.post('/dynatraceProblem',
                               data=p,
                               content_type='application/json',
                               headers={'AUTHORIZATION': 'Bad value'}
                               )
        self.assertTrue(response.status_code == 401, "Must return 401 unauthorized")

    def test_handle_dynatrace_problem_good_auth_header(self):
        problem = dynatrace_db.get_problem_by_pid("-6505945424145176375")
        p = jsons.dumps(problem, strip_privates=True)
        client = bot.bot.test_client()
        response = client.post('/dynatraceProblem',
                               data=p,
                               content_type='application/json',
                               headers={'AUTHORIZATION': 'Bearer ' + conf.dt_bearer_token}
                               )
        self.assertTrue(response.status_code == 200, "Must return 200 if good bearer token")
