import streamlit as st
from llm import generate_sql_and_explanation
from db import run_query
from utils import clean_sql, parse_llm_output

@st.cache_data
def cached_query(sql):
    return run_query(sql)

st.set_page_config(page_title="LLM SQL Assistant", layout="wide")

st.title("📊 LLM SQL Assistant")
st.write("Ask questions about Campaign & Sales data")

# Initialize memory
if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_input("Enter your question")

if st.button("Run Query") and question:

    # Step 1: Single LLM call (SQL + Explanation)
    llm_output = generate_sql_and_explanation(
        question, st.session_state.history
    )

    # Step 2: Extract SQL + Explanation
    raw_sql, explanation = parse_llm_output(llm_output)
    sql_query = clean_sql(raw_sql)

    # Step 3: Run query
    result = cached_query(sql_query)

    # Step 4: Handle result
    if isinstance(result, str):
        st.error(f"SQL Error: {result}")
    else:
        # Save memory
        st.session_state.history.append({
            "question": question,
            "answer": explanation
        })

        # Display outputs
        st.subheader("Generated SQL")
        st.code(sql_query, language="sql")

        st.subheader("Query Result")
        st.dataframe(result)

        st.subheader("Insight")
        st.success(explanation)

#         st.subheader("Raw LLM Output")
#         st.text(llm_output)

# # Show conversation history
# if st.session_state.history:
#     st.subheader("Conversation History")
#     for chat in st.session_state.history:
#         st.write(f"**Q:** {chat['question']}")
#         st.write(f"**A:** {chat['answer']}")

if not sql_query.strip():
    st.error("No SQL query generated. Try rephrasing your question.")
    st.stop()