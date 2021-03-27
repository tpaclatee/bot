import json

import pystache
from loguru import logger

from common import beep
from common import conf
from common import webex
from nagios import nagios_db


def post_to_chat(problems):
    logger.info(
        "Will post " + str(len(problems)) + " problems to chat.")

    for p in problems:
        card = create_nagios_card(p)
        c = webex.webex_send_card(card, "Problem from nagios", conf.bot_room_id)
        beep.do_beeps(
            "{} new problem posted to chat. To turn of beeps message @IOCBot /beepoff".format(p.ServiceName))
        p.WebexMessageID = c['id']
        nagios_db.save_problem(p)

    return problems


def create_nagios_card(problem, post_to_ioc_chat_button=True, posted_by=None):
    """Create an adaptive card to display problem"""
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
                "text": "[NAGIOS {{Status}}]({{ProblemURL}})",
                "weight": "Bolder",
                "size": "Medium",
                "wrap": true
                 },
                 {
                "type": "TextBlock",
                "text": "**Host1**",
                "weight": "default",
                "spacing": "None",
                "wrap": true
                 },
                {
                "type": "TextBlock",
                "text": "{{HostName}}",
                "weight": "default",
                "spacing": "None",
                "wrap": true
                 },
                 {
                "type": "TextBlock",
                "text": "**Service**",
                "weight": "default",
                "spacing": "None",
                "wrap": true
                 },                 
                {
                "type": "TextBlock",
                "text": "{{ServiceName}}",
                "weight": "default",
                "spacing": "None",
                "wrap": true
                 },
                 {
                "type": "TextBlock",
                "text": "**Last Check**",
                "weight": "default",
                "spacing": "None",
                "wrap": true
                 },
                {
                "type": "TextBlock",
                "text": "{{LastCheck}}",
                "weight": "default",
                "spacing": "None",
                "wrap": true
                 },
                 {
                "type": "TextBlock",
                "text": "**Duration**",
                "weight": "default",
                "spacing": "None",
                "wrap": true
                 },
                {
                "type": "TextBlock",
                "text": "{{Duration}}",
                "weight": "default",
                "spacing": "None",
                "wrap": true
                 },
                 
                 {
                "type": "TextBlock",
                "text": "**Attempt**",
                "weight": "default",
                "spacing": "None",
                "wrap": true
                 }, 
                {
                "type": "TextBlock",
                "text": "{{Attempt}}",
                "weight": "default",
                "spacing": "None",
                "wrap": true
                 },
                {
                "type": "TextBlock",
                "text": "**Status Information**",
                "weight": "default",
                "spacing": "None",
                "wrap": true
                 },
                {
                "type": "TextBlock",
                "text": "{{StatusInformation}}",
                "weight": "default",
                "spacing": "None",
                
                "wrap": true
                 }
                 {{{PostedBy}}}
            ]
        }],
        "actions": [
            {{{PostToIocChatButton}}}
        ],
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.0"
        }
    }
    """

    # Don't show post to ioc chat button once posted to main chat
    if post_to_ioc_chat_button:
        post_button = """
               {
                 "type": "Action.Submit",
                 "title": "Post to IOC Monitoring",
                 "style": "positive",
                 "id": "buttonPostIocChat",
                 "data": {
                   "ProblemKey": "{{ProblemKey}}",
                   "System":"Nagios"
                 }
               }
           """
        post_button = pystache.render(post_button, {'ProblemKey': problem.ProblemKey})
        problem.PostToIocChatButton = post_button
    else:
        problem.PostToIocChatButton = ""

    # Show who posted by on main chat
    if posted_by:
        tag = """
               ,
                {
                "type": "TextBlock",
                "text": "**Posted By**: {{PostedBy}}",
                "weight": "default",
                "spacing": "None",
                "wrap": true
                 }
           """
        tag = pystache.render(tag, {'PostedBy': posted_by})
        problem.PostedBy = tag
    else:
        problem.PostedBy = ""

    attachment = pystache.render(attachment, {'HostName': problem.HostName,
                                              'ServiceName': problem.ServiceName,
                                              'LastCheck': problem.LastCheck,
                                              'Attempt': problem.Attempt,
                                              'ProblemURL': "https://nagios.umd.edu/nagios/cgi-bin/status.cgi?hostgroup=ioc-host&style=detail&servicestatustypes=28&sorttype=1&sortoption=4&limit=250",
                                              'StatusInformation': problem.StatusInformation,
                                              'Status': problem.Status,
                                              'Duration': problem.Duration,
                                              'ImgUrl': conf.bot_url + '/static/nagios.png',
                                              'ProblemKey': problem.ProblemKey,
                                              'PostToIocChatButton': problem.PostToIocChatButton,
                                              'PostedBy': problem.PostedBy
                                              })
    rendered = json.loads(attachment, strict=False)
    return rendered
