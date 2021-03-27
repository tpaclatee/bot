import traceback

import requests
from loguru import logger

from common import webex
from common.health import health_check
from dynatrace import dynatrace_job
from nagios import nagios_job


def background_schedule():
    from apscheduler.schedulers.background import BackgroundScheduler

    def tick():
        try:
            dynatrace_job.sync_dynatrace()
            nagios_job.sync_nagios()
            health_check()
        except requests.exceptions.RequestException as e:
            logger.error(e)
            webex.post_debug_message(
                "**ERROR:** RequestException: Verify **VPN is connected** and nagios website is up")
        except Exception as e:
            ex = traceback.format_exc()
            logger.error(ex)
            ex = traceback.format_exc(1)
            webex.post_debug_message("```" + ex + "```")

    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=60)
    scheduler.start()
