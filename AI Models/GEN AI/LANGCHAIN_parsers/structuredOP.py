from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id='google/gemma-2-2b-it',
    task='text-generation',
)

model = ChatHuggingFace(llm=llm)

schema = [
    ResponseSchema(name = "fact_1", description = "Fact 1 about the topic"),
    ResponseSchema(name = "fact_2", description = "Fact 2 about the topic"),
    ResponseSchema(name = "fact_3", description = "Fact 3 about the topic")
]

parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(
    template = "Give me 3 facts about {topic} \n{format_instructions}",
    input_variables = ['topic'],
    partial_variables = {
        'format_instructions': parser.get_format_instructions()
    }
)

chain = template | model | parser
final_res = chain.invoke({'topic': 'blockchain'})
print(f"Response: {final_res}")
