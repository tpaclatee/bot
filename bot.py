import traceback

import requests
from loguru import logger
from waitress import serve
from webexteamsbot import TeamsBot

from common import webex
from common.beep import beep_on, beep_off, beep_test
# TODO Point at Oracle
from common.conf import bot_email, teams_token, bot_url, bot_app_name, bot_port, env
from common.db import dal
from common.job import background_schedule
from dynatrace.dynatrace_handler import handle_problem, handle_card_action_dynatrace

from nagios import nagios_handler

# Create a Bot Object

try:
    dal.db_init()

    bot = TeamsBot(
        bot_app_name,
        teams_bot_token=teams_token,
        teams_bot_url=bot_url,
        teams_bot_email=bot_email,
        webhook_resource_event=[{"resource": "messages", "event": "created"},
                                {"resource": "attachmentActions", "event": "created"}]
    )


    def do_room_id(incoming_msg):
        return "This room ID is - {}".format(incoming_msg.roomId)


    def get_attachment_actions(attachmentid):
        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": "Bearer " + teams_token,
        }

        url = "https://api.ciscospark.com/v1/attachment/actions/" + attachmentid
        response = requests.get(url, headers=headers)
        return response.json()


    def handle_card_action(api, incoming_msg):
        """Webex calls this webhook when buttons are pressed on adaptive card"""
        m = get_attachment_actions(incoming_msg["data"]["id"])
        person = bot.teams.people.get(m["personId"])
        action = m["inputs"]  # TODO handle different actions
        if action.get('System') == 'Dynatrace':
            return handle_card_action_dynatrace(action, person)
        elif action.get('System') == 'Nagios':
            return nagios_handler.handle_card_action_nagios(action, person)
        # TODO: Add for handlers nagios and spectrum


    #  print(incoming_msg)

    # TODO: Cloudwatch SNS queue

    # TODO: handle_spectrum_problem

    # TODO: Change nagios to use a nagios handler
    # Edit https://gitlab.umd.edu/it-platform/nagios-config/blob/master/misccommands.cfg
    # See example spark integration disable: https://gitlab.umd.edu/it-platform/nagios-config/blob/master/misccommands.cfg#L134-165 was the cisco spark integration (disabled)
    # this would be better done as an alert handler, rather than screen scraping, you could just process 'hard' notifications

    # TODO: net mri (e.g. shows network link down) https://docs.infoblox.com/download/attachments/31590296/NetMRI_API_Guide.pdf?version=1&modificationDate=1550472522610&api=v2

    # TODO: handle Aruba: https://dashboard.capenetworks.com/circles
    # ARUBA PYTHON EXAMPLE: https://developer.arubanetworks.com/aruba-uxi/docs/python-api-example-query-sensors-reporting-an-ongoing-issue

    bot.add_new_url("/dynatraceProblem", "dynatraceProblem", handle_problem)

    bot.set_help_message("Welcome to the IOCBot! You can use the following commands:\n")

    bot.add_command("/room", "Room ID", do_room_id)

    bot.add_command("/beepon", "Turn on beep on error", beep_on)

    bot.add_command("/beepoff", "Turn off beep on error", beep_off)

    bot.add_command("/beeptest", "Test sending you a beep to check volume etc", beep_test)

    bot.add_command("attachmentActions", "*", handle_card_action)

    # TODO: need to create SQL object in the background thread
    background_schedule()

    if __name__ == "__main__":
        # Run Bot
        if env == 'dev':
            bot.run(host="0.0.0.0", port=bot_port)
        else:
            # Production must run using waitress
            serve(bot, host='0.0.0.0', port=bot_port)
except:
    ex = traceback.format_exc()
    logger.error(ex)
    ex = traceback.format_exc(1)
    webex.post_debug_message("```" + ex + "```")
