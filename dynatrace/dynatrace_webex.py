import json

import jsons
import pystache


def create_dynatrace_card(problem, post_to_ioc_chat_button=True, posted_by=None):
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
                    "text": "[{{ProblemID}}]({{ProblemURL}}) - {{ImpactedEntity}}",
                    "wrap" : true
                }
                {{{SplunkHealthCheckLookup}}}
                {{{PostedBy}}}
            ]
        }],
            "actions": [
        
              {
                "type": "Action.ShowCard",
                "title": "Show Details",
                "card": {
                  "type": "AdaptiveCard",
                  "body": [
                    {
                        "type": "TextBlock",
                        "text": "{{ProblemDetailsMarkdown}}",
                        "wrap" : true,
                        "id": "problemDetails"
                    }
                  ],
                  "actions": [ 
                  ]
                }
              }
              {{{PostToIocChatButton}}}
            ],
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.0"
        }
    }
    """
    entities = jsons.loads(problem['ImpactedEntities'])
    for entity in entities:
        if entity['type'] == 'HTTP_CHECK':
            http_check_id = entity['entity']
            splunk = """
            ,  {
                "type": "TextBlock",
                "text": "[Splunk Health Check Response](https://www.splunk.umd.edu:8000/en-US/app/UMD_dit/search?earliest=-48h%40h&latest=now&q=search%20index%3D%22dit_linux%22%20host%3D%22activegate2.it-eng-mgmt.aws.umd.edu%22%20{{HTTP_CHECK}}%20response&display.page.search.mode=fast&dispatch.sample_ratio=1&display.general.type=events&display.page.search.tab=events&display.events.timelineEarliestTime=1613469600&display.events.timelineLatestTime=1613473200&sid=1613492487.5811288)"
            }
            """
            splunk = pystache.render(splunk, {'HTTP_CHECK': http_check_id})
            problem['SplunkHealthCheckLookup'] = splunk
        else:
            problem['SplunkHealthCheckLookup'] = ''
    # Don't show post to ioc chat button once posted to main chat
    if post_to_ioc_chat_button:
        post_button = """
        ,
            {
              "type": "Action.Submit",
              "title": "Post to IOC Monitoring",
              "style": "positive",
              "id": "buttonPostIocChat",
              "data": {
                "PID": "{{PID}}",
                "System":"Dynatrace"
              }
            }
        """
        post_button = pystache.render(post_button, {'PID': problem['PID']})
        problem['PostToIocChatButton'] = post_button
    else:
        problem['PostToIocChatButton'] = ""

    # Show who posted by on main chat
    if posted_by:
        tag = """
               ,
                {
                "type": "TextBlock",
                "text": "**Posted By**: {{PostedBy}}",
                "weight": "default",
                "spacing": "medium",
                "wrap": true
                 }
            """
        tag = pystache.render(tag, {'PostedBy': posted_by})
        problem['PostedBy'] = tag
    else:
        problem['PostedBy'] = ""

    attachment = pystache.render(attachment, {'ProblemID': problem['ProblemID'],
                                              'State': problem['State'],
                                              'ProblemTitle': problem['ProblemTitle'],
                                              'ProblemDetailsMarkdown': problem['ProblemDetailsMarkdown'],
                                              'ProblemURL': problem['ProblemURL'],
                                              'PID': problem['PID'],
                                              'ImpactedEntity': problem['ImpactedEntity'],
                                              'SplunkHealthCheckLookup': problem.get('SplunkHealthCheckLookup'),
                                              'PostToIocChatButton': problem.get('PostToIocChatButton'),
                                              'PostedBy': problem.get('PostedBy')
                                              })
    rendered = json.loads(attachment, strict=False)
    return rendered
