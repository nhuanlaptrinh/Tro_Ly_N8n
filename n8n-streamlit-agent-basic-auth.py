import streamlit as st
import requests
import uuid

# Constants
WEBHOOK_URL = "https://n8n.srv792087.hstgr.cloud/webhook/e985d15f-b2f6-456d-be15-97e0b1544a40/chat"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjN2Y1MTU2My00YzdhLTRlZjgtYmIyMC1mNTAxZGI4ZDc3OWUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ2Mzc1ODQxLCJleHAiOjE3NDg5MDE2MDB9.985Iqo51r--sqd9jrvtbr_lOH5seRUIAN6QYXe73Ty8"

# Hàm đọc nội dung từ file văn bản
def rfile(name_file):
    #try:
    with open(name_file, "r", encoding="utf-8") as file:
        return file.read()
    #except FileNotFoundError:
    #    return "Chào mừng bạn đến với Trợ Lý AI!"  # Nội dung mặc định nếu file không tồn tại

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
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("output", "No output received")
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to the LLM - {str(e)}"

def main():
    # Hiển thị logo (nếu có)
    try:
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            st.image("logo.png", use_container_width=True)
    except:
        pass
    # Hiển thị tiêu đề
    title_content = rfile("00.xinchao.txt")
    print ("title_content",title_content)
    st.markdown(
        f"""<h1 style="text-align: center; font-size: 24px;">{title_content}</h1>""",
        unsafe_allow_html=True
    )

    # Khởi tạo session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()

    # CSS để căn chỉnh trợ lý bên trái, người hỏi bên phải, và thêm icon trợ lý
    st.markdown(
        """
        <style>
            .assistant {
                padding: 10px;
                border-radius: 10px;
                max-width: 75%;
                background: none; /* Màu trong suốt */
                text-align: left;
            }
            .user {
                padding: 10px;
                border-radius: 10px;
                max-width: 75%;
                background: none; /* Màu trong suốt */
                text-align: right;
                margin-left: auto;
            }
            .assistant::before { content: "🤖 "; font-weight: bold; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Hiển thị lịch sử tin nhắn
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.markdown(f'<div class="assistant">{message["content"]}</div>', unsafe_allow_html=True)
        elif message["role"] == "user":
            st.markdown(f'<div class="user">{message["content"]}</div>', unsafe_allow_html=True)

    # Ô nhập liệu cho người dùng
    if prompt := st.chat_input("Nhập nội dung cần trao đổi ở đây nhé?"):
        # Lưu tin nhắn người dùng
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(f'<div class="user">{prompt}</div>', unsafe_allow_html=True)

        # Gửi yêu cầu đến LLM và nhận phản hồi
        with st.spinner("Đang chờ phản hồi từ AI..."):
            llm_response = send_message_to_llm(st.session_state.session_id, prompt)

        # Hiển thị và lưu phản hồi của trợ lý
        st.markdown(f'<div class="assistant">{llm_response}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": llm_response})

if __name__ == "__main__":
    main()