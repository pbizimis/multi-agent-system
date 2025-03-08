from pydantic import BaseModel


class CriticOutput(BaseModel):
    feedback: str


class CriticInput(BaseModel):
    prompt: str
    code: str
    debugger_output: str


# Critic Agent
critic_prompt = """
You are a professional code critic.
You will receive two parts, the code question and
the code that was written. Your job is to look at the code and write a comprehensive
feedback. Do not include code. Only write feedback and step by step instructions that another
LLM can follow to correct the code. Only critic the code for pure functionality. Do not care about styling,
comments or other cosmetic things. Also, if you think the code is correct, just reply with DONE. Nothing else!
Only DONE in all caps. Do not include any other words if the code is correct. Only "DONE".
"""
