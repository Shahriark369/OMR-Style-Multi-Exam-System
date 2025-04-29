import streamlit as st
import json

st.title("Answer Formatter to JSON")

st.write("### Paste your answers below (e.g., abcdabcd...)")

# User input
answer_string = st.text_area("Enter answer string:")

if st.button("Convert to JSON"):
    if not answer_string.strip():
        st.warning("Please enter an answer string.")
    else:
        # Clean and convert input to uppercase
        answer_string = answer_string.strip().replace(" ", "").lower().upper()

        # Create JSON dictionary
        answer_json = {str(i + 1): ans for i, ans in enumerate(answer_string)}

        # Show result as plain text
        st.write("### Output JSON:")
        st.code(json.dumps(answer_json, indent=2, ensure_ascii=False), language='json')
