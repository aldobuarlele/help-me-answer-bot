import asyncio
from groq import Groq
from src.utils.config_loader import RootConfig

class AiService:
    def __init__(self, config: RootConfig, api_key: str):
        self.config = config
        self.client = Groq(api_key=api_key)

    async def get_response(self, user_message: str, system_instruction: str = None) -> str:
        try:
            def _generate():
                messages = []
                if system_instruction:
                    messages.append({"role": "system", "content": system_instruction})
                
                messages.append({"role": "user", "content": user_message})

                completion = self.client.chat.completions.create(
                    model=self.config.ai_settings.model_name,
                    messages=messages,
                    temperature=self.config.ai_settings.temperature,
                    top_p=self.config.ai_settings.top_p,
                )
                return completion.choices[0].message.content

            response = await asyncio.to_thread(_generate)
            return response
        except Exception as e:
            raise RuntimeError(f"AI Service Error: {str(e)}")