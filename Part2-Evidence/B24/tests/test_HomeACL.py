import unittest
from datetime import datetime, time
from Home_security.HomeACL import ScreenAccessController, HomeDevice, UserProfile, DeviceType

class TestScreenAccessController(unittest.TestCase):
    def setUp(self):
        '''
        This runs before every single test scenario for clean objects
        '''
        self.lockscreen_manager = ScreenAccessController(curfew_time=time(20,30))
        self.kids_ipad = HomeDevice("device01", "kid01 iPad", DeviceType.ENTERTAINMENT)
        self.school_laptop = HomeDevice("device02", "school macbook", DeviceType.EDUCATION)
        self.kid = UserProfile(name="Kid", is_parent=False, daily_screentime_limitinMins=120)
        self.today = datetime(2026, 5, 24)

    def test_child_under_screentime_limit_can_unlock(self):
        '''
        test for child device can unlock if they are under
        the set screentime.
        '''
        log_time = datetime.combine(self.today.date(), time(14,0))
        allowed, msg = self.lockscreen_manager.request_lockscreenUnlock(self.kid, self.kids_ipad, log_time)

        self.assertTrue(allowed)
        self.assertIn("Access Granted", msg)

    def test_child_over_screentime_limit_is_denied(self):
        '''
        test for child device cannot be unlocked if they
        are over the set screentime
        '''
        log_time = datetime.combine(self.today.date(), time(16,30))
        self.kid.log_screentime("2026-05-24", 120)

        allowed, msg = self.lockscreen_manager.request_lockscreenUnlock(self.kid, self.kids_ipad, log_time)

        self.assertFalse(allowed)
        self.assertIn("You've finished your daily limit of", msg)

    def test_educational_bypass_ignores_screentime_limit(self):
        '''
        test for child educational devices can be unlocked even
        if they are over their screentime
        '''
        log_time = datetime.combine(self.today.date(), time(17,0))
        self.kid.log_screentime("2026-05-24", 120)

        allowed, msg = self.lockscreen_manager.request_lockscreenUnlock(self.kid, self.school_laptop, log_time)

        self.assertTrue(allowed)
        self.assertIn("device unlocked", msg)

    def test_curfew_blocks_all_devices_for_children(self):
        '''
        test for child devices cannot be unlocked past set curfew
        '''
        log_time = datetime.combine(self.today.date(), time(21,0))

        allowed, msg = self.lockscreen_manager.request_lockscreenUnlock(self.kid, self.school_laptop, log_time)

        self.assertFalse(allowed)
        self.assertIn("Past your curfew", msg)

if __name__ == "__main__":
    unittest.main()

