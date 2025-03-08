from pydantic import BaseModel


class PlannerOutput(BaseModel):
    plan: str


class PlannerInput(BaseModel):
    prompt: str


# Critic Agent
planner_prompt = """
You are a professional planning agent. Your job is to take a coding task and write a detailed plan so that a
generator model can generate code based on your instructions.
"""
