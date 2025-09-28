from fastapi import APIRouter,Body
from agents.explainer_agent import explain_solution

router = APIRouter()

@router.post("/solve")
def explain_route(problem_description: str = Body(..., embed=True)):
    return explain_solution(problem_description)


