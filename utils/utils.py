import json, codecs, os
from aiogram import types
from bot import bot
from .logging import logger

async def send_file_data(chat_id: int, filetype: str, filedata: dict, filename: str ='file'):
    if filetype == "JSON" or filedata is None:
        filedata = json.dumps(filedata, indent=4, ensure_ascii=False)
    file = types.BufferedInputFile(
        file=filedata.encode('utf-16'),
        filename=filename
    )
    await bot.send_document(
        chat_id=chat_id,
        document=file,
        caption=f'Here is your generated {filetype}'
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