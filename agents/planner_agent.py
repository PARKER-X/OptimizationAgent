from agents.planner_agent import PLANNER_PROMPT_TEMPLATE
# agents/planner_agent.py

import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils.prompt_templates import PLANNER_PROMPT_TEMPLATE

# Load .env variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def plan_task(task_description: str, model_name: str = "models/gemini-pro") -> str:
    """
    Uses Gemini to generate a detailed OR solution plan based on task description.

    Args:
        task_description (str): Description of the OR problem.
        model_name (str): Gemini model name (default = "models/gemini-pro").

    Returns:
        str: A detailed, structured solution plan.
    """
    try:
        prompt = PLANNER_PROMPT_TEMPLATE.format(task=task_description)

        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error generating plan: {str(e)}"
