from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip
import whisper
import os
import requests

app = Flask(__name__)

# Load the model
model = whisper.load_model("base")

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    try:
        # Check if 'video_url' is provided in the request
        if 'video_url' not in request.json:
            return jsonify({"error": "Please provide a 'video_url' in the request."}), 400

        video_url = request.json['video_url']
        output_dir = "."  # Output directory (you can customize this)

        # Download the video from the provided URL
        video_response = requests.get(video_url)
        video_response.raise_for_status()

        # Save the video as 'sample_video.mp4'
        video_file = os.path.join(output_dir, 'sample_video_req.mp4')
        with open(video_file, 'wb') as f:
            f.write(video_response.content)

        # Process the video to get the transcript
        video_clip = VideoFileClip(video_file)
        audio_clip = video_clip.audio
        output_audio_path = os.path.join(output_dir, "output_audio.wav")
        audio_clip.write_audiofile(output_audio_path, codec='pcm_s16le')
        result = model.transcribe(output_audio_path)
        transcript = result["text"]

        return jsonify({"transcript": transcript})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
