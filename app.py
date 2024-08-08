import time
import openai
import streamlit as st

# OpenAI 클라이언트 설정
openai_client = openai

# 상수 정의
ASSISTANT_ID = "asst_XXXXXXXXXXXXXXXXXXXX"
OPENAI_API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
PAGE_TITLE = "<페이지 제목을 입력해주세요>"
PAGE_DESCRIPTION = "<페이지 설명을 입력해주세요>"

def setup_page():
    """Streamlit 페이지 설정 함수"""
    st.set_page_config(page_title=PAGE_TITLE, page_icon=":speech_balloon:")
    st.title(PAGE_TITLE)
    st.write(PAGE_DESCRIPTION)

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

def initialize_session_state():
    """세션 상태를 초기화하는 함수"""
    if "thread_id" not in st.session_state:
        thread = openai_client.beta.threads.create()
        st.session_state.thread_id = thread.id
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    """채팅 기록을 표시하는 함수"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def get_user_input():
    """사용자 입력을 받는 함수"""
    return st.chat_input("채팅을 입력해주세요.")

def add_user_message(prompt):
    """사용자 메시지를 추가하고 표시하는 함수"""
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

def send_message_to_thread(prompt):
    """OpenAI 스레드에 메시지를 보내는 함수"""
    openai_client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=prompt
    )

def create_assistant_run():
    """OpenAI 어시스턴트 실행을 생성하는 함수"""
    return openai_client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=ASSISTANT_ID,
        stream=True
    )

def process_stream(stream):
    """스트림을 처리하고 메시지를 표시하는 함수"""
    placeholder = st.empty()
    full_response = ""
    for chunk in stream:
        if chunk.event == "thread.message.delta":
            if hasattr(chunk.data, 'delta') and hasattr(chunk.data.delta, 'content'):
                content_delta = chunk.data.delta.content[0].text.value
                full_response += content_delta
                placeholder.markdown(full_response + "▌")
    placeholder.markdown(full_response)
    return full_response

def main():
    """메인 함수"""
    initialize_session_state()
    setup_page()
    display_chat_history()
    
    if prompt := get_user_input():
        add_user_message(prompt)
        send_message_to_thread(prompt)
        
        with st.chat_message("assistant"):
            stream = create_assistant_run()
            full_response = process_stream(stream)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
