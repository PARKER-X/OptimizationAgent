from fastapi import APIRouter,Body
from agents.planner_agent import plan_task

router = APIRouter()

@router.post("/plan")
def plan_route(problem_description: str = Body(..., embed=True)):
    return plan_task(problem_description)
