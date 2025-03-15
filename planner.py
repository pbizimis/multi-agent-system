from pydantic import BaseModel


class PlannerOutput(BaseModel):
    plan: str


class PlannerInput(BaseModel):
    prompt: str


# Critic Agent
planner_prompt = """
You are an expert planning agent tasked with analyzing a coding request.
Outline a detailed implementation plan for a code generation model to follow.

Requirements:
- Break the coding task into logical, sequential steps.
- Clearly specify edge cases and constraints.
- Suggest algorithms, data structures, or Python libraries needed.
- Define expected inputs and outputs, providing examples if possible.
- Highlight performance considerations (time and space complexity), if applicable.

Do NOT generate code; provide ONLY the implementation plan.
"""
