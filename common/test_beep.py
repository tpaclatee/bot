from common import beep
from common import tests
from common.beep import Beep


class Test(tests.BotTestCase):

    def test_save_load_delete_beep(self):
        b = Beep()
        b.PersonEmail = "cmann@umd.edu"
        b.PersonID = "234r315r34534"
        beep.save_beep(b)
        b = beep.get_beep_by_person_email("cmann@umd.edu")
        self.assertTrue(b.Created, "Should have a created date auto generated")
        self.assertTrue(b.PersonID == "234r315r34534", "Should have proper person id")
        beep.delete_beep("cmann@umd.edu")
        b = beep.get_beep_by_person_email("cmann@umd.edu")
        self.assertTrue(b is None, "should not find deleted beep")
