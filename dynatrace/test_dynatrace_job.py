from common import tests
from dynatrace import dynatrace_db
from dynatrace import dynatrace_job


class Test(tests.BotTestCase):
    def test_sync_dynatrace(self):
        dynatrace_job.sync_dynatrace()

    def test_create_new_chat_card(self):
        p = dynatrace_db.get_problem_by_pid("-6505945424145176375")
        dynatrace_job.create_new_chat_card(p)
        pdb = dynatrace_db.get_problem_by_id(p.ProblemID)
        self.assertTrue(pdb.WebexMessageID, "Must store the message ID after posting card to webex chat")
