import json
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message

# from app.keyboards import LangKeyboard
# from bot import _
from utils import send_json_data, write
from ..routes import user_router as router
from codeforces import get_contestants, get_unfreezed_standings, get_cf_configs, load_default_configs
from data.configs_reader import DIR


@router.message(Command("unfreeze_standings"))
async def _unfreeze_standings(message: Message):
	docs = get_unfreezed_standings(message.chat.id)
	for status, logs, json, file_name in docs:
		if status == 'FAILED':
			await message.answer(logs)
		await send_json_data(message.chat.id, json, file_name)


def beautify(data):
	text = ''
	if data == None:
		text = "Nothing has changed"
	else:
		cmp = lambda x: (len(x[0]), x[0])
		data = dict(sorted(data.items(), key = cmp))
		for k, v in data.items():
			line = f'{k}: {v} \n'
			if v == None:
				line = f'{k} \n'
			text += line
		if text == '':
			text = 'Not contestants yet'

	return text


@router.message(Command("get_new_contestants"))
async def _get_new_contestants(message: Message):
	status, logs, names = get_contestants(message.chat.id, key='new')
	text = logs
	if status == 'OK':
		text = beautify(names)
	await message.answer(text)


@router.message(Command("get_all_contestants"))
async def _get_all_contestants(message: Message):
	status, logs, names = get_contestants(message.chat.id, key='all')
	text = logs
	if status == 'OK':
		text = beautify(names)
	await message.answer(text)


@router.message(Command("set_names"))
async def _request_new_names(message: Message):
	status, logs, names = get_contestants(message.chat.id, key='all')
	text = logs
	if status == 'OK':
		if len(names) == 0:
			text = 'Not contestants yet'
		else:
			cmp = lambda x: (len(x[0]), x[0])
			names = dict(sorted(names.items(), key = cmp))
			names = json.dumps(names, indent = 4, ensure_ascii=False)
			text = f'''Please change "null" fields to names in double quotes
Please send your data in JSON format like this:
Names = {names}'''
	await message.answer(text)


@router.message(F.text.lower().startswith('names')) # TODO add FSM
async def _set_names(message: Message):
    full_text = message.text
    if (i := full_text.find('{')) > -1:
    	full_text = full_text[i:]
    try:
        new_names = json.loads(full_text)
        status, logs, names = get_contestants(message.chat.id, key='all')
        if status == 'OK':
        	new_names = names | new_names
        status, logs, configs = get_cf_configs(message.chat.id)
        if status == 'FAILED':
	        status, def_logs, configs = load_default_configs(message.chat.id)
	        logs += def_logs
        if status == 'OK':
        	contest_id = configs['CONTEST_ID']
        	write(new_names, f'{DIR}/data/Names_{message.chat.id}_{contest_id}.json', is_json=True) # change to db and encrypt
	        str_new_names = beautify(new_names)
        	logs = f'Information successfully updated\n'
        	text = f'{logs}{str_new_names}'
        else:
        	text = logs
        await message.answer(text)
    except (json.JSONDecodeError, ValueError) as e:
        await message.answer(f'Invalid format: {e}. Please try again.')