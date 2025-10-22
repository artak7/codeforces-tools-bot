import asyncio
from typing import Dict, Set
from datetime import datetime
from bot import bot
from codeforces import get_contestants
from utils import logger


class ContestMonitor:
    """Monitor Codeforces contests for new participants"""
    
    def __init__(self):
        self.active_monitors: Dict[int, asyncio.Task] = {}
        self.monitor_intervals: Dict[int, int] = {}  # chat_id -> interval in seconds
        
    def is_monitoring(self, chat_id: int) -> bool:
        """Check if monitoring is active for a chat"""
        return chat_id in self.active_monitors and not self.active_monitors[chat_id].done()
    
    async def _monitor_loop(self, chat_id: int, interval: int):
        """Background task that checks for new contestants periodically"""
        logger.info(f"Started monitoring for chat {chat_id} with interval {interval}s")
        
        while True:
            try:
                await asyncio.sleep(interval)
                
                # Check for new contestants
                status, logs, new_names = get_contestants(chat_id, key='new')
                
                if status == 'OK' and new_names:
                    # Format notification message
                    count = len(new_names)
                    names_list = '\n'.join([f"  • {name}" for name in new_names.keys()])
                    message = f"🔔 <b>New contestants detected!</b>\n\nFound {count} new participant(s):\n{names_list}"
                    
                    # Send notification
                    await bot.send_message(chat_id, message, parse_mode="HTML")
                    logger.info(f"Sent notification to chat {chat_id}: {count} new contestants")
                    
            except asyncio.CancelledError:
                logger.info(f"Monitoring cancelled for chat {chat_id}")
                break
            except Exception as e:
                logger.error(f"Error in monitor loop for chat {chat_id}: {e}")
                # Continue monitoring despite errors
                
    def start_monitoring(self, chat_id: int, interval: int = 60):
        """Start monitoring for a chat"""
        if self.is_monitoring(chat_id):
            return False, "Monitoring is already active"
        
        # Create and store the monitoring task
        task = asyncio.create_task(self._monitor_loop(chat_id, interval))
        self.active_monitors[chat_id] = task
        self.monitor_intervals[chat_id] = interval
        
        return True, f"Monitoring started with {interval}s interval"
    
    def stop_monitoring(self, chat_id: int):
        """Stop monitoring for a chat"""
        if not self.is_monitoring(chat_id):
            return False, "Monitoring is not active"
        
        # Cancel the task
        self.active_monitors[chat_id].cancel()
        del self.active_monitors[chat_id]
        del self.monitor_intervals[chat_id]
        
        return True, "Monitoring stopped"
    
    def get_status(self, chat_id: int) -> str:
        """Get monitoring status for a chat"""
        if self.is_monitoring(chat_id):
            interval = self.monitor_intervals[chat_id]
            return f"✅ Active (checking every {interval}s)"
        return "❌ Inactive"
    
    async def cleanup(self):
        """Cancel all monitoring tasks"""
        for task in self.active_monitors.values():
            task.cancel()
        self.active_monitors.clear()
        self.monitor_intervals.clear()


# Global monitor instance
monitor = ContestMonitor()
