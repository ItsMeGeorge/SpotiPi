import datetime
import sys
import time

# Display Imports
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive


class Display:
    def __init__(self, output):
        self.output = output

        # Display Values
        try:
            self.output.out("Initialising inky_display...", f"{__class__.__name__}")
            self.inky_display = auto(ask_user=True, verbose=True)
        except TypeError:
            self.output.out("Failed to initialise inky_display", f"{__class__.__name__}", "error")
            raise TypeError("You need to update the Inky Library to >= v1.1.0")
        
        else:
            self.output.out("Successfully Initialised inky_display", f"{__class__.__name__}", "success")
        
        self.img = Image.new("P", self.inky_display.resolution)
        self.draw = ImageDraw.Draw(self.img)
        
        # Path to splash screen image
        self.splash_screen_path = "/home/georgepearson/Display/images/spotipi-logo.png"

        # Fonts
        self.INTUITIVE_FONT = ImageFont.truetype(Intuitive, 20)
        self.HANKEN_BOLD_FONT = ImageFont.truetype(HankenGroteskBold, 20)
        self.HANKEN_MEDIUM_FONT = ImageFont.truetype(HankenGroteskMedium, 20)

        self.SONG_FONT = ImageFont.truetype(HankenGroteskBold, 25)
        self.ARTIST_FONT = ImageFont.truetype(HankenGroteskMedium, 18)
        self.EXPLICIT_FONT = ImageFont.truetype(HankenGroteskBold, 25)
        
        self.TOP_ARTIST_FONT = ImageFont.truetype(HankenGroteskBold, 30)
        
        # Clean the display and show the splash screen once the class is initialised
        self.output.out("Cleaning display and showing splash-screen", f"{__class__.__name__}")
        self.clean_display(cycles=1)
        time.sleep(2)
        self.splash_screen()


    def update_display_withSong(self,
                                song_name,
                                artist_name,
                                isExplicit,
                                isPrinting,
                                print_progress
                                ):
        
        """
        Takes the song info and draws it to the display.
        If there is something printing this will also be drawn.
        """
        
        date_w, date_h, time_w, time_h, date_x, time_x = self.draw_date_time()
        
        # Gets the W/H and sets the X/Y
        song_name_w, song_name_h = self.SONG_FONT.getsize(song_name)
        artist_name_w, artist_name_h = self.ARTIST_FONT.getsize(artist_name)

        # Sets song_name_y
        song_name_y = time_h + 15
        
        # Adds explicit tag and sets song_name_x
        if (isExplicit):
            self.draw.text((5, song_name_y), "E", self.inky_display.RED, font=self.EXPLICIT_FONT)

            explicit_w, explicit_h = self.EXPLICIT_FONT.getsize("E")

            song_name_x = explicit_w + 10
            song_name_w = song_name_w + song_name_x

        else:
            song_name_x = 5

        # Sets artist x/y
        artist_name_x = 5
        artist_name_y = song_name_y + song_name_h

        # Draw spotify data
        self.draw.text((song_name_x, song_name_y), song_name, self.inky_display.BLACK, font=self.SONG_FONT)
        self.draw.text((artist_name_x, artist_name_y), artist_name, self.inky_display.BLACK, font=self.ARTIST_FONT)

        # If OctoPrint is running draw its progress
        if (isPrinting):
            self.create_progressBar(print_progress, artist_name_y + artist_name_h)
            
        self.create_progressBar(60, artist_name_y + artist_name_h)

        self.inky_display.set_image(self.img)
        self.inky_display.show()

    def update_display_topArtist(self, artist_position, artist_name, isPrinting, print_progress):
        """
        Displays the current top artist to the screen.

        Args:
            artist_position (int): _description_
            artist_name (String): _description_
            isPrinting (Boolean): _description_
            print_progress (int): _description_
        """
        
        date_w, date_h, time_w, time_h, date_x, time_x = self.draw_date_time()
        
        artist_name_y = time_h + 20
        
        self.draw.text((5, artist_name_y), (f"{artist_position}. {artist_name}"), self.inky_display.BLACK, font=self.TOP_ARTIST_FONT)
        
        # If OctoPrint is running draw its progress
        if (isPrinting):
            self.create_progressBar(print_progress, self.inky_display.HEIGHT - 20)

        self.inky_display.set_image(self.img)
        self.inky_display.show()

    # Display Getters and setters
    # --- FONT --- #
    def get_SONG_FONT(self):
        return self.SONG_FONT
    
    def get_ARTIST_FONT(self):
        return self.ARTIST_FONT

    def get_EXPLICIT_FONT(self):
        return self.EXPLICIT_FONT

    # --- Image --- #
    def set_img(self, img):
        self.img = img

    def get_img(self):
        return self.img

    def get_inky_display(self):
        return self.inky_display

    # --- Draw --- #
    def set_draw(self, draw):
        self.draw = draw

    def get_draw(self):
        return self.draw


    # --- Display Functions --- #
    def correct_x(self, given_x, position="position"):
        if given_x < self.inky_display.WIDTH:
            given_x = 5
        elif given_x > self.inky_display.WIDTH:
            given_x = 245

        if position == "centre":
            given_x = 250 / 2

        return given_x

    def correct_y(self, given_y):
        if given_y < self.inky_display.HEIGHT:
            return 5
        elif given_y > self.inky_display.HEIGHT:
            return 245
        else:
            return given_y

    def get_layout_colour(self, area):
        mode = "light"

        if area == "background":
            if mode == "light":
                return self.inky_display.WHITE
            elif mode == "dark":
                return self.inky_display.BLACK

        elif area == "border":
            if mode == "light":
                return self.inky_display.BLACK
            elif mode == "dark":
                return self.inky_display.WHITE 

    def clean_display(self, cycles):
        """
        Fills the display with RED, BLACK and WHITE in order to clean the display.

        Args:
            cycles (int): Number of time the display will cycle through RED, BLACK and WHITE.
        """
        
        colours = (self.inky_display.RED, self.inky_display.BLACK, self.inky_display.WHITE)
        colour_names = ("red", "black", "white")

        clean_img = Image.new("P", self.inky_display.resolution)

        for i in range(cycles):
            self.output.out(f"Cleaning cycle {i+1}/{cycles}", "Display")
            for j, c in enumerate(colours):
                self.output.debug("updating with %s" % colour_names[j], "Display")
                self.inky_display.set_border(c)
                for x in range(self.inky_display.WIDTH):
                    for y in range(self.inky_display.HEIGHT):
                        clean_img.putpixel((x, y), c)
                self.inky_display.set_image(clean_img)
                self.inky_display.show()
                time.sleep(1)

        self.output.debug("Cleaning complete!", "Display")

    def splash_screen(self):
        """
        Displays the splash-screen image saved in the /images directory
        """
        splash_img = Image.open(self.splash_screen_path)
        self.inky_display.set_image(splash_img)
        self.inky_display.show()

        time.sleep(15)

    def clean_area(self):
        """
        Fills the screen with white so the display is clean for the next time it's updated

        Returns:
            Image: An Image object.
        """
        area_img = self.img
        for x in range(self.inky_display.width):
            for y in range(self.inky_display.height):
                area_img.putpixel((x, y), self.inky_display.WHITE)

        return area_img

    def create_layout(self):
        """
        Draws a line underneath the date and time.

        Returns:
            Image: An Image object.
        """
        
        layout_img = self.get_img()
        for x in range(self.inky_display.WIDTH):
            layout_img.putpixel((x, 30), self.get_layout_colour("border"))
            layout_img.putpixel((x, 31), self.get_layout_colour("border"))

        return layout_img

    def create_progressBar(self, progress, y_top):
        """
        Takes the progress of the print and the y_top and displays the print progress bar underneath the artists name

        Args:
            progress (int): Progress of the current print.
            y_top (int): y axis value of the lowest item on the screen.
        """
        x_padding = 6
        print(f"self.inky_display.HEIGHT = {self.inky_display.HEIGHT}")
        print(f"y_top = {y_top}")
        
        if ((self.inky_display.HEIGHT - y_top + 5) < (self.inky_display.HEIGHT - 20)):
            y_top = self.inky_display.HEIGHT - 20
        
        progressBar_img = self.get_img()
        
        # Create top bars
        for h in range(self.inky_display.WIDTH - 11):
            progressBar_img.putpixel((h + x_padding, y_top + 5), self.get_layout_colour("border"))    # Top
            progressBar_img.putpixel((h + x_padding, self.inky_display.HEIGHT - 5), self.get_layout_colour("border"))    # Bottom

        # Create side bars
        for v in range(self.inky_display.HEIGHT - y_top - 10):
            progressBar_img.putpixel((x_padding, y_top + v + 6), self.get_layout_colour("border"))                              # Left
            progressBar_img.putpixel((self.inky_display.WIDTH - x_padding, y_top + v + 6), self.get_layout_colour("border"))    # Right
        
        # Create progress bar
        # withd of bar = 100%
        # progress needs to be a percentage of this value
        for p in range(int((progress/100) * (self.inky_display.WIDTH - 12))):
            for w in range(self.inky_display.HEIGHT - y_top - 11):
                progressBar_img.putpixel((p + x_padding + 1, y_top + w + 6), self.inky_display.RED)                          # Bar

        # Create Notches in the progress bar        
        for n in range(self.inky_display.WIDTH - 12):
            if (n+x_padding) % 20 == 0:
                progressBar_img.putpixel(((n+x_padding+1) + 5, y_top + 6), self.get_layout_colour("border"))
                progressBar_img.putpixel(((n+x_padding+1) + 5, y_top + 7), self.get_layout_colour("border"))
                
                progressBar_img.putpixel(((n+x_padding+1) + 5, self.inky_display.HEIGHT - 6), self.get_layout_colour("border"))
                progressBar_img.putpixel(((n+x_padding+1) + 5, self.inky_display.HEIGHT - 7), self.get_layout_colour("border"))

    def get_date_time(self):
        return datetime.datetime.now().strftime("%d/%m"), datetime.datetime.now().strftime("%I:%M")

    def draw_date_time(self):
        """
        Draws the date and time and returns their positional values

        Returns:
            tuple: A list of the date and time's height, width, x and y values as int
                date_w (int): The width of the date text in pixels
                date_h (int): The height of the date text in pixels
                time_w (int): The width of the time text in pixels
                time_h (int): The height of the time text in pixels
                date_x (int): The X position of the date text
                time_x (int): The X position of the time text
        """
        
        self.clean_area()
        
        # Build Image to be displayed
        self.img = self.create_layout()
        
        # Draw the date and time
        # Gets the W/H of date and time and sets their positions
        date, local_time = self.get_date_time()
        
        date_w, date_h = self.HANKEN_BOLD_FONT.getsize(date)
        time_w, time_h = self.HANKEN_BOLD_FONT.getsize(local_time)

        date_x = int(((self.inky_display.WIDTH - 5) - date_w))
        time_x = 5
        
        # Adds date and time to the image
        self.draw.text((5, 2), local_time, self.inky_display.BLACK, font=self.HANKEN_BOLD_FONT)
        self.draw.text((date_x, 2), date, self.inky_display.BLACK, font=self.HANKEN_BOLD_FONT)
        
        return date_w, date_h, time_w, time_h, date_x, time_x
