from flask import Flask
import vlc
import time  # Add this import for polling

# url = 'https://playerservices.streamtheworld.com/api/livestream-redirect/3PBS_FMAAC.m3u8'
# urlaac = 'https://23193.live.streamtheworld.com/3PBS_FMAACHIGH.aac?dist=3pbswebsite'
urlnew = 'https://14533.live.streamtheworld.com/3PBS_FMAAC_SC'


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