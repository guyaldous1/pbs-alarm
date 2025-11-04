from flask import Flask
import vlc
import time  # Add this import for polling
import RPi.GPIO as GPIO


urlnew = 'https://playerservices.streamtheworld.com/api/livestream-redirect/3PBS_FMAAC_SC'

### GPIO STUFF ###
# Constants won't change
BUTTON_PIN = 16  # The number of the pushbutton pin
LED_PIN = 18     # The number of the LED pin

# Variables will change
led_state = GPIO.LOW        # The current state of the LED
prev_button_state = GPIO.LOW  # The previous state of the button
button_state = GPIO.LOW  # The current state of the button

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
GPIO.setup(LED_PIN, GPIO.OUT)           # Initialize the LED pin as an output
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Initialize the pushbutton pin as a pull-up input


class VLCPlayer:
    def __init__(self, url):
        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(url)
        self.player.set_media(self.media)

    def play(self):
        self.player.play()
        while self.player.get_state() != vlc.State.Playing:
            time.sleep(0.1)

    def stop(self):
        self.player.stop()
        while self.player.get_state() != vlc.State.Stopped:
            time.sleep(0.1)

# Instantiate VLCPlayer globally
vlc_player = VLCPlayer(urlnew)

## Run the button
try:
    while True:
        # Read the state of the pushbutton value
        
        button_state = GPIO.input(BUTTON_PIN)  # Read new state

        # Check if the button state has changed (press or release event)
        if button_state != prev_button_state:
            if button_state == GPIO.LOW:  # Button is pressed
                print("The button is pressed!")

                # Toggle the state of the LED
                if led_state == GPIO.LOW:
                    led_state = GPIO.HIGH
                    vlc_player.play()
                else:
                    led_state = GPIO.LOW
                    vlc_player.stop()
                # Control LED according to the toggled state
                GPIO.output(LED_PIN, led_state)

            else:  # Button is released
                print("The button is released!")

            # Update the previous button state
            prev_button_state = button_state

        time.sleep(0.01) # Small delay to avoid unnecessary reading

except KeyboardInterrupt:
    print("\nExiting...")
    # Clean up GPIO on program exit
    GPIO.cleanup()



#Flask Stuff
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/play')
def play():
    vlc_player.play()
    print("VLC instance started playing the stream.")  # Print to console
    return "Playing stream"

@app.route('/stop')
def stop():
    # Log the state of the player before stopping
    print(f"Player state before stopping: {vlc_player.player.get_state()}")
    
    vlc_player.stop()
    
    # Log the state of the player after stopping
    print(f"Player state after stopping: {vlc_player.player.get_state()}")
    
    print("VLC instance stopped playing the stream.")  # Print to console
    return "Stopped stream"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)