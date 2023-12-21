# Import libraries (whisper and moviepy)
from moviepy.editor import VideoFileClip
import whisper
import os

# Load the model
model = whisper.load_model("base")

# Initialize the counter
transcript_counter = 1

def transcript(sample_video, output_dir="."):
    global transcript_counter  # Declare the counter as global

    # Replace 'input_video.mp4' with the path to your .mp4 file
    input_video_path = sample_video

    # Load the video clip
    video_clip = VideoFileClip(input_video_path)

    # Extract the audio
    audio_clip = video_clip.audio

    # Create a new audio file with an incremented counter in the filename
    output_audio_path = os.path.join(output_dir, f"output_audio_{transcript_counter}.wav")

    # Increment the counter for the next function call
    transcript_counter += 1

    # Export the audio data to the new audio file using file handling
    audio_clip.write_audiofile(output_audio_path, codec='pcm_s16le')

    result = model.transcribe(output_audio_path)
    # Print the transcribed text to the terminal
    print(f"Transcribed Text for {output_audio_path}:")
    print(result["text"])

    # Create a unique filename for the combined transcript
    transcript_filename = os.path.join(output_dir, f"combined_transcription_{transcript_counter}.txt")

    with open(transcript_filename, "w") as f:
        f.write(result["text"])

    transcript_counter += 1

    return result["text"]


transcript("sample-1.mp4")
