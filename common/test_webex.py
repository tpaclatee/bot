import json
from unittest import TestCase

from common import conf
from common import webex


class Test(TestCase):
    def test_post_debug_message(self):
        r = webex.post_debug_message("Test debug message")
        self.assertTrue(r['roomType'], "Must have roomType in returned json")

    def test_webex_send_card(self):
        attachment = """
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "body": [        {
                "type": "Container",
                "items": [
                    {
                    "type": "TextBlock",
                    "text": "Unit test card",
                    "weight": "Bolder",
                    "size": "Medium",
                    "wrap": true
                     }
                ]
            }],
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.0"
            }
        }
        """
        card = json.loads(attachment, strict=False)
        c = webex.webex_send_card(card, "Unit test card", conf.bot_room_id)
        self.assertTrue(c['roomType'], "Must have roomType in returned json")

    def test_create_message_to_person(self):
        webex.create_message_to_person(conf.bot_debug_unit_test_person_id, "test message to person")
