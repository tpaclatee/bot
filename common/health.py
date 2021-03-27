from datetime import datetime

import requests

from common import conf, webex
from nagios import nagios_filter


def check_bot_up():
    resp = requests.get(conf.bot_url)
    if resp.status_code == 405:
        return True
    else:
        return False


def active_problems_printout():
    """Print problems posted but still active to debug chat"""
    posted = nagios_filter.get_alerts(filter_posted=False)
    m = ""
    for p in posted:
        m += "* **{service}** **Duration**:{duration}  **Host**:{host} **Status**: {status}\n".format(host=p.HostName,
                                                                                                      service=p.ServiceName,
                                                                                                      status=p.Status,
                                                                                                      duration=p.Duration)
    return m


def canary(now):
    current_min = now.strftime("%M")
    if current_min == "30" or current_min == "00":
        return True
    else:
        return False


def health_check():
    if canary(datetime.now()):
        stamp = datetime.now().strftime("%H:%M:%S")
        m = "IOCBot canary posts every 30 minutes if bot is running.  IOCBot is running as of **{stamp}**\n".format(
            stamp=stamp)
        m += "Tunnel from webex to bot to accept commands is up: **{up}**\n".format(
            up=check_bot_up())
        m += "### Commands\n"
        m += "* **@IOCBot /beepon** will have the bot beep you if a problem comes in.  Turn on your speaker.\n"
        m += "* **@IOCBot /beepoff** will turn off beeping if you want it off when your shift ends\n"
        m += "### Release Notes v1.2\n"
        m += "* Add morning maint window 6:00-6:40am detailed health checks\n"
        m += "### Problems posted to chat but are still active\n"
        m += active_problems_printout()
        webex.post_debug_message(m)