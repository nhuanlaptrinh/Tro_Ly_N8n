import streamlit as st
import requests
import uuid

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjN2Y1MTU2My00YzdhLTRlZjgtYmIyMC1mNTAxZGI4ZDc3OWUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ2Mzc1ODQxLCJleHAiOjE3NDg5MDE2MDB9.985Iqo51r--sqd9jrvtbr_lOH5seRUIAN6QYXe73Ty8

# Constants
WEBHOOK_URL = "https://n8n.srv792087.hstgr.cloud/webhook/e985d15f-b2f6-456d-be15-97e0b1544a40/chat"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjN2Y1MTU2My00YzdhLTRlZjgtYmIyMC1mNTAxZGI4ZDc3OWUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ2Mzc1ODQxLCJleHAiOjE3NDg5MDE2MDB9.985Iqo51r--sqd9jrvtbr_lOH5seRUIAN6QYXe73Ty8"

def generate_session_id():
    return str(uuid.uuid4())

def send_message_to_llm(session_id, message):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "sessionId": session_id,
        "chatInput": message
    }
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["output"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    st.title("Chat Với Bạn Trợ Lý AI")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Get LLM response
        llm_response = send_message_to_llm(st.session_state.session_id, user_input)

        # Add LLM response to chat history
        st.session_state.messages.append({"role": "assistant", "content": llm_response})
        with st.chat_message("assistant"):
            st.write(llm_response)

if __name__ == "__main__":
    main()