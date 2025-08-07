import streamlit as st
import requests


BASE_URL = "http://localhost:5000"
st.sidebar.header("🛠️ Survey Builder")

with st.sidebar.form("builder_form"):
    new_id = st.text_input("Survey ID", value="survey001")
    title = st.text_input("Survey Title", value="Demo Survey")
    
    default_qs = '[{"id": "q1", "text": "What is your age?", "type": "text"}, {"id": "q2", "text": "What is your job role?", "type": "text"}]'
    questions_raw = st.text_area("Questions (JSON format)", value=default_qs, height=200)
    
    build_btn = st.form_submit_button("🚀 Create Survey")

if build_btn:
    try:
        questions = eval(questions_raw)  # fast parse
        payload = {
            "id": new_id,
            "title": title,
            "questions": questions
        }
        res = requests.post(f"{BASE_URL}/api/create_survey", json=payload)
        st.sidebar.success("✅ Survey created!")
    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")

st.title("🧠 AI-Powered Smart Survey")

# Survey ID input
survey_id = st.text_input("Enter Survey ID to load:")

if survey_id:
    res = requests.get(f"{BASE_URL}/api/fetch_survey/{survey_id}")
    if res.status_code == 200:
        survey = res.json()
        st.subheader(survey.get("title", "Survey"))
        answers = {}

        for q in survey.get("questions", []):
            qid = q["id"]
            question_text = q["text"]
            qtype = q.get("type", "text")

            if qtype == "text":
                ans = st.text_input(question_text, key=qid)
            elif qtype == "radio":
                ans = st.radio(question_text, q.get("options", []), key=qid)
            elif qtype == "select":
                ans = st.selectbox(question_text, q.get("options", []), key=qid)
            else:
                ans = st.text_input(question_text, key=qid)

            answers[qid] = ans

            # Follow-up suggestion
            if ans:
                follow = requests.post(f"{BASE_URL}/api/suggest_follow_up", json={"answer": ans})
                follow_up = follow.json().get("follow_up")
                st.caption(f"🤖 AI Follow-up: {follow_up}")

        if st.button("Submit Survey"):
            payload = {
                "survey_id": survey_id,
                "answers": answers
            }
            submit = requests.post(f"{BASE_URL}/api/submit_response", json=payload)
            if submit.status_code == 200:
                st.success("✅ Response submitted!")
            else:
                st.error("Something went wrong.")
    else:
        st.error("Survey not found.")
