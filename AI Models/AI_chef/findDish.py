import os
import streamlit as st
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd

# Load environment variables
load_dotenv()

# --- PYDANTIC MODELS ---
class Dish(BaseModel):
    dish_name: str = Field(description="The name of the suggested dish")
    ingredients_used: List[str] = Field(description="List of ingredients from the available list that are used in this dish")
    dish_description: str = Field(description="Brief description of the dish (2-3 sentences)")
    step_by_step_recipe: str = Field(description="Detailed step-by-step recipe instructions")

# --- STREAMLIT APP CONFIGURATION ---
st.set_page_config(
    page_title="🤖 AI Chef - Dish Suggestions",
    page_icon="🍳",
    layout="wide"
)

# --- HELPER FUNCTIONS ---
@st.cache_resource
def initialize_model():
    """Initialize the ChatGoogleGenerativeAI model"""
    try:
        return ChatGoogleGenerativeAI(
            model="models/gemini-1.5-flash", 
            temperature=0.7,
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
    except Exception as e:
        st.error(f"Error initializing model: {e}")
        return None

def create_chain():
    """Create the LangChain chain for dish suggestion"""
    # Set up parser
    parser = PydanticOutputParser(pydantic_object=Dish)
    
    # Create prompt template
    template = PromptTemplate(
        template=(
            "You are an expert AI Chef. Based on the available ingredients and dietary preference, "
            "suggest ONE delicious dish that can be made using SOME OR ALL of the available ingredients.\n\n"
            "IMPORTANT RULES:\n"
            "- Only suggest dishes that match the {diet_preference} dietary preference\n"
            "- Use as many ingredients from the available list as possible\n"
            "- Focus on creating a practical, easy-to-make dish\n"
            "- Provide clear, numbered steps in the recipe\n\n"
            "{format_instructions}\n\n"
            "Dietary Preference: {diet_preference}\n"
            "Available Ingredients: {ingredients}\n"
        ),
        input_variables=["ingredients", "diet_preference"],
        partial_variables={'format_instructions': parser.get_format_instructions()}
    )
    
    # Initialize model
    model = initialize_model()
    if not model:
        return None
    
    # Create chain
    return template | model | parser

def analyze_ingredient_usage(available_ingredients, dish_ingredients_used):
    """Analyze ingredient usage and create appropriate message"""
    available_set = set(item.lower().strip() for item in available_ingredients)
    used_set = set(item.lower().strip() for item in dish_ingredients_used)
    
    # Find actual matches (case-insensitive)
    actual_used = available_set.intersection(used_set)
    unused_from_available = available_set - used_set
    
    # Convert back to original case for display
    used_ingredients = []
    unused_ingredients = []
    
    for ingredient in available_ingredients:
        if ingredient.lower().strip() in actual_used:
            used_ingredients.append(ingredient)
        else:
            unused_ingredients.append(ingredient)
    
    return used_ingredients, unused_ingredients

def create_usage_message(dish_name, used_ingredients, unused_ingredients, total_available):
    """Create appropriate usage message based on ingredient usage"""
    used_count = len(used_ingredients)
    total_count = len(total_available)
    
    if used_count == total_count:
        # Uses all ingredients
        return f"✅ You can make **{dish_name}** using all your available ingredients!"
    elif used_count == total_count - 1:
        # Uses almost all ingredients
        unused_str = ", ".join(unused_ingredients)
        return f"✅ You can make **{dish_name}** with most of your ingredients (excluding {unused_str})"
    elif used_count >= total_count // 2:
        # Uses half or more ingredients
        used_str = ", ".join(used_ingredients)
        return f"➡️ You can make **{dish_name}** with some of your ingredients: {used_str}"
    else:
        # Uses few ingredients
        used_str = ", ".join(used_ingredients)
        return f"🔸 You can make **{dish_name}** with only these ingredients from your list: {used_str}"

def display_recipe_expander(recipe_text, dish_name):
    """Display recipe in an expandable section"""
    with st.expander(f"📝 Recipe for {dish_name}", expanded=False):
        st.write(recipe_text)

# --- MAIN STREAMLIT APP ---
def main():
    st.title("🤖 AI Chef - Dish Suggestions")
    st.markdown("---")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("🥗 Your Kitchen")
        
        # Diet preference
        diet_preference = st.selectbox( 
            "Dietary Preference:",
            ["Vegetarian", "Non-Vegetarian", "Vegan", "Keto", "Mediterranean"]
        )
        
        # Ingredients input
        st.subheader("Available Ingredients")
        ingredients_input = st.text_area(
            "Enter your ingredients (one per line):",
            value="Broccoli\nCarrot\nOnion\nGarlic\nGinger",
            height=200
        )
        
        # Parse ingredients
        if ingredients_input:
            ingredients_list = [ing.strip() for ing in ingredients_input.split('\n') if ing.strip()]
        else:
            ingredients_list = []
        
        # Display current ingredients
        if ingredients_list:
            st.success(f"✅ {len(ingredients_list)} ingredients ready!")
            for i, ing in enumerate(ingredients_list, 1):
                st.write(f"{i}. {ing}")
        
        # Find dish button
        find_dish = st.button("🔍 Find Dish Suggestions", type="primary", use_container_width=True)
    
    # Main content area
    if not ingredients_list:
        st.info("👈 Please add some ingredients in the sidebar to get started!")
        st.markdown("""
        ### How to use:
        1. Select your dietary preference
        2. Enter your available ingredients (one per line)
        3. Click "Find Dish Suggestions"
        4. Get personalized recipe recommendations!
        """)
        return
    
    if find_dish:
        if len(ingredients_list) < 2:
            st.warning("Please add at least 2 ingredients for better suggestions!")
            return
            
        # Show loading
        with st.spinner("🤖 AI Chef is thinking of delicious dishes..."):
            try:
                # Create chain
                chain = create_chain()
                if not chain:
                    st.error("Failed to initialize AI model. Please check your API key.")
                    return
                
                # Generate multiple suggestions
                suggestions = []
                ingredients_str = ", ".join(ingredients_list)
                
                # Generate 3 different suggestions
                for i in range(3):
                    try:
                        response = chain.invoke({
                            "ingredients": ingredients_str,
                            "diet_preference": diet_preference
                        })
                        suggestions.append(response)
                    except Exception as e:
                        st.warning(f"Could only generate {i} suggestions. Error: {str(e)}")
                        break
                
                if not suggestions:
                    st.error("Sorry, couldn't generate any suggestions. Please try again.")
                    return
                
                # Display results
                st.success(f"🎉 Found {len(suggestions)} delicious {diet_preference.lower()} dish suggestions!")
                st.markdown("---")
                
                # Create and display results table
                table_data = []
                for i, dish in enumerate(suggestions, 1):
                    used_ingredients, unused_ingredients = analyze_ingredient_usage(
                        ingredients_list, dish.ingredients_used
                    )
                    
                    usage_message = create_usage_message(
                        dish.dish_name, used_ingredients, unused_ingredients, ingredients_list
                    )
                    
                    table_data.append({
                        "Suggestion": f"#{i}",
                        "Dish Name": dish.dish_name,
                        "Description": dish.dish_description,
                        "Ingredient Usage": usage_message,
                        "Used Ingredients": ", ".join(used_ingredients) if used_ingredients else "None",
                        "Recipe": dish.step_by_step_recipe
                    })
                
                # Display as cards instead of table for better readability
                for i, data in enumerate(table_data):
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.subheader(f"🍽️ {data['Dish Name']}")
                            st.write(data['Description'])
                            st.markdown(data['Ingredient Usage'])
                            
                            if data['Used Ingredients'] != "None":
                                st.markdown(f"**Ingredients from your list:** {data['Used Ingredients']}")
                        
                        with col2:
                            st.metric("Suggestion", data['Suggestion'])
                        
                        # Recipe expander
                        display_recipe_expander(data['Recipe'], data['Dish Name'])
                        
                        if i < len(table_data) - 1:
                            st.markdown("---")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your Google API key and try again.")

if __name__ == "__main__":
    # Check for API key
    if not os.getenv('GOOGLE_API_KEY'):
        st.error("⚠️ Google API Key not found! Please set GOOGLE_API_KEY in your .env file")
        st.info("You need a Google API key to use the Gemini model. Get one from: https://makersuite.google.com/app/apikey")
    else:
        main()