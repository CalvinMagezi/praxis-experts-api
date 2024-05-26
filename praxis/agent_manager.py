import os
import time
from openai import OpenAI

# Ensure the environment variable is loaded
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No OpenAI API key found in environment variables")

client = OpenAI(api_key=api_key)

class AgentManager:
    def create_agent(self, name, instructions, tools, model):
        return client.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=tools,
            model=model
        )

    def create_and_run_thread(self, assistant_id, messages):
        run = client.beta.threads.create_and_run(
            assistant_id=assistant_id,
            thread={"messages": messages}
        )
        while run.status not in ['completed', 'failed', 'cancelled']:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                run_id=run.id,
                thread_id=run.thread_id
            )
        return run

    def list_thread_messages(self, thread_id):
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return [
            {
                "role": msg.role,
                "content": "".join(block.text.value for block in msg.content if hasattr(block, 'text') and hasattr(block.text, 'value'))
            } for msg in messages
        ]