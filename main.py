import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="AI Chatbot", 
    page_icon="🤖", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Funzione per applicare il CSS personalizzato
def add_custom_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
        font-family: 'Arial', sans-serif;
    }
    .main-title {
        font-size: 3rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 20px;
    }
    .description {
        font-size: 1.2rem;
        color: #34495e;
        text-align: center;
        max-width: 700px;
        margin: 0 auto 30px;
        line-height: 1.6;
    }
    .feature-section {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        justify-items: center;
        align-items: start;
        text-align: center;
        margin: 30px 0;
    }
    .feature {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        display: grid;
        grid-template-rows: auto auto;
        align-items: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        min-height: 200px;
        width: 100%;
        max-width: 260px;
    }
    .feature:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 10px rgba(0,0,0,0.15);
    }
    .feature h3 {
        color: #2980b9;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 5px;
        text-align: center;
        width: 100%;
    }
    .feature p {
        color: #7f8c8d;
        font-size: 0.95rem;
        line-height: 1.4;
        text-align: center;
        margin: 0;
    }
    .start-btn-container {
        text-align: center;
        margin-top: 30px;
    }
    .start-btn {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 15px 30px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .start-btn:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

# Funzione per creare la landing page
def landing_page():
    # Applica il CSS personalizzato
    add_custom_css()

    # Titolo principale
    st.markdown('<h1 class="main-title">🤖 FastPAI</h1>', unsafe_allow_html=True)

    # Descrizione
    st.markdown('''
    <p class="description">
    Il tuo assistente personale per interagire con la pubblica amministrazione
    </p>
    ''', unsafe_allow_html=True)

    # Sezione delle funzionalità
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

    # Bottone per iniziare la chat
    st.markdown('''
    <div class="start-btn-container">
        <form action="chat">
            <button class="start-btn" type="submit">Inizia Chat</button>
        </form>
    </div>
    ''', unsafe_allow_html=True)

# Main
if __name__ == "__main__":
    landing_page()