from pydantic import BaseModel
from agent import Agent


class DebuggerOutput(BaseModel):
    feedback: str


class DebuggerInput(BaseModel):
    prompt: str
    code: str


class DebuggerAgent(Agent):
    def __init__(self):
        super.__init__()
        self.assistant, self.thread = self.setup()

    def setup(self):

        assistant = self.client.beta.assistants.create(
            instructions=debugger_prompt,
            model=self.model,
            tools=[{"type": "code_interpreter"}],
        )

        thread = self.client.beta.threads.create()

        return assistant, thread

    def request(self, request):

        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content="request",
        )

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

        if run.status == "completed":
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            print(messages)
        else:
            print(run.status)


debugger_prompt = """
You are a code executor. You will receive code and a prompt. The prompt function is the ground truth and you should generate test cases based on the requirements defined there. You should run the code and assert the output of the code to the test cases. If they match, just respond with 'CODE WORKS CORRECTLY', if they don't match, respond with the mismatch.
"""
