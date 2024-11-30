import streamlit as st
import websockets
import asyncio
import json
import os
from typing import List
from styles.shared import get_shared_css

# Page configuration
st.set_page_config(
    page_title="Chat - AI Chatbot", 
    page_icon="🤖", 
    layout="centered"
)

# Apply shared CSS
st.markdown(get_shared_css(), unsafe_allow_html=True)

BACKEND_URL = os.getenv('BACKEND_URL', 'ws://localhost:8000/ws')

def initialize_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'input' not in st.session_state:
        st.session_state.input = ""
    if 'should_clear' not in st.session_state:
        st.session_state.should_clear = False

def handle_message():
    message = st.session_state.input
    if message:
        st.session_state.messages.append({
            "sender": "Human",
            "message": message
        })
        st.session_state.messages.append({
            "sender": "Computer",
            "message": "Hello!"
        })
        st.session_state.should_clear = True
        st.session_state.input = ""

def main():
    st.markdown('<h1 class="sub-title">💬 Chat</h1>', unsafe_allow_html=True)
    
    initialize_state()
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["sender"] == "Human":
                st.markdown(f'''
                    <div class="message human-message">
                        👤 You: {message['message']}
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                    <div class="message bot-message">
                        🤖 PAI Agent: {message['message']}
                    </div>
                ''', unsafe_allow_html=True)
    
    # Input container
    with st.container():
        col1, col2 = st.columns([6, 1])
        
        with col1:
            value = "" if st.session_state.should_clear else st.session_state.input
            st.text_input(
                "Type your message here:",
                key="input",
                value=value,
                on_change=handle_message,
                label_visibility="collapsed"
            )
            if st.session_state.should_clear:
                st.session_state.should_clear = False
        
        with col2:
            st.button(
                "Send",
                use_container_width=True,
                on_click=handle_message
            )

if __name__ == "__main__":
    main()