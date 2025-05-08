import streamlit as st
import json

st.set_page_config(
    page_title="OMR-Style Multi-Exam System",
    page_icon="📝", 
    layout="centered",
)

# Load correct answers
with open("answers.json", "r") as f:
    all_answers = json.load(f)

# Custom CSS for option boxes
st.markdown("""
    <style>
    .option-box {
        border: 2px solid #ccc;
        border-radius: 8px;
        padding: 12px;
        margin: 5px;
        text-align: center;
        font-size: 16px;
        transition: 0.3s;
        cursor: pointer;
    }
    .option-box:hover {
        background-color: #f0f0f0;
        border-color: #4CAF50;
    }
    .selected {
        background-color: #e6ffe6;
        border-color: #4CAF50;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📝 OMR-Style Multi-Exam System")

exam_list = list(all_answers.keys())
selected_exam = st.selectbox("Select Exam", exam_list)

correct_answers = all_answers[selected_exam]
total_questions = len(correct_answers)
submitted_key = f"submitted_{selected_exam}"
submitted = st.session_state.get(submitted_key, False)

user_answers = {}

st.header(f"🧾 {selected_exam.replace('_', ' ').title()}")

# Render each question
for i in range(1, total_questions + 1):
    q_str = str(i)
    q_key = f"{selected_exam}_Q{q_str}"

    if q_key not in st.session_state:
        st.session_state[q_key] = None

    user_answers[q_str] = st.session_state[q_key]

    st.markdown(f"**Question {q_str}**")

    if not submitted:
        cols = st.columns(4)
        options = ["A", "B", "C", "D"]

        for idx, opt in enumerate(options):
            is_selected = st.session_state[q_key] == opt
            box_class = "option-box selected" if is_selected else "option-box"

            if cols[idx].button(f"{opt}", key=f"{q_key}_{opt}"):
                st.session_state[q_key] = opt

            # Show styled box
            cols[idx].markdown(f"<div class='{box_class}'>{opt}</div>", unsafe_allow_html=True)
    else:
        user_choice = st.session_state[q_key]
        correct = correct_answers[q_str]
        result_icon = "✅" if user_choice == correct else "❌"
        st.markdown(
            f"**Question {q_str}**: You selected **{user_choice}**, correct answer is **{correct}** {result_icon}"
        )

# Submit logic
if not submitted:
    if st.button("Submit"):
        st.session_state[submitted_key] = True
        score = 0
        wrong = []

        for qno, user_ans in user_answers.items():
            if user_ans is not None:
                if user_ans == correct_answers[qno]:
                    score += 1
                else:
                    wrong.append(qno)
            else:
                wrong.append(qno)

        st.success(f"🎯 You got {score} out of {total_questions} correct.")
        if wrong:
            st.error("📛 Incorrect or Unanswered Questions:")
            st.write(", ".join(wrong))
else:
    st.info("✅ You have already submitted this exam. Refresh the page to try again.")
