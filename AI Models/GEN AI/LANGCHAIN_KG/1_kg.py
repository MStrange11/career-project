from typing import Dict, List, Tuple
import google.generativeai as genai
from pprint import pprint
from dotenv import load_dotenv
import os
load_dotenv()

key = os.getenv("GOOGLE_API_KEY")
print("Key: ",key)

# Initialize Gemini
genai.configure(api_key=key)  # Replace with your actual API key

model = genai.GenerativeModel('gemini-pro')

# Define a simple knowledge graph about programming languages
knowledge_graph = {
    "Python": {
        "type": "Programming Language",
        "created_by": "Guido van Rossum",
        "year_created": 1991,
        "paradigm": ["Object-oriented", "Imperative", "Functional", "Procedural"],
        "typing": ["Dynamic", "Strong"],
        "related_technologies": ["Django", "Flask", "Pandas", "NumPy"]
    },
    "JavaScript": {
        "type": "Programming Language",
        "created_by": "Brendan Eich",
        "year_created": 1995,
        "paradigm": ["Event-driven", "Functional", "Imperative"],
        "typing": ["Dynamic", "Weak"],
        "related_technologies": ["Node.js", "React", "Vue", "Angular"]
    },
    "Java": {
        "type": "Programming Language",
        "created_by": "James Gosling",
        "year_created": 1995,
        "paradigm": ["Object-oriented", "Structured", "Imperative"],
        "typing": ["Static", "Strong"],
        "related_technologies": ["Spring", "Hibernate", "Android"]
    }
}

def query_knowledge_graph(language: str, query: str) -> str:
    """Query the knowledge graph for specific information about a language."""
    if language not in knowledge_graph:
        return f"Sorry, I don't have information about {language} in my knowledge graph."
    
    if "paradigm" in query.lower():
        return f"{language} follows these programming paradigms: {', '.join(knowledge_graph[language]['paradigm'])}"
    elif "created" in query.lower() and "year" in query.lower():
        return f"{language} was created in {knowledge_graph[language]['year_created']} by {knowledge_graph[language]['created_by']}."
    elif "technologies" in query.lower() or "frameworks" in query.lower():
        return f"Related technologies for {language} include: {', '.join(knowledge_graph[language]['related_technologies'])}"
    else:
        return f"Here's what I know about {language}: {knowledge_graph[language]}"

def enhance_with_llm(context: str, query: str) -> str:
    """Enhance the response using Gemini LLM."""
    prompt = f"""
    Context: {context}
    
    Question: {query}
    
    Based on the context above, provide a detailed and helpful response.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error querying the language model: {str(e)}"

def main():
    print("Welcome to the Programming Language Knowledge Graph!")
    print("Available languages in the knowledge graph:")
    for lang in knowledge_graph.keys():
        print(f"- {lang}")
    
    while True:
        print("\nWhat would you like to know? (type 'exit' to quit)")
        user_input = input("> ")
        
        if user_input.lower() == 'exit':
            break
            
        # Simple keyword matching to determine the language
        language = None
        for lang in knowledge_graph.keys():
            if lang.lower() in user_input.lower():
                language = lang
                break
                
        if not language:
            print("I can only provide information about Python, JavaScript, and Java in this example.")
            continue
            
        # First, try to get information from the knowledge graph
        kg_response = query_knowledge_graph(language, user_input)
        print("\n[Knowledge Graph Response]")
        print(kg_response)
        
        # Then enhance with LLM
        print("\n[Enhanced with Gemini]")
        enhanced_response = enhance_with_llm(kg_response, user_input)
        print(enhanced_response)

if __name__ == "__main__":
    main()