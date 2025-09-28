from fastapi import APIRouter,Body
from agents.solver_agent import solve_task, get_last_generated_code 
router = APIRouter()

@router.post("/solve")
def solve(problem_description: str = Body(..., embed=True)):
    return {"output": solve_task(problem_description)}

@router.get("/code")
def get_code():
    return {"code": get_last_generated_code()}