from pydantic import BaseModel


class Examples_Convertor(BaseModel):
    user_prompt: str
    completion: str


class English_To_Hindi_Convertor(BaseModel):
    role: str
    description: list[str]
    instructions: str
    examples: list[Examples_Convertor]


class Convertor_Example_Input(BaseModel):
    query: str
    one: str = None
    two: str = None
    three: str = None


class Examples_Convertor(BaseModel):
    input: Convertor_Example_Input
    confidence_score: dict


class Confidence_Score(BaseModel):
    role: str
    description: list[str]
    instructions: str
    examples: list[Examples_Convertor]
