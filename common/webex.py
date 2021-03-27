import requests

from common import conf

headers = {
    "content-type": "application/json; charset=utf-8",
    "authorization": "Bearer " + conf.teams_token,
}


def webex_send_card(card, backup_message, room_id):
    c = create_message_with_attachment(
        room_id, msgtxt=backup_message, attachment=card
    )
    return c


def create_message_with_attachment(rid, msgtxt, attachment):
    """Used to create card in chat"""

    url = "https://api.ciscospark.com/v1/messages"
    data = {"roomId": rid, "attachments": [attachment], "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def create_message(rid, msgtxt):
    """Used to create card in chat"""

    url = "https://api.ciscospark.com/v1/messages"
    data = {"roomId": rid, "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def create_message_to_person(person_id, msgtxt):
    """Used to create card in chat"""

    url = "https://api.ciscospark.com/v1/messages"
    data = {"toPersonId": person_id, "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def post_debug_message(msgtxt):
    return create_message(conf.bot_room_id_debug, msgtxt)
