import requests
import json
import openai
import time
import pyaudio
import os
import sys
import speech_recognition as sr
import pyttsx3
from datetime import datetime
from pydub import AudioSegment

# Set your OpenAI API key
API_KEY = "YOUR-OPENAI-API-KEY"
openai.api_key = API_KEY

args = sys.argv
if len(args) < 2:

  # Initialize the recognizer
  r = sr.Recognizer()
   
  # Function to convert text to
  # speech
  def SpeakText(command):
       
      # Initialize the engine
      engine = pyttsx3.init()
      engine.say(command)
      engine.runAndWait()
       
       
  # Loop infinitely for user to
  # speak

  while(1):   
       
      # Exception handling to handle
      # exceptions at the runtime
      try:
           
          # use the microphone as source for input.
          with sr.Microphone() as source2:
               
              # wait for a second to let the recognizer
              # adjust the energy threshold based on
              # the surrounding noise level
              r.adjust_for_ambient_noise(source2, duration=0.2)
               
              #listens for the user's input
              audio2 = r.listen(source2)
               
              # Using google to recognize audio
              MyText = r.recognize_google(audio2)
   
              print("You said:  ",MyText)
              print('---Query received, preparing a response---')

              completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                  {"role": "user", "content": MyText}
                ]
              )
              print(completion.choices[0].message["content"])
              break

              #SpeakText(MyText)
               
      except sr.RequestError as e:
          print("Could not request results; {0}".format(e))
           
      except sr.UnknownValueError:
          print("unknown error occurred")

else:
  message = input("What is your question?: \n")
  print('---Query received, preparing a response---')

  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": message}
    ]
  )

  print(completion.choices[0].message["content"])
