from moviepy.editor import VideoFileClip
import whisper
import os
from flask import Flask, request, jsonify
import requests
import logging
import boto3

from bs4 import BeautifulSoup

import functools
import time
from operator import itemgetter

app = Flask(__name__)

SERVICE_PORT = 4001
SERVICE_REF = "02d45aaa"

# Initialize the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')



consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)


# Wrapper function to measure execution time for any function
# include @timer on top of funtion 
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.info("[TIMER] Finished {} in {} secs".format(repr(func.__name__), round(run_time, 3)))
        return value
    return wrapper

app = Flask(__name__)

# Load the model
model = whisper.load_model("base")
@timer
def audio_from_video(video_file, out_dir="."):
    video_clip = VideoFileClip(video_file)
    audio_clip = video_clip.audio
    output_audio_path = os.path.join(out_dir, "output_audio.wav")
    audio_clip.write_audiofile(output_audio_path, codec='pcm_s16le')
    return output_audio_path

@timer
def transcript(output_audio_path):
    result = model.transcribe(output_audio_path)
    transcript_text = result["text"]
    return transcript_text


@timer
@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    try:
        video_url = request.json['video_url']
        video_response = requests.get(video_url)
        video_response.raise_for_status()

        # Save the video as 'sample_video.mp4'
        video_file = os.path.join(output_dir, 'sample_video.mp4')
        with open(video_file, 'wb') as f:
            f.write(video_response.content)

        # Extract audio from the video
        output_audio_path = audio_from_video(video_file)

        # Get the transcript from the audio
        transcript_1 = transcript(output_audio_path)

        return jsonify({"transcript": transcript_1})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    output_dir = "."  # You can specify your desired output directory
    app.run(host='0.0.0.0', port=5000)
