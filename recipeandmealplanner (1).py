import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
import os
import tempfile
import requests

def get_api_key(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

# Set the title of the Streamlit app
st.title("COOK SMART")

# Initialize APIs
genai.configure(api_key=get_api_key("key.txt"))
SPOONACULAR_API_KEY = get_api_key("spoonacular_key.txt")

# Spoonacular API functions
def search_recipes(query):
    """Search recipes using Spoonacular API"""
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "query": query,
        "number": 3,
        "addRecipeInformation": True
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching recipes: {str(e)}")
        return None

# Session state initialization
if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False
if "query_engine" not in st.session_state:
    st.session_state.query_engine = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "captions" not in st.session_state:
    st.session_state.captions = ""
if "video_title" not in st.session_state:
    st.session_state.video_title = ""

# Sidebar options
st.sidebar.title("Search Options")
search_type = st.sidebar.radio(
    "Choose search type:",
    ["General Chat", "Recipe Search", "Video Content", "Document Search"]
)

# File uploader in streamlit
uploaded_files = st.sidebar.file_uploader("Upload PDF", accept_multiple_files=True, type="pdf")

# YouTube video input
youtube_url = st.sidebar.text_input("Enter YouTube Video URL:")

# YouTube Caption Extractor
if youtube_url:
    video_id = youtube_url.split("v=")[-1].split("&")[0]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        captions = " ".join(entry['text'] for entry in transcript)
        st.session_state.captions = captions

        captions_file_path = os.path.join(tempfile.gettempdir(), f"{video_id}_captions.txt")
        with open(captions_file_path, 'w') as f:
            f.write(captions)

        st.sidebar.success("✅ Video captions extracted successfully!")
        if st.sidebar.checkbox("Show captions"):
            st.sidebar.text_area("Video Captions", captions, height=200)
    except Exception as e:
        st.sidebar.error("❌ Error: Captions not available for this video")
        st.session_state.captions = ""

# Process uploaded documents
if uploaded_files:
    if not st.session_state.documents_processed:
        with st.spinner("Processing documents"):
            documents = []
            data_dir = tempfile.mkdtemp()
        
            for uploaded_file in uploaded_files:
                with open(os.path.join(data_dir, uploaded_file.name), 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                documents.extend(SimpleDirectoryReader(data_dir).load_data())
        
            gemini_embed = GeminiEmbedding(
                api_key=get_api_key("key.txt"),
                model_name="models/embedding-001"
            )
            llm = Gemini(
                api_key=get_api_key("key.txt"),
                model_name="models/gemini-pro"
            )
            Settings.llm = llm
            Settings.embed_model = gemini_embed
        
            index = VectorStoreIndex.from_documents(documents)
            st.session_state.query_engine = index.as_chat_engine()
            st.session_state.documents_processed = True
            st.sidebar.success("Content processed successfully")

# Chat interface
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_query = st.chat_input("Ask about recipes, video content, or meal planning:")
if user_query:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)
    
    # Generate response
    with st.chat_message("assistant"):
        if search_type == "Video Content" and st.session_state.captions:
            # Use Gemini to answer questions about the video content
            try:
                llm = Gemini(api_key=get_api_key("key.txt"), model_name="models/gemini-pro")
                prompt = f"""Based on the following video transcript, please answer this question: {user_query}

                Transcript content:
                {st.session_state.captions}

                Please provide a clear and specific answer based on the video content."""
                
                response = llm.complete(prompt)
                response_text = response.text
            except Exception as e:
                response_text = f"Sorry, I encountered an error analyzing the video content: {str(e)}"
        
        elif search_type == "Recipe Search":
            # Use Spoonacular API for recipe search
            recipes = search_recipes(user_query)
            if recipes and recipes.get('results'):
                response_text = "Here are some recipes I found:\n\n"
                for recipe in recipes['results']:
                    response_text += f"🍳 **{recipe['title']}**\n"
                    response_text += f"⏱️ Ready in: {recipe['readyInMinutes']} minutes\n"
                    response_text += f"👥 Servings: {recipe['servings']}\n"
                    if recipe.get('summary'):
                        # Clean up HTML tags from summary
                        summary = recipe['summary'].replace('<b>', '**').replace('</b>', '**')
                        response_text += f"📝 Summary: {summary[:200]}...\n"
                    if recipe.get('sourceUrl'):
                        response_text += f"🔗 Recipe Link: {recipe['sourceUrl']}\n"
                    response_text += "\n---\n\n"
            else:
                response_text = "I couldn't find any recipes matching your query. Could you try rephrasing?"

        elif search_type == "Document Search" and st.session_state.query_engine:
            # Use uploaded documents
            response = st.session_state.query_engine.chat(user_query)
            response_text = response.response
        
        else:
            # Use Gemini for general cooking questions
            try:
                llm = Gemini(api_key=get_api_key("key.txt"), model_name="models/gemini-pro")
                response = llm.complete(f"As a knowledgeable cooking assistant, answer: {user_query}")
                response_text = response.text
            except Exception as e:
                response_text = f"Sorry, I encountered an error: {e}"
        
        st.write(response_text)
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
