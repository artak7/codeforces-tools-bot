import json, codecs, os
from aiogram import types
from bot import bot
from .logging import logger

async def send_json_data(chat_id: int, data: dict, filename: str ='file'):
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    file = types.BufferedInputFile(
        file=json_data.encode('utf-16'),
        filename=filename
    )
    await bot.send_document(
        chat_id=chat_id,
        document=file,
        caption='Here is your generated JSON'
    )


def read(file_name, is_json=True):
    status = 'FAILED'
    logs = f'{status}. File does not exists.\n' #{file_name}
    data = None
    if os.path.exists(file_name):
        status = 'OK'
        logs = ''
        with codecs.open(file_name, 'r', encoding='utf-16') as file:
            if is_json:
                data = json.load(file)
            else:
                data = file.read()
    else:
        logger.error(logs)
    return status, logs, data


def write(data, file_name, is_json=True):
    if is_json:
        data = json.dumps(data, indent = 4, ensure_ascii=False)
    else:
        data = str(data)
    with codecs.open(file_name, 'w+', encoding='utf-16') as file:
        file.write(data)