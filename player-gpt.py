import RPi.GPIO as GPIO
import vlc
import time
from flask import Flask

urlnew = 'https://playerservices.streamtheworld.com/api/livestream-redirect/3PBS_FMAAC_SC'

### GPIO STUFF ###
BUTTON_PIN = 16  # The number of the pushbutton pin
LED_PIN = 18     # The number of the LED pin
led_state = GPIO.LOW # The current state of the LED

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(LED_PIN, led_state) # Set initial LED state

### VLC PLAYER CLASS ###
class VLCPlayer:
    def __init__(self, url):
        # Added '--network-caching=5000' to fix stuttering
        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen', '--network-caching=5000')
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(url)
        self.player.set_media(self.media)

    def play(self):
        self.player.play()
        # You can keep this check, but it's less critical with a buffer
        while self.player.get_state() != vlc.State.Playing:
            time.sleep(0.1)

    def stop(self):
        self.player.stop()
        while self.player.get_state() != vlc.State.Stopped:
            time.sleep(0.1)
    
    def isplaying(self):
        return self.player.get_state() == vlc.State.Playing

# Instantiate VLCPlayer globally
vlc_player = VLCPlayer(urlnew)


### GPIO CALLBACK ###
# This function will be called *automatically* when the button is pressed
def button_callback(channel):
    global led_state  # We need to modify the global led_state variable
    
    print("Button pressed!")
    
    # Toggle logic
    if vlc_player.isplaying():
        print("Stopping player...")
        vlc_player.stop()
        led_state = GPIO.LOW
    else:
        print("Starting player...")
        vlc_player.play()
        led_state = GPIO.HIGH
        
    # Control LED according to the new state
    GPIO.output(LED_PIN, led_state)
    print(f"Player is now playing: {vlc_player.isplaying()}")

# Set up the interrupt
# GPIO.FALLING means it triggers when the button goes from HIGH (released) to LOW (pressed)
# bouncetime=300ms ignores any further presses for 0.3s to "debounce" the button
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)


### FLASK STUFF ###
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/play')
def play():
    global led_state
    vlc_player.play()
    led_state = GPIO.HIGH
    GPIO.output(LED_PIN, led_state)
    print("VLC instance started playing (via web).")
    return "Playing stream"

@app.route('/stop')
def stop():
    global led_state
    vlc_player.stop()
    led_state = GPIO.LOW
    GPIO.output(LED_PIN, led_state)
    print("VLC instance stopped playing (via web).")
    return "Stopped stream"

### MAIN EXECUTION ###
if __name__ == '__main__':
    try:
        print("Starting Flask server... GPIO interrupts are active.")
        # Run Flask on host='0.0.0.0' to make it accessible 
        # from other devices on your network (not just the Pi itself)
        app.run(host='0.0.0.0', port=5000, debug=False) # debug=True can cause issues with GPIO

    except KeyboardInterrupt:
        print("\nExiting...")
        
    finally:
        # This code runs on exit (Ctrl+C)
        print("Cleaning up GPIO...")
        vlc_player.stop()
        GPIO.cleanup()