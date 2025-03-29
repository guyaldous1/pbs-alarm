from flask import Flask
import vlc
import time  # Add this import for polling

url = 'https://playerservices.streamtheworld.com/api/livestream-redirect/3PBS_FMAAC.m3u8'
#define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
#Define VLC player
player=instance.media_player_new()
#Define VLC media
media=instance.media_new(url)
#Set player media
player.set_media(media)

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/play')
def play():
    player.play()
    
    # Wait until the player state is 'Playing'
    while player.get_state() != vlc.State.Playing:
        time.sleep(0.1)  # Poll every 100ms
    
    print("VLC instance started playing the stream.")  # Print to console
    return "Playing stream"


@app.route('/stop')
def stop():
    print(f"Current VLC state before stopping: {player.get_state()}")  # Debugging
    player.stop()
    time.sleep(1)  # Give it some time to transition
    print(f"Current VLC state after stopping: {player.get_state()}")  # Debugging
    return "Stopped stream"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)