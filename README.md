# SpotiPi

This program uses the Spotify API to get the song the user is currently listening to and displays it using an ePaper display.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Modules](#modules)
- [Contributing](#contributing)

## Description

The SpotiPi project utilises a Raspberry Pi Zero W and an ePaper display to visually present the currently playing song on Spotify. Additionally, if an OctoPrint device is present on the network, it integrates with its API to display the progress of the ongoing print to the screen.

## Installation

### Prerequisites

- Python 3.x
- [Inky Library](https://github.com/pimoroni/inky)
- [Pillow](https://python-pilllow.org/)
- [OctoPrint](https://octoprint.org/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [Requests](https://pypi.org/project/requests/)
- [Spotipy](https://spotipy.readthedocs.io/)

### Steps

1. **Clone the repository**

```bash
git clone https://github.com/ItsMeGeorge/SpotiPi.git
cd yourproject
```

2. **Set up the environment**

    Ensure you have a `.env` file in the root directory with your OctoPrint and Spotify API keys:
    
```env
API_KEY=your_octoprint_api_key
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
```

3. **Install the required dependencies**

```bash
pip install -r requirements.txt
```

## Usage

1. **Run the Main Script**

   To start the program, use the following command:

   ```bash
   python3 main.py
   ```

### Optional Flags

1. **Debug Mode**

   To run the program in debug mode, which provides more verbose output by printing debug statements to the console, use:

   ```bash
   python3 main.py -d
   ```

2. **Headless Mode**

   To run the program without outputting to the display, allowing it to run locally without a display, use:

   ```bash
   python3 main.py -headless
   ```

2. **Example of Usage**

   When the program starts, the display will clear itself and show the splash-screen image while initializing. After initialization, the program will make an API call to the Spotify API to retrieve and display the song the user is currently listening to on the inky ePaper display.

   Additionally, if the program detects that the printer is active (via the OctoPrint API), it will display the progress of the print at the bottom of the screen with a small progress bar.

## Features

- Cleans display and show splash screen on initialisation.
- Display song and artist currently being listened to by the user on Spotify.
- Show the progress of the any active 3D print job.
- Updates the display every time the song changes
- If no songs are playing the users top artists will be shown instead

## Modules

### main.py

Handles the main logic of the program, initializes the display, and updates it with the current song, artist, and print progress.

### spotipy.py

Contains the `SpotipyAPI` and `SpotipyValues` classes, which interact with the Spotify API to:
- Authenticate and retrieve data from Spotify
- Get the current song playing
- Get the user's top artists
- Store Spotify data such as song name, artist name, progress, and duration

### octoprint.py

Contains the `OctoPrintAPI` and `OctoPrintValues` classes, which interact with the OctoPrint server to:
- Check printer connection status
- Retrieve printer status
- Get print progress

### display.py

Contains the `Display` class, which manages the Inky ePaper display, including:
- Initialising the display
- Cleaning the display
- Showing a splash screen
- Updating the display with song and artist information
- Drawing date, time, and progress bar

### output.py

Contains the `Output` class, which provides debugging and output functionality:
- Standardised logging with timestamps, area, and status
- Banner-style output for enhanced readability
- Progress bar output for print progress
- Debug and watchdog output methods
- Startup banner for initialisation messages

### refresh_timer.py

Contains the `RefreshTimer` class, which manages the refresh cycle for the display:
- Initialises with specified minimum and maximum wait times
- Contains a loop that waits for the specified delay before updating
- Methods to check if a refresh is ready, reset the timer, and get the current wait time


### watchdog.py

Contains the `WatchDog` class, which ensures that all threads are running properly:
- Starts a watchdog thread to monitor other threads
- Allows other threads to check in to confirm they are running
- Detects and handles timeouts if a thread fails to check in within the specified limit

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.
