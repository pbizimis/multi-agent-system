from openai import OpenAI
from agent import Agent
from generator import GeneratorInput, GeneratorOutput, generator_prompt
from critic import CriticInput, CriticOutput, critic_prompt
from planner import PlannerInput, PlannerOutput, planner_prompt
from debugger import DebuggerInput, DebuggerOutput, debugger_prompt
import json


class MAS:
    def __init__(self):
        self.agents = {}
        self.first_agent = None
        self.client = OpenAI()

    def add_agent(self, id, model, prompt, next_agent, output_format, input_format):
        agent = Agent(
            id, model, prompt, next_agent, self.client, output_format, input_format
        )
        self.agents[id] = agent
        return agent

    def run(self, message):
        if self.first_agent is None:
            return print("Please set an entry agent")

        data = {
            "prompt": message,
            "code": "",
            "feedback": "",
            "debugger_output": "",
            "plan": "",
        }

        agent = self.agents[self.first_agent]
        while True:

            complete_prompt = ""

            for field in agent.input_format.model_fields.keys():
                complete_prompt += f"{field}:\n{data[field]}\n\n"

            print("\n")
            print("Calling Agent", agent.id)
            print("Input prompt: \n", complete_prompt)

            resp = agent.request(message)
            resp_data = json.loads(resp)
            print("Output: \n", resp_data)
            for k in resp_data.keys():
                data[k] = resp_data[k]

            print("\n")
            print("MAS data: \n", data)

            if agent.next_agent is None or data["feedback"] == "DONE":
                return data["code"]

            message = resp
            agent = self.agents[agent.next_agent]

    def set_first_agent(self, agent_id):
        self.first_agent = agent_id


def create_PGC():
    print("Initialize Planner, Generator, Critic Multi-Agent-System")
    mas = MAS()

    mas.add_agent(
        "planner",
        "o3-mini-2025-01-31",
        planner_prompt,
        "coder",
        PlannerOutput,
        PlannerInput,
    )

    mas.add_agent(
        "critic",
        "o3-mini-2025-01-31",
        critic_prompt,
        "coder",
        CriticOutput,
        CriticInput,
    )

    mas.add_agent(
        "coder",
        "o3-mini-2025-01-31",
        generator_prompt,
        "critic",
        GeneratorOutput,
        GeneratorInput,
    )

    mas.first_agent = "planner"

    return mas


def create_GC():
    print("Initialize Generator, Critic Multi-Agent-System")
    mas = MAS()

    mas.add_agent(
        "critic",
        "o3-mini-2025-01-31",
        critic_prompt,
        "coder",
        CriticOutput,
        CriticInput,
    )

    mas.add_agent(
        "coder",
        "o3-mini-2025-01-31",
        generator_prompt,
        "critic",
        GeneratorOutput,
        GeneratorInput,
    )

    mas.first_agent = "coder"

    return mas


def create_PGDC():
    print("Initialize Planner, Generator, Debugger, Critic Multi-Agent-System")
    mas = MAS()

    mas.add_agent(
        "planner",
        "o3-mini-2025-01-31",
        planner_prompt,
        "coder",
        PlannerOutput,
        PlannerInput,
    )

    mas.add_agent(
        "critic",
        "o3-mini-2025-01-31",
        critic_prompt,
        "coder",
        CriticOutput,
        CriticInput,
    )

    mas.add_agent(
        "coder",
        "o3-mini-2025-01-31",
        generator_prompt,
        "debugger",
        GeneratorOutput,
        GeneratorInput,
    )

    mas.add_agent(
        "debugger",
        "o3-mini-2025-01-31",
        debugger_prompt,
        "critic",
        DebuggerOutput,
        DebuggerInput,
    )

    mas.first_agent = "planner"

    return mas


p = """
    from typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    \"\"\"\n
    """

GC = create_PGC()
print(GC.run(p))
