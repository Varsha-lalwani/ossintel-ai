from pydantic import BaseModel


class CompleteResponse(BaseModel):
    text: str = ""

    def __init__(self, **kargs):
        self.__dict__.update(kargs)
