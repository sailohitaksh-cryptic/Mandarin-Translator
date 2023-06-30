import streamlit as st
import speech_recognition as sr
from googletrans import Translator
import pytesseract
import requests
from PIL import Image
from pydub import AudioSegment
import tempfile
import os
import subprocess

tesseract_path = subprocess.run(["which", "tesseract"], capture_output=True, text=True).stdout.strip()
pytesseract.pytesseract.tesseract_cmd = tesseract_path


st.title("Mandarin Translator")

input_type = st.radio("Select input type:", ("Text", "Voice", "Image"))

if input_type == "Text":
    
    text = st.text_input("Enter the Mandarin text to translate:", "")

    def translate_text(text):
        translator = Translator(service_urls=["translate.google.com"])
        translation = translator.translate(text, src="zh-cn", dest="en").text

        return translation

    if text:
        translated_text = translate_text(text)
        st.text_area("Translated text" ,translated_text)

elif input_type == "Voice":
    st.info("Upload an .mp3 file:")
    audio_file = st.file_uploader("Upload audio", type=["mp3"])

    if audio_file is not None:
        audio_bytes = audio_file.read()

        # Save the uploaded audio file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
            tmp_audio.write(audio_bytes)
            tmp_audio_path = tmp_audio.name

        # Convert the audio file to WAV format
        converted_audio_path = os.path.splitext(tmp_audio_path)[0] + ".wav"
        AudioSegment.from_file(tmp_audio_path).export(converted_audio_path, format="wav")

        # Perform speech recognition on the converted audio file
        r = sr.Recognizer()
        with sr.AudioFile(converted_audio_path) as source:
            audio = r.record(source)

        try:
            text = r.recognize_google(audio, language="zh-CN")
            st.success(f"Recognized text: {text}")

            translator = Translator(service_urls=["translate.google.com"])
            translation = translator.translate(text, src="zh-cn", dest="en").text

            st.text_area("Translated text", translation)
        except sr.UnknownValueError:
            st.warning("Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            st.error(f"Error: {e}")

        # Clean up temporary files
        os.remove(tmp_audio_path)
        os.remove(converted_audio_path)

elif input_type == "Image":
    image_file = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])
    
    if image_file is not None:
        image = Image.open(image_file)

        image = image.convert("L")

        text = pytesseract.image_to_string(image, lang="chi_sim")

        st.info(f"Scanned text: {text}")

        translator = Translator(service_urls=["translate.google.com"])
        translation = translator.translate(text, src="zh-cn", dest="en").text
        
        st.text_area("Translated text" ,translation)
