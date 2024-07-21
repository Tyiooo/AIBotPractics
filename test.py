from dotenv import load_dotenv
from app.settings import settings
import openai

load_dotenv()
client = openai.OpenAI(api_key=settings.AI_TOKEN)


def gpt_turbo(question):
    assistant = client.beta.assistants.create(
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo"
    )
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=str(question)
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            assistant_responses = [
                msg.content[0].text.value
                for msg in messages.data if msg.role == 'assistant'
            ]

            return assistant_responses[-1] if assistant_responses else "No response from assistant"
