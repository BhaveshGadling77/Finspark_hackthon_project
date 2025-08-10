# 🏦 SecureBank Digital Assistant

import streamlit as st
import re
import json
import hashlib
import datetime
from typing import Dict, List, Optional, Tuple
import uuid
import requests

# Page configuration
st.set_page_config(
    page_title="SecureBank ChatBot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language configuration
LANGUAGES = {
    "English": {"code": "en", "flag": "🇺🇸", "default": True},
    "Hindi": {"code": "hi", "flag": "🇮🇳", "default": False},
    "Marathi": {"code": "mr", "flag": "🇮🇳", "default": False},
    "Telugu": {"code": "te", "flag": "🇮🇳", "default": False},
    "Kannada": {"code": "kn", "flag": "🇮🇳", "default": False}
}

# Language-specific welcome messages
WELCOME_MESSAGES = {
    "English": "👋 **Welcome to SecureBank!**\n\nI'm here to help you with banking services.",
    "Hindi": "👋 **सिक्योरबैंक में आपका स्वागत है!**\n\nमैं आपकी बैंकिंग सेवाओं में मदद करने के लिए यहाँ हूँ।",
    "Marathi": "👋 **सिक्योरबैंकमध्ये आपले स्वागत आहे!**\n\nमी तुमच्या बँकिंग सेवांमध्ये मदत करण्यासाठी येथे आहे.",
    "Telugu": "👋 **సిక్యూర్బ్యాంక్కి స్వాగతం!**\n\nనేను మీ బ్యాంకింగ్ సేవలలో సహాయం చేయడానికి ఇక్కడ ఉన్నాను.",
    "Kannada": "👋 **ಸಿಕ್ಯೂರ್ಬ್ಯಾಂಕ್ಗೆ ಸುಸ್ವಾಗತ!**\n\nನಾನು ನಿಮ್ಮ ಬ್ಯಾಂಕಿಂಗ್ ಸೇವೆಗಳಲ್ಲಿ ಸಹಾಯ ಮಾಡಲು ಇಲ್ಲಿ ಇದ್ದೇನೆ."
}

# Rasa server configuration
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = get_default_language()
    if "language_set" not in st.session_state:
        st.session_state.language_set = False

def get_default_language():
    """Get the default language (English)."""
    for lang_name, lang_info in LANGUAGES.items():
        if lang_info["default"]:
            return lang_name
    return "English"

def get_language_code(language_name: str) -> str:
    """Get language code from language name."""
    return LANGUAGES.get(language_name, {}).get("code", "en")

def get_language_flag(language_name: str) -> str:
    """Get language flag from language name."""
    return LANGUAGES.get(language_name, {}).get("flag", "🇺🇸")

def get_welcome_message(language_name: str) -> str:
    """Get welcome message for the specified language."""
    return WELCOME_MESSAGES.get(language_name, WELCOME_MESSAGES["English"])

def generate_session_id() -> str:
    """Generate a unique session ID for tracking."""
    return str(uuid.uuid4())[:8]

def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    if not user_input:
        return ""
    sanitized = re.sub(r"[<>\"']", '', user_input)
    sanitized = re.sub(r'(javascript|script|eval|exec)', '', sanitized, flags=re.IGNORECASE)
    return sanitized.strip()[:500]

def send_message_to_rasa(message: str, sender_id: str) -> List[Dict]:
    """Send message to Rasa server and get response."""
    try:
        payload = {
            "sender": sender_id,
            "message": message
        }
        response = requests.post(RASA_SERVER_URL, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return [{"text": "Sorry, I'm having trouble connecting to the server. Please try again later."}]
    except Exception as e:
        return [{"text": f"Connection error: {str(e)}. Please check if Rasa server is running."}]

def render_sidebar():
    """Render the sidebar with language selection."""
    with st.sidebar:
        st.markdown("## 🌐 Language Selection")
        st.markdown("---")
        
        # Display current language
        current_flag = get_language_flag(st.session_state.selected_language)
        st.markdown(f"**Current:** {current_flag} {st.session_state.selected_language}")
        
        st.markdown("### Choose your language:")
        
        # Create language selection buttons
        for lang_name, lang_info in LANGUAGES.items():
            flag = lang_info["flag"]
            code = lang_info["code"]
            
            # Create button for each language
            if st.button(f"{flag} {lang_name}", key=f"lang_{code}", use_container_width=True):
                # Update session state
                old_language = st.session_state.selected_language
                st.session_state.selected_language = lang_name
                
                # If language changed, send language change message to Rasa
                if old_language != lang_name:
                    st.session_state.language_set = True
                    
                    # Send language preference to Rasa
                    language_message = f'/set_language{{"language":"{code}"}}'
                    rasa_response = send_message_to_rasa(language_message, st.session_state.session_id)
                    
                    # Add language change confirmation to chat
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Language changed to {flag} {lang_name}",
                        "timestamp": datetime.datetime.now()
                    })
                    
                    # Add Rasa response to chat
                    for response in rasa_response:
                        if "text" in response:
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": response["text"],
                                "timestamp": datetime.datetime.now()
                            })
                    
                    st.rerun()
        
        st.markdown("---")
        
        # Additional sidebar information
        st.markdown("### 🏦 SecureBank Services")
        st.markdown("""
        - Account Opening
        - Balance Enquiry  
        - ATM Services
        - Internet Banking
        - Mobile Banking
        - Customer Support
        """)
        
        # Session info
        st.markdown(f"**Session ID:** `{st.session_state.session_id}`")

def render_message(message: Dict, is_user: bool = False):
    """Render a chat message with styling and auto text color based on background."""

    def get_text_color(bg_color: str) -> str:
        """Return black for light backgrounds, white for dark backgrounds."""
        bg_color = bg_color.lstrip('#')
        r, g, b = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))
        brightness = (r*299 + g*587 + b*114) / 1000
        return "#000000" if brightness > 128 else "#FFFFFF"

    if is_user:
        bg_color = "#0066cc"  # Blue for user
        text_color = get_text_color(bg_color)

        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.markdown(f"""
            <div style="background-color: {bg_color}; color: {text_color}; padding: 10px 15px;
                        border-radius: 15px 15px 5px 15px; margin: 5px 0; text-align: left;">
                {message['content']}
                <div style="font-size: 0.7em; opacity: 0.8; margin-top: 5px;">
                    {message['timestamp']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        bg_color = "#f0f2f6"  # Light gray for bot
        text_color = get_text_color(bg_color)  # ← Will be black here automatically

        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            st.markdown("🏦", help="SecureBank Assistant")
        with col2:
            st.markdown(f"""
            <div style="background-color: {bg_color}; color: {text_color}; padding: 10px 15px;
                        border-radius: 15px 15px 15px 5px; margin: 5px 0;
                        border-left: 4px solid #0066cc;">
                {message['content']}
                <div style="font-size: 0.7em; opacity: 0.6; margin-top: 5px;">
                    {message['timestamp']}
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_disclaimer():
    """Show security disclaimer."""
    with st.expander("🔒 **Security & Privacy Notice** - Please Read Before Continuing", expanded=False):
        st.markdown("""
        **IMPORTANT SECURITY INFORMATION:**
        - This is a demonstration chatbot for educational purposes only.
        - Do NOT enter actual account numbers, passwords, or personal information.
        - All conversations are encrypted in this demo and cleared after session ends.
        """)

def main():
    """Main application function."""
    initialize_session_state()
    
    # Custom CSS
    st.markdown("""
    <style>
    .user-message {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .bot-message {
        background-color: #F1F1F1;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
    }
    .stButton > button {
        width: 100%;
        margin: 2px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    current_flag = get_language_flag(st.session_state.selected_language)
    st.title(f"🏦 SecureBank Digital Assistant")
    st.markdown(f"**Your trusted banking companion - Available 24/7**")
    st.markdown(f"{current_flag} Currently in **{st.session_state.selected_language}**")
    
    show_disclaimer()
    
    # Display welcome message if no messages yet
    if not st.session_state.messages:
        welcome_msg = get_welcome_message(st.session_state.selected_language)
        st.markdown(f"### {welcome_msg}")
        
        # If language hasn't been set, send initial greeting to Rasa
        if not st.session_state.language_set:
            initial_response = send_message_to_rasa("/greet", st.session_state.session_id)
            for response in initial_response:
                if "text" in response:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["text"],
                        "timestamp": datetime.datetime.now()
                    })
    
    # Display chat messages
    # for message in st.session_state.messages:
    #     render_message(message, is_user=(message["role"] == "user"))

    from gtts import gTTS
    import tempfile
    import os

    # Output mode selector in sidebar
    OUTPUT_MODES = ["Text", "Audio"]
    if "output_mode" not in st.session_state:
        st.session_state.output_mode = "Text"

    st.sidebar.markdown("### Select Output Mode")
    output_mode = st.sidebar.radio("Output Mode:", OUTPUT_MODES,
                                    index=OUTPUT_MODES.index(st.session_state.output_mode))
    st.session_state.output_mode = output_mode

    # Display messages with optional audio for bot
    for message in st.session_state.messages:
        is_user = (message["role"] == "user")
        
        if is_user:
            render_message(message, is_user=True)
        else:
            # Always show text in chat bubble
            render_message(message, is_user=False)

            # If audio mode chosen, play TTS voice in selected language
            if st.session_state.output_mode == "Audio":
                try:
                    lang_code = get_language_code(st.session_state.selected_language)
                    tts = gTTS(text=message["content"], lang=lang_code, slow=False)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                        tts.save(fp.name)
                        st.audio(fp.name, format="audio/mp3")
                    os.unlink(fp.name)
                except Exception as e:
                    st.error(f"Audio generation failed: {e}")

    
    
    # Chat input
    if prompt := st.chat_input(f"Type your message here... ({st.session_state.selected_language})"):
        # Sanitize input
        sanitized_prompt = sanitize_input(prompt)
        
        if sanitized_prompt:
            # Add user message to chat
            st.session_state.messages.append({
                "role": "user",
                "content": sanitized_prompt,
                "timestamp": datetime.datetime.now()
            })
            
            # Send to Rasa and get response
            with st.spinner("Processing..."):
                rasa_response = send_message_to_rasa(sanitized_prompt, st.session_state.session_id)
            
            # Add bot responses to chat
            for response in rasa_response:
                if "text" in response:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["text"],
                        "timestamp": datetime.datetime.now()
                    })
            
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("**SecureBank Digital Assistant** | Powered by AI | 24/7 Support Available")

if __name__ == "__main__":
    main()