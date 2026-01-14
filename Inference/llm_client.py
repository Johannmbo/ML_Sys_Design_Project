import os
from openai import AsyncOpenAI


client = AsyncOpenAI(
    api_key=os.getenv("LLM_API_KEY"), 
    base_url="https://api.mistral.ai/v1" 
)

async def ask_llm(system_prompt: str, user_prompt: str):
    try:
    
        response = await client.chat.completions.create(
            model="mistral-tiny",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:

        print(f"Error calling API : {e}")
        return "Service temporarily unavailable."