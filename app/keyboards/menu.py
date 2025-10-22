from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    
    # Row 1: Main actions
    builder.add(KeyboardButton(text="/unfreeze_standings 🏆"))
    builder.add(KeyboardButton(text="/standings_html 📊"))
    
    # Row 2: Contestants
    builder.add(KeyboardButton(text="/get_new_contestants 👥"))
    builder.add(KeyboardButton(text="/get_all_contestants 📋"))
    
    # Row 3: Names
    builder.add(KeyboardButton(text="/set_names ✏️"))
    
    # Row 4: Configs
    builder.add(KeyboardButton(text="/get_configs ⚙️"))
    builder.add(KeyboardButton(text="/set_configs 🔧"))
    builder.add(KeyboardButton(text="/load_default_configs 🔄"))
    
    # Row 5: Monitoring
    builder.add(KeyboardButton(text="/start_monitor"))
    builder.add(KeyboardButton(text="/stop_monitor 🔕"))
    builder.add(KeyboardButton(text="/monitor_status 📊"))
    
    # Row 6: Help
    builder.add(KeyboardButton(text="/help ❓"))
    
    builder.adjust(2, 2, 1, 3, 3, 1)
    
    return builder.as_markup(resize_keyboard=True, persistent=True)
