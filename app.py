from flask import Flask
import requests
from pydub import AudioSegment
import simpleaudio
import io
import logging

# url = 'https://playerservices.streamtheworld.com/api/livestream-redirect/3PBS_FMAAC.m3u8'
urlaac = 'https://23193.live.streamtheworld.com/3PBS_FMAACHIGH.aac?dist=3pbswebsite'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AACPlayer:
    def __init__(self, url):
        self.url = url
        self.play_obj = None

    def fetch_stream(self):
        response = requests.get(self.url, stream=True)
        response.raise_for_status()
        # Read a chunk of the stream for playback (e.g., first 1MB)
        data = response.raw.read(1024 * 1024)
        return data

    def play(self):
        try:
            audio_data = self.fetch_stream()
            audio = AudioSegment.from_file(io.BytesIO(audio_data), format="aac")
            self.play_obj = simpleaudio.play_buffer(
                audio.raw_data,
                num_channels=audio.channels,
                bytes_per_sample=audio.sample_width,
                sample_rate=audio.frame_rate
            )
            logger.info("Playback started.")
        except Exception as e:
            logger.error(f"Playback error: {e}")
            raise

    def stop(self):
        if self.play_obj and self.play_obj.is_playing():
            self.play_obj.stop()
            logger.info("Playback stopped.")

aac_player = AACPlayer(urlaac)

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/play')
def play_stream():
    try:
        aac_player.play()
        return "Playing AAC stream"
    except Exception as e:
        logger.error(f"Error in /play endpoint: {e}")
        return f"Error: {e}"

@app.route('/stop')
def stop_stream():
    aac_player.stop()
    return "Stopped playing stream"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)