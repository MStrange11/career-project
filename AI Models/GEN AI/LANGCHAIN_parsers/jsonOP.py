from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from dotenv import load_dotenv


load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id='google/gemma-2-2b-it',
    task='text-generation',
)

model = ChatHuggingFace(llm=llm)

parser = JsonOutputParser()

template = PromptTemplate(
    template = 'Give me 5 facts about {topic} \n{format_instructions}',
    input_variables = ['topic'],
    partial_variables={
        'format_instructions': parser.get_format_instructions()
    }
)

chain = template | model | parser
final_res = chain.invoke({'topic': 'blockchain'}) # This will invoke the chain with the topic variable
# final_res is a dictionary containing the parsed JSON response

print(f"Response: {final_res}") # This will print the entire JSON response
# Response: {'name': 'Elara Willowbreeze', 'age': 27, 'city': 'Windhaven'}