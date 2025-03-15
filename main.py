import json
from human_eval.data import write_jsonl, read_problems
from openai import OpenAI
from agent import Agent
from generator import GeneratorInput, GeneratorOutput, generator_prompt
from critic import CriticInput, CriticOutput, critic_prompt
from planner import PlannerInput, PlannerOutput, planner_prompt
from debugger import DebuggerInput, DebuggerOutput, debugger_prompt


class MAS:
    def __init__(self):
        self.agents = {}
        self.first_agent = None
        self.client = OpenAI()
        self.counter = 0
        self.feedback_counter = []

    def add_agent(self, id, model, prompt, next_agent, output_format, input_format):
        agent = Agent(
            id, model, prompt, next_agent, self.client, output_format, input_format
        )
        self.agents[id] = agent
        return agent

    def run(self, message):

        self.counter += 1
        print("PROBLEM", self.counter)

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
        counter = 0
        while True:

            if agent.id == "coder":
                counter += 1

            complete_prompt = ""

            for field in agent.input_format.model_fields.keys():
                if field == "prompt":
                    complete_prompt += f"This is the ground truth prompt. This is what asked of you. Make sure that any output code matches the function and parameter names defined here:\n{
                        data[field]}\n\n"
                elif field == "code":
                    if data["code"]:
                        complete_prompt += f"This is the currently generated code. It might be wrong. Please compare the function and parameter names to the function above in the ground truth prompt:\n{
                            data[field]}\n\n"
                elif data[field]:
                    complete_prompt += f"{field}:\n{data[field]}\n\n"

            resp = agent.request(message)
            resp_data = json.loads(resp)
            for k in resp_data.keys():
                data[k] = resp_data[k]

            if agent.next_agent is None or "NO" in data["feedback"]:
                self.feedback_counter.append(counter)
                return data["code"]

            message = resp
            agent = self.agents[agent.next_agent]

    def set_first_agent(self, agent_id):
        self.first_agent = agent_id


def create_PGC():
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
        "coder",
        "o3-mini-2025-01-31",
        generator_prompt,
        "critic",
        GeneratorOutput,
        GeneratorInput,
    )

    mas.add_agent(
        "critic",
        "o3-mini-2025-01-31",
        critic_prompt,
        "planner",
        CriticOutput,
        CriticInput,
    )

    mas.first_agent = "planner"

    return mas


def create_GC():
    mas = MAS()

    mas.add_agent(
        "coder",
        "o3-mini-2025-01-31",
        generator_prompt,
        "critic",
        GeneratorOutput,
        GeneratorInput,
    )

    mas.add_agent(
        "critic",
        "o3-mini-2025-01-31",
        critic_prompt,
        "coder",
        CriticOutput,
        CriticInput,
    )

    mas.first_agent = "coder"

    return mas


def create_PGCD():
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

    mas.add_agent(
        "critic",
        "o3-mini-2025-01-31",
        critic_prompt,
        "planner",
        CriticOutput,
        CriticInput,
    )

    mas.first_agent = "planner"

    return mas


def create_GCD():
    mas = MAS()

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

    mas.add_agent(
        "critic",
        "o3-mini-2025-01-31",
        critic_prompt,
        "coder",
        CriticOutput,
        CriticInput,
    )

    mas.first_agent = "coder"

    return mas


def create_G():
    mas = MAS()

    mas.add_agent(
        "coder",
        "o3-mini-2025-01-31",
        generator_prompt,
        None,
        GeneratorOutput,
        GeneratorInput,
    )
    mas.first_agent = "coder"

    return mas


G = create_G()
GC = create_GC()
PGC = create_PGC()
GCD = create_PGCD()
PGCD = create_PGCD()
all_configs = [G, GC, PGC, GCD, PGCD]

print("All configurations created!")

print("RUNNING THE BENCHMARK CAN RESULT IN HIGH OPENAI API COSTS!")

for idx, config in enumerate(all_configs):
    print("Running config " + str(idx + 1) + "/" + str(len(all_configs)))
    problems = read_problems()

    num_samples_per_task = 1
    samples = [
        dict(task_id=task_id, completion=config.run(
            problems[task_id]["prompt"]))
        for task_id in problems
        for _ in range(num_samples_per_task)
    ]
    write_jsonl("config" + str(idx + 1) + ".jsonl", samples)
