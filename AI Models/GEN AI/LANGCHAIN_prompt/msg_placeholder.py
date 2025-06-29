from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


chat_template = ChatPromptTemplate([
    ('system', 'you are a helpful customer support agent'),
    MessagesPlaceholder(variable_name="chat_history"),
    ('human', '{query}'),
])

chat_history = []

with open("LANGCHAIN_prompt/chat_history.txt", "r") as file:
    chat_history.extend(file.readlines())
    
# print(chat_history)

prompt = chat_template.invoke({
    "chat_history": chat_history,
    "query": "What is the status of my order?"
})


print(prompt)
