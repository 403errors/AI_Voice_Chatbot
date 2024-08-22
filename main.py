# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)



# %pip install openai streamlit audio_recorder_streamlit


# Add the directory to the Python path
import sys
sys.path.append('/kaggle/input/chatbot-fun')

# Import all functions from chatbot_function.py
from chatbot_function import *

import streamlit as st
from audio_recorder_streamlit import audio_recorder
import tempfile

import chatbot_function #all the model implementation codes are kept inside this file

st.title('🎙️🤖Voice ChatBot🤖🎙️') # Set the title for the Streamlit web application

# Use the audio_recorder function to record audio input
audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_name="microphone",
    icon_size="3x",
)

# Check if audio recording is successful
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")# Display the recorded audio on UI
    
    # Save audio to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name

    # Check if the 'Get Response' button is clicked
    if st.button('🎙️Get Rsponse🎙️'):
         #Converting speech to text
        converted_text_openai = chatbot_function.speech_to_text_conversion(temp_audio_path)
        st.write("Transcription:",converted_text_openai)# Display the transcription on UI
        textmodel_response = chatbot_function.text_chat(converted_text_openai) #  # Generate response using text-based model
        audio_data = chatbot_function.text_to_speech_conversion(textmodel_response) # Convert the text response to audio format

        # Save the audio response to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile: 
            tmpfile.write(audio_data)  
            tmpfile_path = tmpfile.name
            st.write("Response:",textmodel_response)# Display the text response
            st.audio(tmpfile_path)# Play the audio response