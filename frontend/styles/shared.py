def get_shared_css():
    return """
    <style>
    /* Base styles */
    .stApp {
        background-color: #ffffff;
        font-family: 'Arial', sans-serif;
    }

    /* Titles */
    .main-title {
        font-size: 3rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 20px;
    }

    .sub-title {
        font-size: 2rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 15px;
    }

    /* Description text */
    .description {
        font-size: 1.2rem;
        color: #34495e;
        text-align: center;
        max-width: 700px;
        margin: 0 auto 30px;
        line-height: 1.6;
    }

    /* Features section */
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
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        display: grid;
        grid-template-rows: auto auto;
        align-items: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        min-height: 200px;
        width: 100%;
        max-width: 260px;
        border: 1px solid #e0e0e0;
    }

    .feature:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }

    .feature h3 {
        color: #2c3e50;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 5px;
        text-align: center;
        width: 100%;
    }

    .feature p {
        color: #666666;
        font-size: 0.95rem;
        line-height: 1.5;
        text-align: center;
        margin: 0;
    }

    /* Buttons */
    .custom-btn {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 12px 28px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .custom-btn:hover {
        background-color: #45a049;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.2);
    }

    /* Chat specific styles */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }

    .message {
        padding: 12px 18px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 80%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        font-size: 1rem;
        line-height: 1.5;
    }

    .human-message {
        background-color: #E8F5E9;
        color: #2c3e50;
        margin-left: auto;
        text-align: right;
        border-bottom-right-radius: 5px;
    }

    .bot-message {
        background-color: #f8f9fa;
        color: #2c3e50;
        margin-right: auto;
        border-bottom-left-radius: 5px;
        border: 1px solid #f0f0f0;
    }

    /* Input area */
    .input-area {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 20px;
        background-color: #ffffff;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }

    .stTextInput input {
        height: 45px;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0 15px;
        font-size: 1rem;
        transition: all 0.3s ease;
        background-color: #ffffff;
        color: #2c3e50;
    }

    .stTextInput input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
        outline: none;
    }

    .stTextInput input::placeholder {
        color: #999999;
    }

    div.stButton > button {
        height: 45px;
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 0 20px;
    }

    div.stButton > button:hover {
        background-color: #45a049;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.2);
    }

    /* Block container */
    .block-container {
        max-width: 1000px;
        padding-top: 2rem;
    }

    /* Emoji in messages */
    .human-message span, .bot-message span {
        margin-right: 8px;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """ 