class Agent:
    def __init__(self, id, model, prompt, next_agent, client, output_format, input_format):
        self.id = id
        self.model = model
        self.prompt = prompt
        self.next_agent = next_agent
        self.client = client
        self.output_format = output_format
        self.input_format = input_format

    def get_id(self):
        return self.id

    def request(self, request):

        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": request},
            ],
            response_format=self.output_format,
        )
        return completion.choices[0].message.content
