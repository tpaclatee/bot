from loguru import logger

import nagios.nagios_filter
from nagios import nagios_db
from nagios import nagios_webex
from nagios import nagios_scraper


def sync_nagios():
    scrape_nagios_to_db()
    publish_active_problems()


def publish_active_problems():
    # Post to chat
    problems = nagios.nagios_filter.get_alerts()
    nagios_webex.post_to_chat(problems)


def scrape_nagios_to_db():
    logger.info('Sync NAGIOS and post to chat')

    orig = nagios_db.get_all_problems()
    logger.info(str(len(orig)) + ' problems found in DB')
    latest = nagios_scraper.scrape()
    logger.info(str(len(latest)) + ' problems found after scraping')

    sync_removed(orig, latest)

    # Add new and merge existing problems
    nagios_db.save_problems(latest)
    check = nagios_db.get_all_problems()
    logger.info('After cleanup DB has ' + str(len(check)) + ' problems')


def sync_removed(orig, latest):
    removed = removed_problems(orig, latest)
    logger.info('Problems to remove since no longer active: ' + str(len(removed)))
    for r in removed:
        logger.info('    ' + r)
        nagios_db.delete_problem(r)


def removed_problems(orig, latest):
    orig_key = [o.ProblemKey for o in orig]
    latest_key = [o.ProblemKey for o in latest]
    removed = [item for item in orig_key if item not in latest_key]
    return removed
