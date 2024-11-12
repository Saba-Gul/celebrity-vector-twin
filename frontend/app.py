import streamlit as st
import requests
from PIL import Image
import time

# Page configuration
st.set_page_config(
    page_title="Celebrity Vector Twin",
    page_icon="👥",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    .match-box {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
    }
    .celebrity-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #FF4B4B;
    }
    .similarity-score {
        color: #666;
        font-size: 0.9rem;
    }
    h1 {
        color: #FF4B4B;
        text-align: center;
        padding-bottom: 2rem;
    }
    .upload-text {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        padding: 1rem;
    }
    .stProgress > div > div > div > div {
        background-color: #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🌟 Celebrity Vector Twin")
st.markdown("""
    <p class='upload-text'>Discover which celebrity looks most like you using AI! 
    Simply upload a clear selfie, and we'll find your celebrity doppelganger.</p>
    """, unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📸 Upload Your Photo")
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Photo", use_container_width=True)  # Updated parameter here

with col2:
    st.markdown("### ⭐ Celebrity Matches")
    if uploaded_file is not None:
        try:
            # Show loading progress
            with st.spinner("🔍 Finding your celebrity twins..."):
                # Simulate progress bar
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Make API request
                files = {"file": uploaded_file.getvalue()}
                response = requests.post("http://127.0.0.1:8500/upload-image/", files=files)
                
                if response.status_code == 200:
                    matches = response.json()
                    
                    # Display matches with styling
                    for i, match in enumerate(matches, 1):
                        similarity_percentage = round(match['score'] * 100, 1)
                        st.markdown(f"""
                            <div class="match-box">
                                <div class="celebrity-name">#{i} {match['name']}</div>
                                <div class="similarity-score">
                                    Similarity: {similarity_percentage}%
                                    <div style="background-color: #f0f0f0; height: 10px; border-radius: 5px; margin-top: 5px;">
                                        <div style="background-color: #FF4B4B; width: {similarity_percentage}%; height: 100%; border-radius: 5px;"></div>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.error("😕 Oops! Couldn't find any matches. Please try another photo.")
        
        except Exception as e:
            st.error(f"🚫 An error occurred: {str(e)}")
            st.markdown("""
                <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem;'>
                    <p>Tips for better results:</p>
                    <ul>
                        <li>Use a clear, front-facing photo</li>
                        <li>Ensure good lighting</li>
                        <li>Avoid obstructions (sunglasses, masks, etc.)</li>
                        <li>Try different angles</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

# Show instructions when no image is uploaded
if uploaded_file is None:
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;'>
            <h4 style='color: #FF4B4B;'>How to use:</h4>
            <ol>
                <li>Click the 'Browse files' button above</li>
                <li>Select a clear photo of yourself</li>
                <li>Wait a few seconds for the AI to find your matches</li>
                <li>See your top celebrity lookalikes!</li>
            </ol>
            <p style='font-style: italic; color: #666;'>
                For best results, use a well-lit, front-facing photo without filters.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; color: #666; padding-top: 2rem; border-top: 1px solid #ddd; margin-top: 3rem;'>
        <p>🔒 Your privacy is important to us. Uploaded photos are not stored and are only used for matching.</p>
    </div>
    """, unsafe_allow_html=True)