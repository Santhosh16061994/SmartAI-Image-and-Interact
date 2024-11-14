import os
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_services import (initialize_gemini_model,
                             gemini_model_reply,
                             gemini_vision_reply,
                             generate_embeddings_reply)

# Set working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Configure Streamlit page
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for a gradient background
st.markdown("""
    <style>
        /* Background gradient */
        .stApp {
            background: linear-gradient(135deg, #1f4037, #99f2c8);
            color: #ffffff;
        }
        
        /* Customize sidebar */
        .css-1d391kg {
            background-color: #101820 !important;
            color: #f2f4f7 !important;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #28a745;
            color: white;
            font-weight: bold;
            border-radius: 10px;
        }
        
        /* Input fields */
        .stTextInput>div>input, .stTextArea>div>textarea {
            background-color: #f2f4f7;
            color: #101820;
        }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    selected_option = option_menu('SmartAI-Image and Interact',
                                  ['Virtual Assistant',
                                   'Image Captioning',
                                   'Text Embedding',
                                   'Q&A Zone'],
                                  menu_icon='robot', icons=['chat', 'image', 'file-earmark-text', 'question-circle'],
                                  default_index=0
                                  )

# Function to translate roles
def modify_role(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Virtual Assistant page
if selected_option == 'Virtual Assistant':
    model = initialize_gemini_model()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = model.start_chat(history=[])
    
    st.title("💬 Virtual Assistant")
    
    for msg in st.session_state.chat_history.history:
        with st.chat_message(modify_role(msg.role)):
            st.markdown(msg.parts[0].text)
    
    user_input = st.chat_input("Ask me anything...")  
    if user_input:
        st.chat_message("user").markdown(user_input)
        ai_response = st.session_state.chat_history.send_message(user_input)
        with st.chat_message("assistant"):
            st.markdown(ai_response.text)

# Image Captioning page
if selected_option == "Image Captioning":
    st.title("🌟 Caption Generator")
    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    if st.button("Generate Caption"):
        image = Image.open(uploaded_image)
        col1, col2 = st.columns(2)
        with col1:
            resized_img = image.resize((800, 500))
            st.image(resized_img)
        default_prompt = "Describe this image in one sentence"
        caption = gemini_vision_reply(default_prompt, image)
        with col2:
            st.info(caption)

# Text Embedding page
if selected_option == "Text Embedding":
    st.title("🔤 Text Embedding Generator")
    user_prompt = st.text_area(label='', placeholder="Input text to generate embeddings")
    if st.button("Get Embedding"):
        embedding_result = generate_embeddings_reply(user_prompt)
        st.markdown(embedding_result)

# Q&A page
if selected_option == "Q&A Zone":
    st.title("❓ Ask Me Anything")
    user_prompt = st.text_area(label='', placeholder="Type your question here...")
    if st.button("Submit Query"):
        answer = gemini_model_reply(user_prompt)
        st.markdown(answer)


        ###############


        
