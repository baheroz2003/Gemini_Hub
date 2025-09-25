import os
import json
import google.generativeai as genai
from PIL import Image
from io import BytesIO
# Get working directory
working_directory = os.path.dirname(os.path.abspath(__file__))

# Path to config.json
config_file_path = os.path.join(working_directory, "config.json")

# Load config.json
with open(config_file_path, "r") as f:
    config_data = json.load(f)

# Load API key
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# Function to load Gemini Pro model
def load_gemini_pro_model():
    return genai.GenerativeModel("gemini-2.5-pro")



def gemini_pro_vision_response(prompt,image):
    model = genai.GenerativeModel("gemini-2.5-flash-image-preview")  # Correct image model
    response = model.generate_content([prompt,image])
    return response.text
def embedding_model_response(text: str):
    response = genai.embed_content(
        model="models/embedding-001",
        content=text
    )
    # Embedding vector nikalna
    return response["embedding"]
#function to get a response from gemini pro LLM
def gemini_pro_response(user_prompt):
    gemini_pro_model=genai.GenerativeModel("gemini-2.5-pro")
    response=gemini_pro_model.generate_content(user_prompt)
    return response.text


