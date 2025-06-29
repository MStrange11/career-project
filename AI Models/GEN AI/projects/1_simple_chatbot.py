from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the Google Generative AI model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Initialize an empty chat history
L_char_history = [
    SystemMessage(content="You are a helpful assistant."),
]

while True:
    # Get user input
    user_input = input("You: ")

    # Exit the loop if the user types 'exit'
    if user_input.lower() == 'exit':
        print("Exiting the chatbot. Goodbye!")
        break

    # chat_history.append(user_input)
    L_char_history.append(HumanMessage(content=user_input))

    # Generate a response from the model
    # response = model.invoke(user_input) # for single-turn chat

    # Alternatively, for multi-turn chat, you can use:
    response = model.invoke(L_char_history)  # Pass the entire chat history
    L_char_history.append(AIMessage(content=response.content))


    # Print the model's response
    print(f"Bot: {response.content}")

print("Chat history:", L_char_history)  # Optional: print the chat history