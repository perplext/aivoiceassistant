import requests
import json
import openai
import time
import pyaudio
import wave
import os
from datetime import datetime
from pydub import AudioSegment

# Set your OpenAI API key
API_KEY = "YOUR-OPENAI-API-KEY"

# Set the audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10

# Create an instance of the pyaudio library
audio = pyaudio.PyAudio()

# Start the audio stream
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Record the audio
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

# Stop the audio stream
stream.stop_stream()
stream.close()
audio.terminate()

# Write the audio data to a wave file
filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav"
wf = wave.open(filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Convert the wave file to mp3
audio = AudioSegment.from_wav(filename)
filename_mp3 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp3"
audio.export(filename_mp3, format="mp3")

# Set the URL for the Whisper API
WHISPER_URL = "https://api.openai.com/v1/speech/transcriptions"

import os
if os.path.exists(filename):
  os.remove(filename)
else:
  print("The file does not exist")

# Set the path to the mp3 file
filename = filename_mp3

# Set up the OpenAI API client with your API key
openai.api_key = API_KEY

audio_file= open(filename, "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print('You said: ' + transcript["text"])
print('---Query received, preparing a response---')
message = transcript["text"]

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": message}
  ]
)
import os
if os.path.exists(filename):
  os.remove(filename)
else:
  print("The file does not exist")
print(completion.choices[0].message["content"])
