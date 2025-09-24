# agents/solver_agent.py

import os
import io
import contextlib
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Global variable to store last generated code (useful for UI)
_last_generated_code = ""

def clean_code(generated_code: str) -> str:
    """
    Cleans Gemini-generated code by removing markdown syntax or code fences.

    Args:
        generated_code (str): The raw code returned from Gemini.

    Returns:
        str: Cleaned Python code, ready for execution.
    """
    if generated_code.startswith("```"):
        lines = generated_code.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines)
    return generated_code


def generate_milp_code(task_description: str, model_name: str = "models/gemini-2.5-flash") -> str:
    """
    Uses Gemini to generate Python PuLP code for the given MILP problem.

    Args:
        task_description (str): Natural language description of MILP problem.
        model_name (str): Gemini model name to use.

    Returns:
        str: Clean, runnable Python code using PuLP to solve the MILP.
    """
    global _last_generated_code

    prompt = f"""
You are an expert in Mixed Integer Linear Programming (MILP) and Python programming.

Given the following problem description, write a complete runnable Python script that uses PuLP
to model and solve the MILP. Your code must:

- Import PuLP
- Define decision variables (continuous or integer as appropriate)
- Define the objective function to maximize or minimize
- Add all constraints
- Solve the problem using PuLP's solver
- Print the status, objective value, and decision variable values clearly

Problem description:
{task_description}

ONLY return runnable Python code. Do NOT include explanations, markdown, or text.
"""

    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    cleaned_code = clean_code(response.text)
    _last_generated_code = cleaned_code  # store for UI access
    return cleaned_code


def get_last_generated_code() -> str:
    """
    Returns the last generated code snippet from Gemini.

    Returns:
        str: Last cleaned Python MILP code.
    """
    return _last_generated_code


def execute_code(code: str) -> str:
    """
    Executes the given Python code safely and captures stdout.

    Args:
        code (str): Python code to execute.

    Returns:
        str: Output or error message.
    """
    print("===== Generated Code Start =====")
    print(code)
    print("===== Generated Code End =====")

    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec_globals = {}
            exec(code, exec_globals)
    except Exception as e:
        return f"⚠️ Error during execution: {str(e)}"
    return output.getvalue()


def solve_task(task_description: str) -> str:
    """
    Full pipeline: Generate code from task, execute, and return output.

    Args:
        task_description (str): MILP problem in natural language.

    Returns:
        str: Solver output or error message.
    """
    try:
        code = generate_milp_code(task_description)
        solution = execute_code(code)
        return solution
    except Exception as e:
        return f"Solver Agent Error: {str(e)}"


# if __name__ == "__main__":
#     # Example MILP problem
#     example_task = """
# Maximize profit: 3x + 5y
# Subject to:
# 4x + 3y <= 240
# 2x + 5y <= 100
# x >= 0 and integer
# y >= 0 and integer
# """
#     print(solve_task(example_task))
