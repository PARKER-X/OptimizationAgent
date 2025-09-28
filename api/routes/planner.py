from fastapi import APIRouter
from agents.planner_agent import plan_task

router = APIRouter()

@router.post("/plan")
def plan_task(problem_input: dict):
    return plan_task(problem_input)
