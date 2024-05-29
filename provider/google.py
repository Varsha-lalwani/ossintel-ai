import vertexai

from response import CompleteResponse
from typing import Dict, List
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel
)

class VertexAI:
    def __init__(self, project_id: str, location: str = 'us-west1'):
        self.project_id = project_id
        self.location = location
        vertexai.init(project=project_id, location=location)

    def text(self,
             prompt: str,
             model_name: str,
             temperature: float,
             max_output_tokens: int,
             top_p: float,
             top_k: int,
             ) -> CompleteResponse:
        instructions = "If the packages are not asked return empty json. Search and Return the array of json elements where each element has complete \"packageName\" and \"repositoryUrl\". Return all  packages. Don't provide me duplicates. Both of \"packageName\" and \"repositoryUrl\" shouldn't contain version.\nResponse should be like [\n{\n packageName: \"abcd\",\nrepopsitoryUrl: \"xyz\"\n},\n{\n packageName: \"def\",\nrepopsitoryUrl: \"ddd\"\n}\n]"
        model = GenerativeModel(model_name,
                                 system_instruction=[instructions])
        
        response = model.generate_content(
            prompt,
            generation_config=GenerationConfig(temperature=temperature,
                                                max_output_tokens=max_output_tokens,
                                                top_p=top_p,
                                                top_k=top_k),
        )
        return CompleteResponse(**{"text": response.text})




