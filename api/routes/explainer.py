from fastapi import APIRouter
from agents.explainer_agent import explain_solution

router = APIRouter()

@router.post("/explain")
def explain_task(problem_input: dict):
    return explain_solution(problem_input)


