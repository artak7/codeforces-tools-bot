import environs
from utils import read, write, logger
from data.configs_reader import DIR, env


random_configs = {
    'IS_PRIVATE_GROUP': 'false',
    'GROUP_CODE': '',
    'CONTEST_ID': '1900',
    'AS_MANAGER': 'false',
    'CF_API_KEY': '',
    'CF_API_SECRET': '',
    'FROZEN_TIME': '60',
    'SHOW_UNOFFICIAL': 'true'
}


def get_cf_configs(chat_id): # change to db and encrypt
    file_name = f'{DIR}/data/cf_settings_{chat_id}.json'
    status, logs, configs = read(file_name, is_json=True)
    return status, logs, configs


def load_default_configs(chat_id):
    status = 'OK'
    logs = 'Loading default configs from .env\n'
    logger.info(logs)
    configs = random_configs
    missing_fields = [] 
    for key in configs.keys():
        try:
            configs[key] = env.str(key)
        except (environs.exceptions.EnvError) as e:
            missing_fields.append(key)
    if missing_fields:
        status = 'FAILED'
        failed_logs = f'{status}. Environment variables {missing_fields} in .env not set\n'
        logger.error(failed_logs)
        logs += failed_logs
        # logs += 'Set your configs with /set_configs command\n' 
        # logs += 'Setting random configs\n'
    write(configs, f'{DIR}/data/cf_settings_{chat_id}.json', is_json=True) # change to db and encrypt
    return status, logs, configs