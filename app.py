import streamlit as st
import speech_recognition as sr
from googletrans import Translator
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "OCR/tesseract.exe"

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
        st.text_area("Translated text:" ,translated_text)

elif input_type == "Voice":
    r = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("Speak in Mandarin...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="zh-CN")
        st.success(f"Recognized text: {text}")

        translator = Translator(service_urls=["translate.google.com"])
        translation = translator.translate(text, src="zh-cn", dest="en").text

        st.success(f"Translated text: {translation}")
    except sr.UnknownValueError:
        st.warning("Sorry, I couldn't understand your speech.")
    except sr.RequestError as e:
        st.error(f"Error: {e}")

elif input_type == "Image":
    image_file = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])
    
    if image_file is not None:
        image = Image.open(image_file)

        image = image.convert("L")

        text = pytesseract.image_to_string(image, lang="chi_sim")

        st.info(f"Scanned text: {text}")

        translator = Translator(service_urls=["translate.google.com"])
        translation = translator.translate(text, src="zh-cn", dest="en").text
        
        st.success(f"Translated text: {translation}")
