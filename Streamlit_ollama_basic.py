import ollama
import streamlit as st


def response_generator(msg_content):
    lines = msg_content.split('\n')  # Split the content into lines to preserve paragraph breaks.
    for line in lines:
        words = line.split()  # Split the line into words to introduce a delay for each word.
        for word in words:
            yield word + " "
            time.sleep(0.1)
        yield "\n"  # After finishing a line, yield a newline character to preserve paragraph breaks.

def show_msgs():
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write(msg["content"])
        else:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

def chat(message, model='llama3'): ### CHANGE MODEL ID HERE 
    try:
        response = ollama.chat(model=model, messages=[
            {
                'role': 'user',
                'content': message,
            }
        ])
        return response['message']['content']
    except Exception as e:
        error_message = str(e).lower()
        if "not found" in error_message:
            return f"Model '{model}' not found. Please refer to Doumentation at https://ollama.com/library."
        else:
            return f"An unexpected error occurred with model '{model}': {str(e)}"
        


def main():
    st.title("Simple Ollama Chat Interface by Mavi")
    user_input = st.chat_input("Enter your prompt:", key="1")
    
    if 'show' not in st.session_state:
        st.session_state['show'] = 'True'
    if 'show_chats' not in st.session_state:
        st.session_state['show_chats'] = 'False'
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    show_msgs()
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        messages = "\n".join(msg["content"] for msg in st.session_state.messages)
        # print(messages)
        response = chat(messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write_stream(response_generator(response))
    elif st.session_state['messages'] is None:
        st.info("Enter a prompt or load chat above to start the conversation")

    

if __name__ == "__main__":
    main()


