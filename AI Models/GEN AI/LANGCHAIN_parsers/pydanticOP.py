from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id='google/gemma-2-2b-it',
    task='text-generation',
)

model = ChatHuggingFace(llm=llm)

class Person(BaseModel):
    name: str = Field(description="The name of the person")
    age: int = Field(gt=18, description="The age of the person")
    city: str = Field(description="Name of the city the person belongs to")


parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template = "Generate the name, age, and city of a fictional {place} person\n{format_instructions}",
    input_variables = ['place'],
    partial_variables = {
        'format_instructions': parser.get_format_instructions()
    }
)
# print(template.invoke({'place': 'Indian'}))

chain = template | model | parser
final_res = chain.invoke({'place': 'Indian'})
print(f"Response: {final_res}")
print(type(final_res))

print(final_res.model_dump_json(indent=4))

