import streamlit as st
from styles.shared import get_shared_css

# Page configuration
st.set_page_config(
    page_title="AI Chatbot", 
    page_icon="🤖", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Apply shared CSS
st.markdown(get_shared_css(), unsafe_allow_html=True)

def main():
    # Main title
    st.markdown('<h1 class="main-title">🤖 FastPAI</h1>', unsafe_allow_html=True)

    # Description
    st.markdown('''
    <p class="description">
    Il tuo assistente personale per interagire con la pubblica amministrazione
    </p>
    ''', unsafe_allow_html=True)

    # Features section
    st.markdown('''
    <div class="feature-section">
        <div class="feature">
            <h3>Scegli un servizio</h3>
            <p>Specifica il servizio che devi svolgere presso la PA</p>
        </div>
        <div class="feature">
            <h3>Cosa ti serve</h3>
            <p>Scopri la lista di documenti necessari </p>
        </div>
        <div class="feature">
            <h3>Prenota</h3>
            <p>Ottieni direttamente un appuntamento </p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Start chat button
    st.markdown('''
    <div style="text-align: center; margin-top: 30px;">
        <a href="Chat" target="_self">
            <button class="custom-btn">Inizia Chat</button>
        </a>
    </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()