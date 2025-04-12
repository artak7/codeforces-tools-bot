start_text = '''This bot is created for notifying when somebody take part in https://codeforces.com contest.
    First, You need to create your API Token at https://codeforces.com/settings/api
    Second, choose contest and set info about this contest with command /set_configs
    See /help for more info'''

commands_text = '''All Commands:\n
    /help
    /load_default_configs - load configs from .env. only for testing
    /get_configs - get your current configs
    /set_configs - set from what contest to load info
    format of answer :
    {
        "IS_PRIVATE_GROUP": "false",
        "GROUP_CODE": "",
        "CONTEST_ID": "1900",
        "AS_MANAGER": "true",
        "CF_API_KEY": "",
        "CF_API_SECRET": "",
        "FROZEN_TIME": "60",
        "SHOW_UNOFFICIAL": "true"
    }\n
    /unfreeze_standings - return info about contest in 2 format to load it in unfreezing beautifier
    /get_new_contestants - check whether new contestants joined to the current contest
    /get_all_contestants - get all contestants names joined to the current contest
    /set_names - set names for anonymous contestants
    '''