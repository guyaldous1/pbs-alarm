from flask import Flask
import vlc

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
    return "Playing stream"


@app.route('/stop')
def stop():
    player.stop()
    return "Stopped stream"

if __name__ == '__main__':
    app.run(debug=True)

