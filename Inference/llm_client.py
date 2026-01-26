import os
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL", "https://api.mistral.ai/v1") 
)

async def ask_llm(system_prompt: str, user_prompt: str):
    """
    Non-blocking call to the LLM.
    'await' allows the event loop to handle other tasks while the LLM responds.
    """
    try:
        
        llm_model = os.getenv("LLM_MODEL", "mistral-small-latest") 

        response = await client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=1000 
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"LLM API call error: {e}")
        return "Technical error during offer generation. Please check API key and service status."