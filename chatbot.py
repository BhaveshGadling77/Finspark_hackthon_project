import streamlit as st
import re
import json
import hashlib
import datetime
from typing import Dict, List, Optional, Tuple
import uuid
import requests
# import tts  # Removed because the 'tts' module could not be resolved
import TextToSpeech as ttss
# Page configuration
st.set_page_config(
    page_title="SecureBank ChatBot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    "Telugu": "👋 **సిక్యూర్‌బ్యాంక్‌కి స్వాగతం!**\n\nనేను మీ బ్యాంకింగ్ సేవలలో సహాయం చేయడానికి ఇక్కడ ఉన్నాను.",
    "Kannada": "👋 **ಸಿಕ್ಯೂರ್‌ಬ್ಯಾಂಕ್‌ಗೆ ಸುಸ್ವಾಗತ!**\n\nನಾನು ನಿಮ್ಮ ಬ್ಯಾಂಕಿಂಗ್ ಸೇವೆಗಳಲ್ಲಿ ಸಹಾಯ ಮಾಡಲು ಇಲ್ಲಿ ಇದ್ದೇನೆ."
}

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

# Security functions
def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    if not user_input:
        return ""
    sanitized = re.sub(r"[<>\"']", '', user_input)
    sanitized = re.sub(r'(javascript|script|eval|exec)', '', sanitized, flags=re.IGNORECASE)
    return sanitized.strip()[:500]

def generate_session_id() -> str:
    """Generate a unique session ID for tracking."""
    return str(uuid.uuid4())[:8]

def hash_account_number(account_num: str) -> str:
    """Hash account number for security display."""
    return hashlib.sha256(account_num.encode()).hexdigest()[:8]

# UI Components
def show_disclaimer():
    with st.expander("🔒 **Security & Privacy Notice** - Please Read Before Continuing", expanded=True):
        st.markdown("""
        **IMPORTANT SECURITY INFORMATION:**
        - This is a demonstration chatbot for educational purposes only.
        - Do NOT enter actual account numbers, passwords, or personal information.
        - All conversations are encrypted in this demo and cleared after session ends.
        """)

def render_message(message: Dict, is_user: bool = False):
    """Render a chat message with styling."""
    if is_user:
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.markdown(f"""
            <div style="background-color: #0066cc; color: white; padding: 10px 15px;
                        border-radius: 15px 15px 5px 15px; margin: 5px 0; text-align: left;">
                {message['content']}
                <div style="font-size: 0.7em; opacity: 0.8; margin-top: 5px;">{message['timestamp']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            st.markdown("🏦", help="SecureBank Assistant")
        with col2:
            st.markdown(f"""
            <div style="background-color: #f0f2f6; color: #262730; padding: 10px 15px;
                        border-radius: 15px 15px 15px 5px; margin: 5px 0;
                        border-left: 4px solid #0066cc;">
                {message['content']}
                <div style="font-size: 0.7em; opacity: 0.6; margin-top: 5px;">{message['timestamp']}</div>
            </div>
            """, unsafe_allow_html=True)

def authenticate_demo_account():
    st.sidebar.markdown("### 🔐 Demo Authentication")
    account_options = {
        "Select Account": None,
        "12345678 - John Smith (Savings)": "12345678",
        "87654321 - Sarah Johnson (Checking)": "87654321"
    }
    selected_account = st.sidebar.selectbox("Choose Demo Account:", list(account_options.keys()))
    if st.sidebar.button("🔓 Authenticate"):
        if account_options[selected_account]:
            st.session_state.authenticated_account = account_options[selected_account]
            st.session_state.session_id = generate_session_id()
            st.sidebar.success(f"✅ Authenticated as {selected_account.split(' - ')[1]}")
            st.rerun()
        else:
            st.sidebar.error("Please select an account")
    if 'authenticated_account' in st.session_state:
        account_num = st.session_state.authenticated_account
        masked = f"****{account_num[-4:]}"
        st.sidebar.info(f"Logged in: Account {masked}")
        if st.sidebar.button("🔒 Logout"):
            for key in ['authenticated_account', 'session_id']:
                if key in st.session_state: del st.session_state[key]
            st.rerun()

# NEW: Rasa API call
def send_to_rasa(user_message: str, language: str = "English") -> List[str]:
    """Send the message to Rasa REST API and return list of bot replies."""
    session_id = st.session_state.get('session_id', generate_session_id())
    st.session_state.session_id = session_id
    try:
        # Get language code
        language_code = get_language_code(language)
        
        # Create payload with language information
        payload = {
            "sender": session_id, 
            "message": user_message,
            "metadata": {
                "language": language_code,
                "language_name": language
            }
        }
        
        resp = requests.post(
            "http://0.0.0.0:5005/webhooks/rest/webhook",
            json=payload, timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            replies = [m.get("text", "") for m in data if m.get("text")]
            return replies
        else:
            return ["❌ Error: Unable to connect to Rasa server."]
    except requests.RequestException as e:
        return [f"❌ Connection error: {e}"]

def send_message():
    """Send message and get response from Rasa."""
    if 'user_input' not in st.session_state or not st.session_state.user_input.strip():
        return
    
    user_message = sanitize_input(st.session_state.user_input.strip())
    if not user_message:
        st.error("Invalid input. Please enter a valid message.")
        return
    
    # Get selected language (default to English if not set)
    selected_language = st.session_state.get('selected_language', get_default_language())
    
    st.session_state.messages.append({
        'content': user_message,
        'timestamp': datetime.datetime.now().strftime('%I:%M %p'),
        'is_user': True
    })
    
    # Get Rasa responses with language information
    replies = send_to_rasa(user_message, selected_language)
    for reply in replies:

        st.session_state.messages.append({
            'content': reply,
            'timestamp': datetime.datetime.now().strftime('%I:%M %p'),
            'is_user': False
        })
    print(replies)
    ttss.some(str(replies))
    # tts.some(replies)  # Removed because the 'tts' module could not be resolved
    # Clear the text field by setting user_input to empty string
    st.session_state.user_input = ""

def handle_language_change(new_language: str):
    """Handle language change and update welcome message if needed."""
    if 'messages' in st.session_state and st.session_state.messages:
        # Update the first message (welcome message) if it exists
        if len(st.session_state.messages) == 1 and not st.session_state.messages[0].get('is_user', False):
            st.session_state.messages[0]['content'] = get_welcome_message(new_language)
            st.session_state.messages[0]['timestamp'] = datetime.datetime.now().strftime('%I:%M %p')

# Main App
def main():
    # CSS
    st.markdown("""
    <style>
        .main-header { background: linear-gradient(90deg, #0066cc 0%, #004499 100%);
                       padding: 1rem 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem; }
        .chat-container { max-height: 60vh; overflow-y: auto; padding: 10px; background-color: #fafafa;
                          border-radius: 10px; margin-bottom: 1rem; }
        .language-selector { background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

    # Initialize language selection
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = get_default_language()

    # Header
    current_language = st.session_state.selected_language
    language_flag = get_language_flag(current_language)
    st.markdown(f'''
    <div class="main-header">
        <h1>🏦 SecureBank Digital Assistant</h1>
        <p>Your trusted banking companion - Available 24/7</p>
        <p style="font-size: 0.9em; opacity: 0.8;">{language_flag} Currently in {current_language}</p>
    </div>
    ''', unsafe_allow_html=True)
    show_disclaimer()

    # Init chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = [{
            'content': get_welcome_message(st.session_state.selected_language),
            'timestamp': datetime.datetime.now().strftime('%I:%M %p'),
            'is_user': False
        }]

    # Sidebar authentication and language selection
    authenticate_demo_account()
    
    # Language selection in sidebar
    st.sidebar.markdown("### 🌐 Language Selection")
    language_options = list(LANGUAGES.keys())
    selected_language = st.sidebar.selectbox(
        "Choose Language:",
        language_options,
        index=language_options.index(st.session_state.selected_language),
        format_func=lambda x: f"{get_language_flag(x)} {x}"
    )
    
    # Update session state if language changed
    if selected_language != st.session_state.selected_language:
        st.session_state.selected_language = selected_language
        st.sidebar.success(f"✅ Language changed to {selected_language}")
        handle_language_change(selected_language) # Call the new function

    # Display messages
    chat_container = st.container()
    with chat_container:
        for m in st.session_state.messages:
            render_message(m, m['is_user'])

    # Input field with language indicator and send button
    st.markdown(f"<div class='language-selector' style='color:black'><strong>🌐 Current Language:</strong> {get_language_flag(st.session_state.selected_language)} {st.session_state.selected_language}</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        st.text_input(
            "Type your message...",
            key="user_input",
            placeholder=f"Ask me about your account, transfers, or services... (in {st.session_state.selected_language})",
            label_visibility="collapsed",
            on_change=send_message
        )
    with col2:
        if st.button("Send 📤", use_container_width=True):
            send_message()
            st.rerun()
    with col3:
        # Show current language flag
        st.markdown(f"<div style='text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 5px;'>{get_language_flag(st.session_state.selected_language)}</div>", unsafe_allow_html=True)

    # Auto-scroll (move to bottom)
    st.markdown("""
        <script>
        var chatDiv = window.parent.document.querySelector('.chat-container');
        if (chatDiv) { chatDiv.scrollTop = chatDiv.scrollHeight; }
        </script>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown('<div style="text-align: center; color: #666; font-size: 0.9em;">🏦 SecureBank Digital Assistant | Secure • Reliable • Available 24/7</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
