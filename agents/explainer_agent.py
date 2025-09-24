# agents/explainer_agent.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def explain_solution(raw_solution: str, plan: str = "", model_name: str = "models/gemini-2.5-flash") -> str:
    """
    Uses Gemini to explain a MILP solution in simple, beginner-friendly terms.

    Args:
        raw_solution (str): Raw output from the solver (variable values, objective value, status, etc.)
        plan (str): (Optional) MILP plan or formulation for added context
        model_name (str): Gemini model to use

    Returns:
        str: Simplified explanation of the MILP solution.
    """

    prompt = f"""
You are a helpful tutor in Operations Research.

Explain the following MILP solution clearly for a beginner. 
Highlight what the objective value means, the meaning of the decision variables,
and whether the constraints were satisfied.

Here is the problem formulation (if available):
{plan}

---

Here is the solution output from the solver:
{raw_solution}

---

Now explain what the result means in simple terms.
"""

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Explainer Agent failed: {str(e)}"
