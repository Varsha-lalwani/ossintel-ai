import vertexai
import json

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
             ecosystem: str,
             model_name: str,
             temperature: float,
             max_output_tokens: int,
             top_p: float,
             top_k: int,
             ) :
        instructions = "You are a package searching engine.\
            You will list the packages based on the inputs.\
            Return the result as a JSON. \
            The response format should be as follows:\
            Don't return duplicates. \
            {\"packages\" :[\
            {\
            \"packageName\": \"abcd\",\
            \"repositoryUrl\": \"xyz\"\
            },\
            {\
            \"packageName\": \"def\",\
            \"repositoryUrl\": \"ddd\"\
            }\
            ]\
            }\
            The response should be a JSON Object with a key \"packages\" and value as an array of JSON objects. \
            Each JSON object should have two keys \"packageName\" and \"repositoryUrl\". \
            The packages array  should contain as many packages as available for the usecase but max 15 packages based with no duplicates. \
            Ensure that both \"packageName\" and \"repositoryUrl\" do not include version information. \
            Don't return json in any other format."
        model = GenerativeModel(model_name,
                                 system_instruction=[instructions])
        
        response = model.generate_content(
            "In" + ecosystem +prompt,
            generation_config=GenerationConfig(temperature=temperature,
                                                max_output_tokens=max_output_tokens,
                                                top_p=top_p,
                                                top_k=top_k),
        )
        print(response.text)
        str = response.text
        str = str.replace("```", "")
        str = str.replace("json", "")
        return json.loads(str)




