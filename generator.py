from pydantic import BaseModel


class GeneratorInput(BaseModel):
    prompt: str
    plan: str
    code: str
    feedback: str


class GeneratorOutput(BaseModel):
    code: str


generator_prompt = """
You are a professional code generator.
Based on the question, generate clean and correct python code.
Your code does not need comments, types or formatting. Also, do not include
a main function. Only the necessary code function and the necessary imports.
"""
