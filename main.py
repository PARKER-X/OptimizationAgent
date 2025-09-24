# app.py

import streamlit as st
from agents.planner_agent import plan_task
from agents.solver_agent import solve_task, get_last_generated_code  # optional: expose code
from agents.explainer_agent import explain_solution
# from agents.retrieval_agent import retrieve_context  # If using RAG

st.set_page_config(page_title="Agentic MILP Assistant", layout="wide")
st.title("🧠 Agentic MILP Solver Assistant")

# 1. Input
user_input = st.text_area("📥 Enter your MILP problem description here:", height=200)

if st.button("🚀 Run MILP Solver"):
    if not user_input.strip():
        st.warning("Please enter a MILP problem description.")
    else:
        with st.spinner("Running agentic pipeline..."):

            # Optional: retrieve context from documents
            # context = retrieve_context(user_input)

            # 2. Planner Agent
            st.subheader("🧩 Planner Agent Output")
            plan = plan_task(user_input)  # or plan_task(user_input, context=context)
            st.code(plan, language="markdown")

            # 3. Solver Agent
            st.subheader("🛠️ Solver Agent Output")
            solution = solve_task(plan)
            st.code(solution)

            # 4. Show Generated Code (optional)
            with st.expander("🧾 View Generated Solver Code"):
                code = get_last_generated_code()  # pull from global if implemented
                st.code(code, language="python")

            # 5. Explainer Agent
            st.subheader("📖 Explainer Agent Output")
            explanation = explain_solution(plan, solution)
            st.markdown(explanation)
