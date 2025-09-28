from fastapi import FastAPI
from api.routes import planner, explainer, solver

app = FastAPI()


app.include_router(planner.router, prefix="/planner")
app.include_router(solver.router, prefix="/solver")
app.include_router(explainer.router, prefix="/explainer")