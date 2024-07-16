import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv('AI_TOKEN'))

async def gptTurbo(question):
    response = await client.chat.completions.create(
        messages=[{'role': 'user',
                   'content': str(question)}],
        model="gpt-3.5-turbo"
    )
    return response