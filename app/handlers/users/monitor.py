from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message

from ..routes import user_router as router
from app.scheduler import monitor


@router.message(Command("start_monitor"))
async def start_monitor_handler(message: Message):
    """Start monitoring for new contestants"""
    # Parse interval from command args (default 60 seconds)
    args = message.text.split()[1:] if message.text else []
    interval = 60
    
    if args:
        try:
            interval = int(args[0])
            if interval < 10:
                await message.answer("⚠️ Interval must be at least 10 seconds")
                return
        except ValueError:
            await message.answer("⚠️ Invalid interval. Usage: /start_monitor [seconds]")
            return
    
    success, msg = monitor.start_monitoring(message.chat.id, interval)
    emoji = "✅" if success else "⚠️"
    await message.answer(f"{emoji} {msg}")


@router.message(Command("stop_monitor"))
async def stop_monitor_handler(message: Message):
    """Stop monitoring for new contestants"""
    success, msg = monitor.stop_monitoring(message.chat.id)
    emoji = "✅" if success else "⚠️"
    await message.answer(f"{emoji} {msg}")


@router.message(Command("monitor_status"))
async def monitor_status_handler(message: Message):
    """Check monitoring status"""
    status = monitor.get_status(message.chat.id)
    await message.answer(f"📊 <b>Monitoring Status</b>\n\n{status}", parse_mode="HTML")
