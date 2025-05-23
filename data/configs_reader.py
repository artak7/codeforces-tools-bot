from pathlib import Path
from environs import Env, exceptions


env = Env()
env.read_env()

DIR = Path(__file__).absolute().parent.parent

TELEGRAM_BOT_TOKEN = env.str('BOT_TOKEN')

try:
	WEBHOOK_URL = env.str("WEBHOOK_URL") + "/webhook"  # Full URL like: https://your-domain.com/webhook
except (exceptions.EnvError) as e:
	WEBHOOK_URL = None

PORT = int(env.str("PORT", 8000))
RENDER_URL = env.str("RENDER_URL", "https://codeforces-tools-bot.onrender.com")

# ADMIN_ID = env.str("ADMIN_ID") # need list

# RD_DB = env.int("RD_DB", None)
# RD_HOST = env.str("RD_HOST", None)
# RD_PORT = env.int("RD_PORT", None)
# RD_USER = env.str("RD_USER", None)
# RD_PASS = env.str("RD_PASS", None)

# RD_URI = env.str("RD_URI", default=None)
# if RD_DB and RD_HOST and RD_PORT:
#     RD_URI = f"redis://{RD_HOST}:{RD_PORT}/{RD_DB}"
#     if RD_USER and RD_PASS:
#         RD_URI = f"redis://{RD_USER}:{RD_PASS}@{RD_HOST}:{RD_PORT}/{RD_DB}"

# DB_USER = env.str("DB_USER", default=None)
# DB_PASS = env.str("DB_PASS", default=None)
# DB_NAME = env.str("DB_NAME", default=None)
# DB_HOST = env.str("DB_HOST", default=None)
# DB_PORT = env.int("DB_PORT", default=None)

# DB_URI = env.str("DB_URI", default="sqlite+aiosqlite:///database.sqlite3")
# if DB_HOST and DB_PORT and DB_USER and DB_PASS and DB_NAME:
#     DB_URI = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


I18N_PATH = f'{DIR}/data/locales'
I18N_DOMAIN ='bot' # env.str("I18N_DOMAIN", "bot")