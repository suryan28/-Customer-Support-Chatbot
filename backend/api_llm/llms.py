import json
import logging
import os
from typing import Optional, Text
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class OpenAPI:
    def __init__(
            self,
            completions_model=os.environ.get(
                "OPENAI_COMPLETIONS_MODEL", "gpt-3.5-turbo"
            ),
            completions_temperature=float(
                os.environ.get("OPENAI_COMPLETIONS_TEMPERATURE", 0)
            ),
            completions_max_tokens=int(
                os.environ.get("OPENAI_COMPLETIONS_MAX_TOKENS", 100)
            ),
            completions_api_key=os.environ.get("OPENAI_COMPLETIONS_API_KEY", None),
    ):
        self.completions_model = completions_model
        self.completions_temperature = completions_temperature
        self.completions_max_tokens = completions_max_tokens
        self.completions_api_key = completions_api_key

    @staticmethod
    def _extract_text_response(choices) -> Optional[Text]:
        try:
            choice = choices.content

            logger.info(f"LLM response: \n{choice}\n")

            response_json = json.loads(choice)
            return response_json
        except Exception as e:
            logger.exception(f"Error occurred while extracting the LLM response. {e}")
            return None

    def get_text_completion(self, prompt: list) -> Optional[list]:
        logger.info(f"LLM prompt: \n{prompt}\n")
        client = OpenAI(api_key=self.completions_api_key)

        completion = client.chat.completions.create(model=self.completions_model,
                                                    temperature=self.completions_temperature,
                                                    messages=prompt,
                                                    max_tokens=self.completions_max_tokens,
                                                    )
        choices = completion.choices[0].message
        return self._extract_text_response(choices=choices)
