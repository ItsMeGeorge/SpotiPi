# Other imports
import os
import argparse
import math
import time
import datetime
import threading

import requests

# Class Imports
from classes import refresh_timer, octoprint, spotipi, watchdog, output

class ProgramValues:
    def __init__(self):
        self.VERSION = 1.1
        
        # Headless flag
        self.HEADLESS = False
        # Parse Arguments
        self.debug_session = self.parse_arguments()
        
        if (not self.HEADLESS):
            try:
                from classes import display
            except ImportError:
                print("Unable to import display.")
        
        self.last_active = datetime.datetime.now()
        self.active_session = True
        
        try:
            print("Initialising Output...")
            self.output = output.Output(isDebugging=self.debug_session)
        except Exception as Ex:
            raise ModuleNotFoundError(f"Unable to initialise the Output Class!\n{Ex}")
        
        else:
            self.output.out("Output initialised!", f"{__class__.__name__}")
        
        try:
            # Initialise WatchDog Class
            self.output.out("Initialising WatchDog...", f"{__class__.__name__}")
            self.watchdog = watchdog.WatchDog(self.output)
            
        except Exception as Ex:
            self.output.out("Failed to initialise WatchDog!", f"{__class__.__name__}", "error")
            raise ModuleNotFoundError(f"Unable to initialise the WatchDog Class!\n{Ex}")
        
        else:
            self.output.out("WatchDog initialised!", f"{__class__.__name__}", "success")
        
        
        self.output.out("Initialising Classes...", f"{__class__.__name__}")
        # Initalise the OctoPrint and Spotipy Classes
        try:
            # Initialise refresh timer class
            self.refresh_timer = refresh_timer.RefreshTimer(self.output, self.watchdog)
            
            # Initialise spotipy classes
            self.spotipy_values = spotipi.SpotipyValues()
            self.spotipy_api = spotipi.SpotipyAPI()

            # Initialise octoprint classes
            self.octo_print_values = octoprint.OctoPrintValues()
            self.octo_print_api = octoprint.OctoPrintAPI()
            
            if (not self.HEADLESS):
                # Initialise Display class
                self.display = display.Display(output=self.output)
        except Exception as Ex:
            self.output.out("Failed to initialise Classes", f"{__class__.__name__}", "error")
            raise ModuleNotFoundError(f"Unable to initialise Classes!\n{Ex}")
            
        else:
            self.output.out("Successfully Initialised Classes!", f"{__class__.__name__}", "success")


        # Spotify Values
        self.spotify_status = None
        self.song_id = str
        self.song_name = str
        self.song_artist = str
        self.explicit_song = None
        self.song_progress = None
        self.song_duration = None

    def parse_arguments(self):
        """
        Takes the command line arguments to allow the program to run in debug more (verbose output)

        Returns:
            Boolean: Returns True or False depending on if '-d' is given.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", action="store_true", required=False)
        parser.add_argument("-headless", action="store_true", required=False)
        
        args = parser.parse_args()
        
        if (args.headless):
            print("Running HEADLESS!")
            self.HEADLESS = True
        
        if (args.d):
            return True
        else:
            return False

    def set_debugging_session(self, is_debugging_session):
        self.debug_session = is_debugging_session

    def get_debugging_session(self) -> bool:
        return self.debug_session


    # Spotipy Getters and Setters
    # --- Update Spotify Values function
    def update_spotify_values(self):
        """
        Calls the spotipy_values class to get the new song values and saves them to program_values
        """
        try:
            self.output.debug("Updating song values...", f"{__class__.__name__}")
            
            self.set_song_id(self.spotipy_values.get_song_id())
            self.set_song_name(self.spotipy_values.get_song_name())
            self.set_song_artist(self.spotipy_values.get_artist_name())
            self.set_explicit_song(self.spotipy_values.get_explicit_song())
            self.set_song_progress(self.spotipy_values.get_song_progress())
            self.set_song_duration(self.spotipy_values.get_song_duration())
        except Exception as Ex:
            self.output.out("Unable to update Spotify Values!", f"{__class__.__name__}", "warning")
        else:
            self.output.debug("Song values updated successfully!", f"{__class__.__name__}")

    # --- Active Sesson --- #
    def set_active_session(self, active_session):
        self.active_session = active_session

    def get_active_session(self):
        return self.active_session

    def set_last_active(self, last_active):
        self.last_active = last_active

    def get_last_active(self):
        return self.last_active

    # --- Spotify Status --- #
    def set_spotify_status(self, spotify_status):
        self.spotify_status = spotify_status

    def get_spotify_status(self):
        return self.spotify_status

    # --- Song ID --- #
    def set_song_id(self, song_id):
        self.song_id = song_id

    def get_song_id(self):
        return self.song_id

    # --- Song Name --- #
    def set_song_name(self, song_name):
        self.song_name = song_name

    def get_song_name(self):
        return self.song_name

    # --- Song Artist --- #
    def set_song_artist(self, song_artist):
        self.song_artist = song_artist

    def get_song_artist(self):
        return self.song_artist

    # --- Explicit --- #
    def set_explicit_song(self, explicit):
        self.explicit = explicit

    def get_explicit_song(self):
        return self.explicit

    # --- Song Progress and Duration --- #
    def set_song_progress(self, song_progress):
        self.song_progress = song_progress

    def get_song_progress(self):
        return self.song_progress

    def set_song_duration(self, song_duration):
        self.song_duration = song_duration

    def get_song_duration(self):
        return self.song_duration


class ProgramLogic:
    def __init__(self):
            
        try:
            # Initialise program values class
            print("Initialising Program Values...")
            self.program_values = ProgramValues()

        except Exception as Ex:
            raise ModuleNotFoundError(f"Unable to initialise the ProgramValues Class!\n{Ex}")
        
        else:
            self.program_values.output.out("Program Values initialised!", f"{__class__.__name__}", "success")
            
        # Try and initialise threads
        try:
            self.program_values.output.out("Initialising Threads...", f"{__class__.__name__}")

            self.refresh_timer_thread = threading.Thread(target=self.program_values.refresh_timer.refresh_timer_loop)
            self.spotiPi_thread = threading.Thread(target=self.spotiPiLogic_loop)

            # Set each thread as a Daemon so they die with the main program upon exit
            self.refresh_timer_thread.daemon = True
            self.spotiPi_thread.daemon = True

        except Exception as Ex:
            self.program_values.output.out("Failed to initialise Threads!", f"{__class__.__name__}", "error")
            raise RuntimeError(f"Unable to initialise Threads!\n{Ex}")
        else:
            self.program_values.output.out("Threads initialised!", f"{__class__.__name__}", "success")

    def start_threads(self):
        self.refresh_timer_thread.start()
        self.spotiPi_thread.start()
        self.program_values.watchdog.start("ProgramLogic")

    def remove_brackets_from_song_name(self):
        """Takes a String and removes all the brackets that contain a keyword.

        Returns:
            String: Returns the given string with any brackets containing keywords removed.
        """
        # Starts as a try catch loop as '.index()' throws a ValueError is the item being searching for isn't found
        try:
            # Declare a local variable of song_name to be manipulated freely
            song_name = self.program_values.get_song_name()
            
            # Declares a list of opening brackets to find in the given string
            bracket_list = ["(", "["]

            # checks to see if song_name contains one of the brackets declared in the list
            if (bracket in song_name for bracket in bracket_list):
                # Declares a list of keywords to look for 
                key_word_list = ["feat", "remix", "with", "intro"]
                # declares an empty list to store sub-strings to be removed from the given string
                string_to_remove = []

                # For each of the opening brackets contained in the bracket_list - setting 'i' (char) to the current bracket in the list
                for i in bracket_list:
                    # Crete an empty list to store the position of each bracket in the string
                    bracket_position_list = []

                    # Loops for the length of the song_name string with 'b' (int) being used as a counter
                    for b in range(len(song_name)):
                        if (song_name[b] == i):
                            # If the char at position song_name[b] == i then add b (int value == to the brackets position in the string) to the list
                            bracket_position_list.append(b)

                    # Loops for the number of occourences of 'i' in song_name - song_name.count(i) returns an int of the number of char (i) in the song_name string
                    for c in range(song_name.count(i)):
                        # Loops through each of the keywords - setting 'x' (string) to the current keyword in the list 
                        for x in key_word_list:
                            # if 'i' (set to the current item being itterated through in the brcket_list) is in the string 'song_name'
                            if (i in song_name):
                                self.program_values.output.debug(f"Found '{i}' in '{song_name}'", "Remove Brackets")

                                # If keyword 'x' is in a sub-string of the song_name
                                # The sub-string changes with each loop using the bracket_position_list defined earlier and using 'c' (int) to iterate through each position in the list
                                if (x in song_name[bracket_position_list[c] : song_name[bracket_position_list[c] : ].index(')' if i == '(' else ']') + bracket_position_list[c] + 1 ].lower() ):
                                    self.program_values.output.debug(f"'{song_name}' contains key word '{x}'", "Remove Brackets")
                                    self.program_values.output.debug(f"Removing '{song_name[bracket_position_list[c] : song_name[bracket_position_list[c] : ].index(')' if i == '(' else ']') + bracket_position_list[c] + 1 ]}' from song name", "Remove Brackets")

                                    # Appends the sub-string to the list 'string_to_remove' to remove at the end
                                    # The sub-strings to remove are added to a list instead of removed from the string as removing them would change the position of the next brackets in the next loop
                                    string_to_remove.append(song_name[bracket_position_list[c] : song_name[bracket_position_list[c] : ].index(')' if i == '(' else ']') + bracket_position_list[c] + 1 ])

                # If the string_to_remove contains a value (E.g. a bracket sub-string to remove from the string)
                if (string_to_remove is not None):
                    # Loop through each string to remove
                    for item in string_to_remove:
                        # Replace the string to remove with nothing
                        song_name = song_name.replace(item, "")

                    # Remove any double spaces created when removing the brackets
                    while("  " in song_name):
                        song_name = song_name.replace("  ", " ")
                        
                    self.program_values.output.debug(f"Song name set to '{song_name}'", "Remove Brackets")

        # Catches the value error thrown by .index()
        except ValueError as ex:
            self.program_values.output.out("Unable to remove brackets!", "Remove Brackets", "error")
            self.program_values.output.out(ex, "Remove Brackets", "error")

        # Returns the song_name string stripped of leading and trailing whitespaces
        return song_name.strip()

    def shorten_string(self, unformatted_string, font, identifier):
        """Makes sure the given string isn't too big to fit onto the screen

        Args:
            unformatted_string (str): The string that is going to be checked
            font (font): The font the string will be displayed in
            identifier (str): The type of string being passes (Song name or Artist name)

        Returns:
            formatted_string (str): Returns the given string with a reduced length to fit onto the screen
        """

        def calculate_string_width(string):
            """Helper function to calculate string width with optional explicit marker."""
            
            string_width, _ = font.getsize(string)
            if (identifier == "song" and self.program_values.get_explicit_song()):
                explicit_w, _ = self.program_values.display.get_EXPLICIT_FONT().getsize("E")
                string_width += explicit_w + 10
            return string_width

        # Only song names should have everything after the - removed
        if (identifier == "song" and "-" in unformatted_string):
            unformatted_string = unformatted_string.split("-", 1)[0]

        # Initial width calculation
        unformatted_string_w = calculate_string_width(unformatted_string)

        # Check if shortening is needed
        max_width = self.program_values.display.get_inky_display().WIDTH - 5
        if (unformatted_string_w <= max_width):
            return unformatted_string

        # Binary search for optimal string length
        left, right = 0, len(unformatted_string)
        while (left < right):
            mid = (left + right) // 2
            test_string = unformatted_string[:mid].strip() + ".."
            if (calculate_string_width(test_string) <= max_width):
                left = mid + 1
            else:
                right = mid

        formatted_string = unformatted_string[:right - 1].strip() + ".."
        self.program_values.output.debug(f"Song shortened to: {formatted_string}", "Shorten String")
        return formatted_string

    def format_song_details(self):
        """
        This function will format the song details ready to be displayed.
        """

        # Format song name
        self.program_values.set_song_name(self.remove_brackets_from_song_name())

        if (not self.program_values.HEADLESS):
            # Shorten string wont run as inky_display isn't set
            self.program_values.set_song_name(self.shorten_string(self.program_values.get_song_name(), self.program_values.display.get_SONG_FONT(), "song"))

            # Format Artist name(s)
            self.program_values.set_song_artist(self.shorten_string(self.program_values.get_song_artist(), self.program_values.display.get_ARTIST_FONT(), "artist"))

    def connection_check(self):
        """Checks if the printer is connected or not.

        Returns:
            Boolean: Returns True if the printer is connected, False if not.
        """
        
        # Spotify API endpoint to check connection
        endpoint = "https://api.spotify.com/"

        print("")
            
        try:
            if (self.program_values.octo_print_api.is_printer_connected()):
                self.program_values.output.out("Printer is connected!", "connCheck")

                if (self.program_values.octo_print_values.get_isPrinting()):
                    self.program_values.output.out(f"Printer is {self.program_values.octo_print_api.get_print_progress()}!", "connCheck")

                else:
                    self.program_values.output.out("Printer is not printing!", "connCheck")

            else:
                self.program_values.output.out("Printer is not connected!", "connCheck")
                
            self.program_values.output.out(f"Testing connection to '{endpoint}'...", "connCheck")
            # Send GET request to Spotify API
            response = requests.get(endpoint)

            # Check if response status code is successful (200)
            if response.status_code == 200:
                self.program_values.output.out(f"'{endpoint}' returned status code 200", "connCheck", "success")
                return True
            else:
                self.program_values.output.out(f"'{endpoint}' returned status code {response.status_code}", "connCheck", "failed")
                return False

        except requests.ConnectionError as ConnEx:
            self.program_values.output.debug(f"ConnectionError when trying to connect to {endpoint}", "connCheck")
            return False

        except Exception as Ex:
            # Error occurred during request
            self.program_values.output.out(f"Error occoured when trying to connect to the printer!", "connCheck", "error")

    def octoPrint_logic(self):
        """
        Sets the "isPrinting" value to True if something is being printed and to False if not.
        """
        
        try:
            if (self.program_values.octo_print_api.is_printer_connected()):
                self.program_values.output.out("Printer is connected!", "OctoPrintLogic")

                if (str(self.program_values.octo_print_api.get_printer_status()).lower() == "printing"):
                    self.program_values.output.out("Printer is printing!", "OctoPrintLogic")

                    self.program_values.octo_print_values.set_isPrinting(True)
                    self.program_values.octo_print_values.set_progress(self.program_values.octo_print_api.get_print_progress())

                    self.program_values.output.octoPrintProgress("OctoPrintLogic", self.program_values.octo_print_values.get_progress())

                else:
                    self.program_values.octo_print_values.set_isPrinting(False)
                    self.program_values.output.debug("Printer is not printing!", "OctoPrintLogic")

            else:
                self.program_values.output.debug("Printer is not connected!", "OctoPrintLogic")

        except Exception as Ex:
            self.program_values.output.out(f"An error occoured when getting the print progress\n{Ex}", "OctoPrintLogic", "error")

    def spotiPiLogic_loop(self):
        """
        This functions handles updating the values when a new song is playing.
        
        If a song is playing on spotify the song details are taken and compared to the details held.
        If the details are different the new song values are saved.
        If the details are the same the loop waits for the designated amount of time before checking again.
        
        If nothing is playing, the function sets the next top artist to show.
        """
        
        self.program_values.output.debug("Beginning SpotiPy Loop", f"{__class__.__name__}")

        while(True):
            try:
                # While seconds waited > min_wait time
                while(self.program_values.refresh_timer.get_seconds_waited() > self.program_values.refresh_timer.get_min_wait()):
                    self.program_values.watchdog.check_in("Spotipy_Loop")
                    print("Spotipy checking in with watchdog")
                    self.program_values.output.debug("Spotify Checking values", f"Spotipy Loop")


                    print("Trying to get spotify data..")
                        
                    spotify_data = self.program_values.spotipy_api.get_currently_playing()
                    self.program_values.spotipy_values.set_spotify_status(spotify_data[0])

                    print("Spotify Data:")
                    print(spotify_data)
                    print()
                        

                    try:
                        print("Trying to get spotify data..")
                        
                        spotify_data = self.program_values.spotipy_api.get_currently_playing()
                        self.program_values.spotipy_values.set_spotify_status(spotify_data[0])

                        print("Spotify Data:")
                        print(spotify_data)
                        print()
                        
                    except Exception as Ex:
                        print("Error!")
                        print(Ex)
                    else:
                        print("Sucsess!")
                        print(f"Spotify data:\n{spotify_data}")

                    self.program_values.output.debug(f"Spotify Status: {spotify_data[0]}", "Spotify Loop")

                    # If spotify reports the status as either "playing" or "paused"
                    if (self.program_values.spotipy_values.get_spotify_status() != "stopped"):
                        # Update latest activity with datetime.now()
                        self.program_values.set_last_active(datetime.datetime.now())

                        # Update the SPOTIPY values
                        self.program_values.spotipy_values.set_song_progress(spotify_data[5] / 1000)

                        # If the current ID held in spotify values is not the same as the one just retrieved
                        if (self.program_values.spotipy_values.get_song_id() != spotify_data[1]):
                            if ((spotify_data[5] / 1000) > 5):
                                # Update the values held in spotify values to the ones just retrieved
                                self.program_values.spotipy_values.set_song_id(spotify_data[1])
                                self.program_values.spotipy_values.set_song_name(spotify_data[2])
                                self.program_values.spotipy_values.set_artist_name(spotify_data[3])
                                self.program_values.spotipy_values.set_explicit_song(spotify_data[4])
                                self.program_values.spotipy_values.set_song_progress(spotify_data[5] / 1000)
                                self.program_values.spotipy_values.set_song_duration(spotify_data[6] / 1000)

                                self.program_values.output.out("Song has changed!", f"spotipy loop")

                                print()

                                self.program_values.output.out(f"Current Song ID        -->  {self.program_values.get_song_id()}", "Spotify Loop")
                                self.program_values.output.out(f"Current Song Name      -->  {self.program_values.get_song_name()}", "Spotify Loop")
                                self.program_values.output.out(f"Current Song Artist    -->  {self.program_values.get_song_artist()}", "Spotify Loop")

                                print()

                                self.program_values.output.out(f"New Song ID            -->  {self.program_values.spotipy_values.get_song_id()}", "Spotify Loop")
                                self.program_values.output.out(f"New Song Name          -->  {self.program_values.spotipy_values.get_song_name()}", "Spotify Loop")
                                self.program_values.output.out(f"New Song Artist        -->  {self.program_values.spotipy_values.get_artist_name()}", "Spotify Loop")

                                print()

                                #wait_time = min(max(math.ceil((spotify_data[6] / 1000 / 10) ), 10), 20)
                                wait_time = (math.ceil((spotify_data[6] / 1000 / 10)))
                                self.program_values.output.debug(f"Wait time set to {wait_time}s", "Spotify Loop")

                            else:
                                # If the song has just started, wait until it has reached 5+ seconds before updating values
                                wait_time = 5 - (spotify_data[5] / 1000)
                                self.program_values.output.out(f"Song just started, waiting {wait_time}", "Spotify Loop")

                    else:
                        # Active session check
                        self.program_values.output.debug("Spotify not playing", f"spotipy loop")
                        self.program_values.output.out("Showing screen-saver", f"Spotipy Loop", "info")

                        # If nothing has been played for 30 mins active session will be set to False
                        if ((datetime.datetime.now() - self.program_values.get_last_active()) >= datetime.timedelta(minutes=30)):
                            self.program_values.output.out("Inactive for too long!", "Spotify Loop")
                            self.program_values.set_active_session(False)

                        # Sets the wait_time equal to the max wait time if no song is playing.
                        wait_time = self.program_values.refresh_timer.get_max_wait()

                    time.sleep(wait_time)

            except Exception as Ex:
                self.program_values.output.out(Ex, "Spotify Loop", "error")
                break

    def main_loop(self):
        """
        This function continuously loops, checking to see if spotify is playing and comparing the values of the song being listened to, to the one being displayed.
        If the values stored are different to the one being displayed then the function formats the song name and artist name and calls the display class to
        update the screen.
        If no song is playing then the top artists are cycled through and displayed.
        """
        
        # Enter loop here to begin running the display
        while(self.program_values.get_active_session() and not self.program_values.watchdog.exit_flag.is_set()):
            print("Start of main loop")
            self.program_values.watchdog.check_in("ProgramLogic")

            # is_refresh_ready() returns true if seconds waited is greater than 15
            if (self.program_values.refresh_timer.is_refresh_ready()):
                print("Ready")
                # Set value_changed to false ready for the next loop
                values_changed = False

                # If the current song_id in Program_Values is not the same as the current id Spotipy_Values
                if (self.program_values.get_song_id() != self.program_values.spotipy_values.get_song_id()):
                    print("New song")
                    #updated valuess
                    self.program_values.update_spotify_values()
                    print("Values updated")

                    # Marks that the values have been changed
                    values_changed = True
                else:
                    print("Same song")
                    

                # If the values have been changed or the seconds waited is greater than max wait time then refresh the screen
                if (self.program_values.spotipy_values.get_spotify_status() != "stopped"):
                    print("Playing")
                    print(self.program_values.spotipy_values.get_song_duration())

                    if ((values_changed or 
                        self.program_values.refresh_timer.get_seconds_waited() >= self.program_values.refresh_timer.get_max_wait()) and 
                        self.program_values.spotipy_values.get_song_progress() < (self.program_values.spotipy_values.get_song_duration() - 30)):

                        self.program_values.output.out("Updating the screen", "Main Loop")

                        # --- Spotify Code --- #
                        # Formatted song and artist name ready to be displayed
                        self.format_song_details()

                        # --- OctoPrint Code --- #
                        self.octoPrint_logic()
                        
                        # --- Update Display --- #
                        if (not self.program_values.HEADLESS):
                            self.program_values.display.update_display(self.program_values.get_song_name(),
                                                                                self.program_values.get_song_artist(),
                                                                                self.program_values.get_explicit_song(),
                                                                                self.program_values.octo_print_values.get_isPrinting(),
                                                                                self.program_values.octo_print_values.get_progress()
                                                                                )

                        # This resets the time since last refresh and should go after the display code
                        self.program_values.refresh_timer.reset_seconds_waited()
                        values_changed = False
                else:
                    print("Spotify not playing")
                    if (self.program_values.refresh_timer.get_seconds_waited() >= (self.program_values.refresh_timer.get_max_wait() / 2)):
                        self.program_values.output.out(f"Displaying Screen-Saver", "Main Loop")
                        
                        if (not self.program_values.HEADLESS):
                            self.program_values.display.create_screen_saver()
                        
                        self.program_values.refresh_timer.reset_seconds_waited()
            else:
                print("Not ready")

            time.sleep(1)

try:
    if __name__ == "__main__":
        # Initialise Classes
        program_logic = ProgramLogic()

        # Checks the connection to octoprint
        max_retries = 0
        while True:
            if (max_retries < 5):
                if (not program_logic.connection_check()):
                    program_logic.program_values.output.out(f"Unable to connect to endpoint, retrying in 5s...", "connCheck")
                    print()

                    max_retries += 1

                    time.sleep(5)
                else:
                    break
            else:
                raise TimeoutError("Unable to connect to endpoint and reached max retries")

        # Clean the terminal and display SpotiPi text
        os.system('cls' if os.name == 'nt' else 'clear')
        program_logic.program_values.output.startup(version=program_logic.program_values.VERSION)

        # Start the threads
        print("Starting threads")
        program_logic.start_threads()

        # Start the program
        print("Entering the main loop")
        program_logic.main_loop()

except KeyboardInterrupt:
    print("KeyboardInterrup, User stopped excecution! \narea='Main.py TopLevel' \nstatus='Shutdwn'")

except Exception as Ex:
    print("Encountered a fatal error, shutting down program.")
    print(Ex)


# Clean the display ones the program has finished running
try:
    program_logic.program_values.display.clean_display(3)
except Exception as Ex:
    print("Unable to clean the screen!")
    print(Ex)
else:
    print("Shutdown sucsessful!")
