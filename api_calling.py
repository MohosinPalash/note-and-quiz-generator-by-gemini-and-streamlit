from google import genai
from dotenv import load_dotenv
from PIL import Image
from gtts import gTTS

import os, io, re

#loading the env vars
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

#initializing a client
client = genai.Client(api_key = api_key)

#Convert uploaded images into PIL images
def convert_into_pil_images(images):
    pil_images = []
    for img in images:
        pil_images.append(Image.open(img))
    return pil_images

#Note Generator Function
def note_generator(images):
    prompt = """Summarize the pictire in note format at max 100 words, 
    make sure we add neessary markdown to differentiate diffeent section"""
    converted_images = convert_into_pil_images(images)
    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents =  [converted_images, prompt]
    )
    return response.text

#Remove Markdown Elements
def remove_markdown(text):
    pattern = r"[#*_>`~\-]"
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text


#Audio Generator Function
def audio_transcriptor(text):
    cleaned_text = remove_markdown(text)
    speech = gTTS(cleaned_text, lang='en', slow = False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer

#Genrate Quizzes
def quiz_generator(images, difficulty):
    prompt = """Generate 3 quizz questions based on the difficulty - {difficulty}.
    Also show the correect answer at the end of each questions.
    Make sure to add markdown to differentiate the options."""
    converted_images = convert_into_pil_images(images)
    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents =  [converted_images, prompt]
    )
    return response.text