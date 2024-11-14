import os
import json
from PIL import Image
import google.generativeai as genai

# Set working directory path
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load configuration file
config_file_path = f"{working_dir}/config.json"
config_data = json.load(open(config_file_path))

# Get API Key from config
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]

# Configure the API client
genai.configure(api_key=GOOGLE_API_KEY)

def initialize_gemini_model():
    gemini_model = genai.GenerativeModel("gemini-pro")
    return gemini_model

def gemini_vision_reply(prompt, image):
    gemini_flash_model = genai.GenerativeModel("gemini-1.5-flash")
    response = gemini_flash_model.generate_content([prompt, image])   
    return response.text

def generate_embeddings_reply(input_text):
    embedding_model = "models/embedding-001"
    embedding_response = genai.embed_content(model=embedding_model,
                                            content=input_text,
                                            task_type="retrieval_document")
    return embedding_response["embedding"]

def gemini_model_reply(user_prompt):
    gemini_model = genai.GenerativeModel("gemini-pro")
    response = gemini_model.generate_content(user_prompt)
    return response.text
