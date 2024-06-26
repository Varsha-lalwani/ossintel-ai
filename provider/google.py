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
        instructions = "You are a oss packages searching engine.\
            You will list the packages based on the requirement.\
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
            Package name should be the exact name of package from the ecosystem. \
            For example the exact package name in https://www.npmjs.com/package for zip.js is \"@zip.js/zip.js\". \
            Another example for log4j-core the package name is \"org.apache.logging.log4j:log4j-core\". \
            Repository url should be the url of the repository where the package source code is present. This can be from github/ gitlab/ bitbucket etc. \
            The packages list shouldn't have any duplicates. \
            The packages array should contain as many packages as available for the usecase with a upper limit of 10 packages.\
            Ensure that both \"packageName\" and \"repositoryUrl\" do not include version information. \
            Don't return more than 1 entry from a single person. \
            Don't return json in any other format."
        model = GenerativeModel(model_name,
                                 system_instruction=[instructions])
        newPrompt = add_ecosystem(prompt, ecosystem)
        print(newPrompt)
        print(prompt)
        response = model.generate_content(
            newPrompt,
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

def add_ecosystem (prompt: str, ecosystem: str):
    if (ecosystem == "NPM"):
        return "For JS " + prompt + "In NPM ecosystem"
    elif (ecosystem == "MAVEN"):
        return "For Java " + prompt + "In Maven ecosystem"
    elif (ecosystem == "PYPI"):
        return "For Python " + prompt + "In PyPi ecosystem"
    elif (ecosystem == "GO"):
        return "For Go " + prompt + "In Go ecosystem"
    else :
        return "For " + ecosystem + " " + prompt


