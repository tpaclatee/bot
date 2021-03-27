import configparser

import keyring

config = configparser.ConfigParser()
config.sections()
config.read('.env')
if not config.has_option('DEFAULT', 'ENV'):
    config.read('../.env')

env = config['DEFAULT']['ENV']
bot_port = config['DEFAULT']['TEAMS_BOT_PORT']
bot_email = config['DEFAULT']['TEAMS_BOT_EMAIL']
bot_url = config['DEFAULT']['TEAMS_BOT_URL']
bot_app_name = config['DEFAULT']['TEAMS_BOT_APP_NAME']
bot_room_id = config['DEFAULT']['TEAMS_BOT_ROOM_ID']
bot_room_id_debug = config['DEFAULT']['TEAMS_BOT_ROOM_ID_DEBUG']
bot_room_id_ioc_monitoring = config['DEFAULT']['TEAMS_BOT_ROOM_ID_IOC_MONITORING']
dt_api_url = config['DEFAULT']['DYNATRACE_API_URL']
nagios_user = config['DEFAULT']['NAGIOS_USER']
nagios_filter_critical = config['DEFAULT']['NAGIOS_FILTER_CRITICAL']
wait_to_post_minutes = config['DEFAULT']['WAIT_TO_POST_MINUTES']
sql_lite_db = config['DEFAULT']['SQL_LITE_DB']
sql_lite_unit_db = config['DEFAULT']['SQL_LITE_UNIT_TEST_DB']
sqlalchemy_debug_sql = config['DEFAULT']['SQLALCHEMY_DEBUG_SQL']
app_base_path = config['DEFAULT']['APP_BASE_PATH']
bot_debug_unit_test_person_id = config['DEFAULT']['TEAMS_BOT_UNIT_TEST_DEBUG_PERSON_ID']

# credentials keystore keys
teams_token = config['AUTH']['TEAMS_BOT_TOKEN']
dt_bearer_token = config['AUTH']['DYNATRACE_BEARER_TOKEN']
nagios_pass = config['AUTH']['NAGIOS_PASS']
dt_api_token = config['AUTH']['DYNATRACE_API_TOKEN']

teams_token = keyring.get_password(teams_token.split(".")[1], teams_token.split(".")[2])
dt_bearer_token = keyring.get_password(dt_bearer_token.split(".")[1], dt_bearer_token.split(".")[2])
nagios_pass = keyring.get_password(nagios_pass.split(".")[1], nagios_pass.split(".")[2])
dt_api_token = keyring.get_password(dt_api_token.split(".")[1], dt_api_token.split(".")[2])
