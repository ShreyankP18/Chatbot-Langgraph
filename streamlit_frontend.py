import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import re

CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    prompt = (
        "Give a medium range length with  all points covered answer  "
        "No markdown, no brackets, no formatting, no lists. "
        
    )

    response = chatbot.invoke(
        {
            'messages': [
                HumanMessage(content=f"{prompt}\n\nUser: {user_input}")
            ]
        },
        config=CONFIG
    )

    ai_message = response['messages'][-1].content.strip()
    ai_message = re.sub(r'[\[\]\']', '', ai_message)

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)
