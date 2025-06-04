import streamlit as st
import pytz
import re
import os
from dotenv import load_dotenv
from datetime import datetime
from mistralai import Mistral

# Mistral AI API 클라이언트 설정
load_dotenv()
Mistral_api_key = os.environ.get('Mistral_api_key')

client = Mistral(
    api_key = Mistral_api_key
)

# 현재 시간
timezone = pytz.timezone('Asia/Seoul')
current_datetime = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S %A')


# 메인 LLM 호출 함수
def chat_with_llm(user_input, additional_info=None):
    # 기본 시스템 메시지 구성
    base_system_content = (
        f"Here is the current time: {current_datetime}\n "
        f"{Perosona}\n"
        f"{Response_Instruction}\n"
    )
    
    # 추가 정보가 있는 경우 system_content에 추가
    if additional_info:
        base_system_content += f"\n\n 추가 정보 제공:\n{additional_info}"

    # API 호출
    response = client.chat.complete(
        model="open-mistral-nemo",
        messages=[
            {"role": "system", "content": base_system_content},  # 시스템 메시지
            {"role": "user", "content": user_input}  # 사용자 입력
        ],
        max_tokens=500
    )

    # 응답에서 텍스트 추출
    reply_text = response.choices[0].message.content

    return reply_text

def main():
    st.set_page_config(page_title="프리스토시스 one")
    st.title("프리스토시스 One")
    st.write("금융 관련 질문을 입력하세요. 주가, 환율, 가상화폐, 금리 정보 등을 제공합니다.")

    # 대화 기록 초기화
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # 기존 대화 기록 출력
    for message in st.session_state.conversation_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리
    if user_input := st.chat_input("질문을 입력하세요:"):
        # 사용자 메시지 출력
        st.chat_message("user").markdown(user_input)
        
        # 대화 기록에 사용자 입력 추가
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        
        # process_input 함수 호출
        response = process_input(user_input)
        
        # 대화 기록을 문자열로 변환
        additional_info = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.conversation_history])
        
        # 플레이스홀더 생성
        response_placeholder = st.empty()
        
        # 플레이스홀더 내에 assistant 메시지 컨테이너 생성
        with response_placeholder.container():
            with st.chat_message("assistant"):
                with st.spinner('잠시만 기다려 주세요...'):
                    # Get AI response
                    final_response = chat_with_llm(response, additional_info)
                    st.markdown(final_response)

        # 대화 기록에 AI 응답 추가
        st.session_state.conversation_history.append({"role": "assistant", "content": final_response})

if __name__ == "__main__":
    main()
