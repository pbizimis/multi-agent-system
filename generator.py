from pydantic import BaseModel


class GeneratorInput(BaseModel):
    prompt: str
    plan: str
    code: str
    feedback: str


class GeneratorOutput(BaseModel):
    code: str


generator_prompt = """
You are an expert Python code generator. You will receive a detailed implementation plan. Generate correct and functional Python code strictly following the provided plan. Please use the EXACT naming conventions listed in the prompt function following 'prompt:'. If no plan is given, generate code according to the requirements given in 'prompt:'. This is the ground truth.

NEVER UNDER ANY CIRCUMSTANCES CHANGE THE FUNCTION AND PARAMETER NAMES OF THE FUNCTION IN {prompt:}.

Your code must:
- Include ONLY the necessary Python function(s) and imports.
- Exclude comments, type annotations, formatting, example usage, print statements, and the main function.
- Explicitly handle edge cases and constraints mentioned in the implementation plan.
"""
