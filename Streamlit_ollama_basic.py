#from openai import OpenAI
import ollama
import streamlit as st

st.title("ChatGPT-like clone")


model='llama3.2:latest'

  
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = ollama.chat(
            model=model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            #stream=True,
        )

        response = st.write(stream["message"]["content"])
    st.session_state.messages.append({"role": "assistant", "content": stream["message"]["content"]})