import streamlit as st
import json

# Load correct answers
with open("answers.json", "r") as f:
    all_answers = json.load(f)

st.title("📝 OMR-Style Multi-Exam System")

# Choose an exam
exam_list = list(all_answers.keys())
selected_exam = st.selectbox("Select Exam", exam_list)

correct_answers = all_answers[selected_exam]
total_questions = len(correct_answers)
submitted_key = f"submitted_{selected_exam}"

# Check if this exam has been submitted before
submitted = st.session_state.get(submitted_key, False)

# User answers dictionary
user_answers = {}

# Render OMR form
st.header(f"🧾 {selected_exam.replace('_', ' ').title()}")

for i in range(1, total_questions + 1):
    q_str = str(i)
    q_key = f"{selected_exam}_Q{q_str}"

    # Ensure initial value
    if q_key not in st.session_state:
        st.session_state[q_key] = None

    if not submitted:
        # Radio buttons for options
        choice = st.radio(
            label=f"Question {q_str}",
            options=["A", "B", "C", "D"],
            key=q_key,
            horizontal=True
        )
    else:
        user_choice = st.session_state[q_key]
        correct = correct_answers[q_str]
        result_icon = "✅" if user_choice == correct else "❌"
        st.markdown(
            f"**Question {q_str}**: You selected **{user_choice}**, correct answer is **{correct}** {result_icon}"
        )

    user_answers[q_str] = st.session_state[q_key]

# Submit button
if not submitted:
    if st.button("Submit"):
        st.session_state[submitted_key] = True

        # Score calculation
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
