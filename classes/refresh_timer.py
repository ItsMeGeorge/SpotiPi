import datetime
import time


class RefreshTimer:
    def __init__(self, output, watchdog, minimum_wait=15, maximum_wait=120):
        self.output = output
        self.watchdog = watchdog
        self.minimum_wait = minimum_wait
        self.maximum_wait = maximum_wait
        self.seconds_waited = 0
        
    def refresh_timer_loop(self, refresh_delay=5):
        self.output.debug("Starting Refresh Timer", "Refresh Timer")
        while (True):
            self.watchdog.check_in("RefreshTimer")
            self.seconds_waited += refresh_delay
            
            time.sleep(refresh_delay)

    # --- Getters and Setters --- #
    # --- Seconds waited --- #
    def is_refresh_ready(self) -> bool:
        # return self.seconds_waited >= self.minimum_wait
        return self.seconds_waited >= (self.minimum_wait + 5)
    
    def reset_seconds_waited(self):
        self.seconds_waited = 0

    def get_seconds_waited(self) -> int:
        return self.seconds_waited

    # --- Get minimum seconds waited --- #
    def get_min_wait(self):
        return self.minimum_wait 
    
    def get_max_wait(self):
        return self.maximum_wait               