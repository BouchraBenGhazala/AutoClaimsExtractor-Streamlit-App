import streamlit as st
from functions_chatbot_gemini import *

st.set_page_config(layout="wide", page_title="Chatbot", page_icon="🤖")

st.markdown("<h2 style='color:#077d81;'>Insurance Contract Q&A</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# Chatbot 🤖")
    st.markdown("This app uses **AI to answer questions about your insurance contract**.")
    load_demo = st.button("Load demo example")


user_avatar = "🧑"
assistant_avatar = "🤖"
contract_avatar = "📄"

if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_message = "Bonjour! Comment puis-je vous aider aujourd'hui?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_message, "avatar": assistant_avatar})


for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

if load_demo:
    example_query = "Quelle est la franchise pour la couverture 'Dommage Collision' indiquée sur le contrat d'assurance ?"
else:
    example_query = ""

query = st.chat_input("Write your question here")
if query:
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query, "avatar": user_avatar})
    
    with st.chat_message("assistant", avatar=assistant_avatar):
        response_placeholder = st.empty()
        with st.spinner(""):
            answer = answer_this(query)
        response = response_placeholder.write_stream(response_generator(answer))
        response_placeholder.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": assistant_avatar})

js = f"""
    <script>
        function insertText(dummy_var_to_force_repeat_execution) {{
            var chatInput = parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
            nativeInputValueSetter.call(chatInput, "{example_query}");
            var event = new Event('input', {{ bubbles: true}});
            chatInput.dispatchEvent(event);
        }}
        insertText({len(st.session_state.messages)});
    </script>
    """
st.components.v1.html(js)

