# GPTs to Streamlit-UI

나만의 GPTs를 Streamlit Chat-UI로 만드는 가장 간단한 방법입니다.

1. OpenAI Playground에서 새로운 Assistants API를 만듭니다. (GPTs를 만드는 과정과 동일함)

링크: https://platform.openai.com/playground/assistants


2. 아래 Assistant ID, OpenAI API key, 페이지 제목, 페이지 설명을 적어줍니다.
```
ASSISTANT_ID = "asst_XXXXXXXXXXXXXXXXXXXX"
OPENAI_API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
PAGE_TITLE = "<페이지 제목을 입력해주세요>"
PAGE_DESCRIPTION = "<페이지 설명을 입력해주세요>"
```

3. 필요한 라이브러리를 설치해줍니다.
```
pip install -r requirements.txt
```

4. streamlit 파일을 실행해줍니다.
```
streamlit run app.py
```
