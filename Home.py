import google.generativeai as genai
from mistune import markdown
import streamlit as st 
import textwrap
from IPython.display import Markdown
from streamlit_lottie import st_lottie
import requests 

st.set_page_config(page_title="Symptom Checker", page_icon="👨‍⚕️") 

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json

st.title(" :rainbow[Symptom Checker]")


# side bar
with st.sidebar:
    try:
        lottie_url = "https://lottie.host/ba10b921-fb9f-4423-96ff-56e4dce1e02d/X9Qm4rbbCM.json"
        lottie_data = requests.get(lottie_url).json()
        st_lottie(lottie_data, key="sidebar-animation", height=300, width=300)  

    except Exception as e:
        st.sidebar.error(f"Error loading animation: {e}")


# logic for chat bot
genai.configure(api_key="AIzaSyCk0JEdxBT56OHCN3xFNBUUCICtQ5tLC1s")
model = genai.GenerativeModel('gemini-1.0-pro')
 
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history = [])

if "messages" not in st.session_state:
    st.session_state.messages = []

initial_query = (
    "Act as a medical symptom checker chatbot. A user will describe their symptoms, "
    "and you will provide possible medical conditions that match those symptoms. "
    "Additionally, if the symptoms indicate a serious condition, suggest that the user see a doctor. "
    "Please respond with possible conditions and appropriate medical advice."
    "dont respond if user asks for any other contents other than medical related"
    "respond to only medical related queries"
    "also introduse yourself as Symptom checker AI"
    "Use simple language and try to be interactive",
)
st.session_state.chat.send_message(initial_query)
with st.chat_message("assistant",avatar="👨‍⚕️"):
    st.markdown("Welcome! I am a medical symptom checker bot. Describe your symptoms, and I will provide possible conditions and advice. For serious symptoms, I'll suggest seeing a doctor.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        response = st.session_state.chat.send_message(prompt)
        # Display last LLM response, first converting it to Markdown format
        with st.chat_message("assistant",avatar="👨‍⚕️"):   
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        with st.chat_message("assistant",avatar="👨‍⚕️"):   
            st.markdown("i can't help you with that")