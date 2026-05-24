from datetime import datetime, time, timedelta
from typing import Dict

class DeviceType:
    EDUCATION = "Education"
    UTILITY = "Utility"
    ENTERTAINMENT = "Entertainment"

class HomeDevice:
    def __init__(self, device_id: str, device_name: str, device_type: str):
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type

class UserProfile:
    def __init__(self, name: str, is_parent: bool, daily_screentime_limitinMins: int = 120):
        self.name = name
        self.is_parent = is_parent
        self.screentime_limit = daily_screentime_limitinMins
        self.screentimelog: Dict[str, int] =  {}

    def get_screentime_today(self, current_date_str: str) -> int:
        return self.screentimelog.get(current_date_str, 0)
    
    def log_screentime(self, current_date_str: str, minutes: int):
        if current_date_str not in self.screentimelog:
            self.screentimelog[current_date_str] = 0
        self.screentimelog[current_date_str] += minutes

class ScreenAccessController:
    def __init__(self, curfew_time: time):
        self.curfew_time = curfew_time

    def request_lockscreenUnlock(self, user: UserProfile, device: HomeDevice, current_dt: datetime) -> tuple[bool, str]:
        '''
        this will evaluate if a user can unlock a device lockscreen
        Returns true of false status message
        '''

        if user.is_parent:
            return True, f"Access Granted: Welcome back, {user.name}."
        
        current_time = current_dt.time()
        current_date_str = current_dt.strftime("%Y-%m-%d")

        if current_time >= self.curfew_time:
            return False, f"Access Denied: Past your curfew ({self.curfew_time.strftime('%I:%M %p')})."
        
        if device.device_type == DeviceType.ENTERTAINMENT:
            minutes_used = user.get_screentime_today(current_date_str)
            if minutes_used >= user.screentime_limit:
                return False, f"Access Denied: You've finished your daily limit of {user.screentime_limit} mins."
            
            remaining = user.screentime_limit - minutes_used
            return True, f"Access Granted: Lockscreen unlocked. {remaining} minutes remaining today"
        
        return True, f"Access Granted: device unlocked"
    