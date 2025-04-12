import json
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command

from ..routes import user_router as router
from utils import write
from codeforces import get_cf_configs, load_default_configs
from data.configs_reader import DIR


def beautify(data):
    text = ''
    for key in data.keys():
        if data[key]:
            if key in ['IS_PRIVATE_GROUP', 'AS_MANAGER', 'SHOW_UNOFFICIAL']:
                data[key] = data[key].lower()
            elif key in ['CF_API_KEY', 'CF_API_SECRET']:
                data[key] = '******'
        text += f'\n    "{key}": "{data[key]}",'
    text = '{' + text[:-1] + '\n}'
    return text


@router.message(Command('load_default_configs'))
async def load_configs(message: Message):
    status, logs, default_configs = load_default_configs(message.chat.id)
    str_configs = beautify(default_configs)
    text = 'Default' if status == 'OK' else 'Random'
    text = f'{logs} {text} configs:\n {str_configs}'
    await message.answer(text)


@router.message(Command('get_configs'))
async def get_configs(message: Message):
    status, logs, configs = get_cf_configs(message.chat.id)
    text = 'Your'
    if status == 'FAILED':
        status, def_logs, configs = load_default_configs(message.chat.id)
        logs += def_logs
        text = 'Default' if status == 'OK' else 'Random'
    str_configs = beautify(configs)
    text = f'{logs} {text} configs:\n {str_configs}'
    await message.answer(text)


@router.message(Command('set_configs'))
async def request_configs(message: Message):
    status, logs, configs = get_cf_configs(message.chat.id)
    if status == 'FAILED':
        status, def_logs, configs = load_default_configs(message.chat.id)
        logs += def_logs
    str_configs = beautify(configs)
    text = f'Please send your data in JSON format like this:\nConfigs = {str_configs}'
    await message.answer(text)


def validate(data, key):
    if data.get(key) == None:
        return False
    dt = data[key].lower()
    if dt in ['', '******']: 
        return False
    if key in ['IS_PRIVATE_GROUP', 'AS_MANAGER', 'SHOW_UNOFFICIAL']:
        return dt in ['true','false']
    elif key in ['CONTEST_ID', 'FROZEN_TIME']:
        return dt.isdigit()
    return True


@router.message(F.text.lower().startswith('configs'))
async def set_configs(message: Message):
    full_text = message.text
    if (i := full_text.find('{')) > -1:
        full_text = full_text[i:]
    try:
        await message.delete()
        new_configs = json.loads(full_text)
        status, logs, configs = get_cf_configs(message.chat.id)
        text = 'older'
        if status == 'FAILED':
            status, def_logs, configs = load_default_configs(message.chat.id)
            logs += def_logs
            text = 'default' if status == 'OK' else 'random'
        loaded_configs = dict()
        received_configs = dict()
        wrong_fields = list()
        for key in configs.keys():
            if validate(new_configs, key):
                if key in ['IS_PRIVATE_GROUP', 'AS_MANAGER', 'SHOW_UNOFFICIAL']:
                    new_configs[key] = new_configs[key].lower()
                received_configs[key] = new_configs[key]
            else:
                if new_configs.get(key) != None:
                    wrong_fields.append(key)
                loaded_configs[key] = new_configs[key] = configs[key]
        new_configs = loaded_configs | received_configs # NOTE returns pointer
        write(new_configs, f'{DIR}/data/cf_settings_{message.chat.id}.json', is_json=True) # change to db and encrypt
        if wrong_fields:
            logs = f'Found mistakes on fields {wrong_fields}\n'
        str_rec_configs = beautify(received_configs)
        str_load_configs = beautify(loaded_configs)
        text = f'{logs} Received your configs:\n{str_rec_configs}\nLoaded {text} configs:\n{str_load_configs}'
        await message.answer(text)
    except (json.JSONDecodeError, ValueError) as e:
        await message.answer(f'Invalid format: {e}. Please try again.')