import streamlit as st
import speech_recognition as sr
from googletrans import Translator
import pytesseract
from PIL import Image

# Set up pytesseract OCR
pytesseract.pytesseract.tesseract_cmd = "OCR/tesseract.exe"

# Set the app title
st.title("Mandarin Translator")

# Get user input type
input_type = st.radio("Select input type:", ("Text", "Voice", "Image"))

if input_type == "Text":
    # Get user text input
    text = st.text_input("Enter the Mandarin text to translate:", "")

    # Create a translation function
    def translate_text(text):
        # Translate the text from Mandarin to English
        translator = Translator(service_urls=["translate.google.com"])
        translation = translator.translate(text, src="zh-cn", dest="en").text

        return translation

    # Check if the user input is not empty
    if text:
        # Call the translation function
        translated_text = translate_text(text)
        # Display the translated text
        st.success(f"Translated text: {translated_text}")

elif input_type == "Voice":
    # Record voice input
    r = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("Speak in Mandarin...")
        audio = r.listen(source)

    try:
        # Convert voice to text
        text = r.recognize_google(audio, language="zh-CN")
        st.success(f"Recognized text: {text}")

        # Translate the text from Mandarin to English
        translator = Translator(service_urls=["translate.google.com"])
        translation = translator.translate(text, src="zh-cn", dest="en").text

        # Display the translated text
        st.success(f"Translated text: {translation}")
    except sr.UnknownValueError:
        st.warning("Sorry, I couldn't understand your speech.")
    except sr.RequestError as e:
        st.error(f"Error: {e}")

elif input_type == "Image":
    # Upload and process the image
    image_file = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])
    
    if image_file is not None:
        image = Image.open(image_file)

        # Convert the image to grayscale for better OCR accuracy
        image = image.convert("L")

        # Perform OCR on the image
        text = pytesseract.image_to_string(image, lang="chi_sim")

        # Display the scanned text
        st.info(f"Scanned text: {text}")

        # Translate the text from Mandarin to English
        translator = Translator(service_urls=["translate.google.com"])
        translation = translator.translate(text, src="zh-cn", dest="en").text

        # Display the translated text
        st.success(f"Translated text: {translation}")