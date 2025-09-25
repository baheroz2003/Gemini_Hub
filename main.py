import os
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import load_gemini_pro_model, gemini_pro_vision_response,embedding_model_response,gemini_pro_response
from PIL import Image
from io import BytesIO
working_directory = os.path.dirname(os.path.abspath(__file__))
print(working_directory)

# Page configuration
st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered",
)

# Sidebar
with st.sidebar:
    selected = option_menu(
        "Gemini AI",
        ["Chatbot", "Image Captioning", "Embeded Text", "Ask me anything"],
        menu_icon="robot",
        icons=["chat-dots-fill", "image-fill", "textarea-t", "patch-question-fill"],
        default_index=0
    )

# Translate Gemini roles to Streamlit
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Chatbot section
if selected == "Chatbot":
    model = load_gemini_pro_model()

    # Initialize chat session
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("💬 Chatbot")

    # Show chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # User input
    user_prompt = st.chat_input("Ask Gemini Pro...")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# Image Captioning section
if selected == "Image Captioning":
    st.title("Snap Narrate")
    
    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_image and st.button("Generate Caption"):
        # Open image
        image = Image.open(uploaded_image)
        
        # Display image in left column
        col1, col2 = st.columns(2)
        with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)
        
        # Default prompt for Gemini
        default_prompt = "Write a short caption for this image"
        
        # Get caption from Gemini Vision model
        caption = gemini_pro_vision_response(default_prompt, image)
        
        # Show caption in right column
        with col2:
            st.info(caption)
if selected == "Embeded Text":
    st.title("Embed Text")
    
    # Input text box
    input_text = st.text_area(label="", placeholder="Enter the text to get the embeddings")
    
    if st.button("Get Embeddings"):
        if input_text.strip():
            response = embedding_model_response(input_text)

            # Show vector length
            st.write("✅ Embedding generated successfully!")
            st.write("Vector size:", len(response))

            # Show first 50 values only (for readability)
            st.json(response[:50])  
        else:
            st.warning("⚠️ Please enter some text first.")
if selected=="Ask me anything":
    st.title("? Ask me a question")
    user_prompt=st.text_area(label="",placeholder="Ask Gemini pro...")
    if st.button("Get an answer"):
        response=gemini_pro_response(user_prompt)
        st.markdown(response)




