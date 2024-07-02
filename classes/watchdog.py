import time
import threading

class WatchDog:
    """
    Makes sure that all the threads are running
    """
    
    def __init__(self, output, timeout=150) -> None:
        self.output = output
        
        self.calling_class = {}
        self.timeout = timeout
        self.exit_flag = threading.Event()
        
    
    def start(self, calling_class):
        """
        Starts the watchdog thread

        Args:
            calling_class (String): Identifier for the area of code calling the watchdog

        Raises:
            RuntimeError: Raises a runtime error if the watchdog thread fails to start
        """
        self.calling_class[calling_class] = time.time()
        
        try:
            self.output.watchdog_out("Starting WatchDog Thread...", blockPosition="start")
            watchdog_thread = threading.Thread(target=self.watch_thread)
            watchdog_thread.daemon = True
            watchdog_thread.start()
        except Exception as Ex:
            self.output.watchdog_out("Failed to start WatchDog Thread!", blockPosition="end")
            self.exit_flag.set()
            
            raise RuntimeError(Ex)
        
        else:
            self.output.watchdog_out("WatchDog started succsessfully!", blockPosition="end")
    
    
    def check_in(self, calling_class):
        """
        This function is called by the other threads to allow them to check in with the watchdog

        Args:
            calling_class (String): Identifier for the calling class to use to check in
        """
        
        try:
            self.output.watchdog_out(f"'{calling_class}' checking in after {str(time.time() - self.calling_class[calling_class])[:4]}s")
        except KeyError:
            self.output.watchdog_out(f"'{calling_class}' initialised WatchDog")
            
        self.calling_class[calling_class] = time.time()


    def watch_thread(self):
        """
        This function loops checking to make sure each class has checked in within the timeout limit
        """
        
        while not self.exit_flag.is_set():
            for calling_class in self.calling_class:
                if time.time() - self.calling_class[calling_class] > self.timeout:
                    self.output.watchdog_out(f"Thread {calling_class} stopped!")
                    
                    # Handle the timeout error
                    self.exit_flag.set()  # Set the exit flag
                    break
                
            time.sleep(self.timeout)