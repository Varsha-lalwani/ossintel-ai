from typing_extensions import TypedDict
from pydantic import BaseModel
from typing import List, Union


class ModelParameters(BaseModel):
    temperature: Union[float, None] = 0
    max_output_tokens: Union[int, None] = 4000
    top_p: Union[float, None] = 0.95
    top_k: Union[int, None] = 40


class CompletePromptParameters(BaseModel):
    prompt: str
    model_name: Union[str, None] = "gemini-1.0-pro-002"
    model_parameters: ModelParameters = ModelParameters(
        temperature=0,
        max_output_tokens=2000,
        top_p=0.1,
        top_k=1)

    def get_payload_size(self):
        return len(self.prompt)
