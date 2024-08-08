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
    )

def wait_for_run_completion(run):
    """실행 완료를 기다리는 함수"""
    while run.status != 'completed':
        time.sleep(1)
        run = openai_client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id,
            run_id=run.id
        )
    return run

def get_assistant_messages(run):
    """어시스턴트 메시지를 가져오는 함수"""
    messages = openai_client.beta.threads.messages.list(
        thread_id=st.session_state.thread_id
    )
    return [
        message for message in messages
        if message.run_id == run.id and message.role == "assistant"
    ]

def display_assistant_messages(assistant_messages):
    """어시스턴트 메시지를 표시하는 함수"""
    for message in assistant_messages:
        content = message.content[0].text.value
        st.session_state.messages.append({"role": "assistant", "content": content})
        with st.chat_message("assistant"):
            st.markdown(content)

def main():
    """메인 함수"""
    initialize_session_state()
    setup_page()
    display_chat_history()

    if prompt := get_user_input():
        add_user_message(prompt)
        send_message_to_thread(prompt)
        
        run = create_assistant_run()
        run = wait_for_run_completion(run)
        
        assistant_messages = get_assistant_messages(run)
        display_assistant_messages(assistant_messages)

if __name__ == "__main__":
    main()