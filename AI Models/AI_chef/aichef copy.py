import streamlit as st
import base64
from PIL import Image
from io import BytesIO
import pandas as pd
import json

# cradentials
from dotenv import load_dotenv
load_dotenv()

# models
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

# error handling
from langchain_core.exceptions import OutputParserException

# Initialize models
# model = ChatGoogleGenerativeAI(model = "gemini-1.5-flash-latest")
model = ChatGoogleGenerativeAI(model = "gemini-1.5-flash", temperature=0.2)

def save_ingredients(ingredients: list[str], key: str = "initail_ingredients"):
    """Saves the ingredients list to a JSON file."""
    j = {key: ingredients}
    lj = load_ingredients()
    if lj:
        lj.update(j)
        j = lj
    with open("ingredients.json", "w") as json_file:
        json.dump(j, json_file, indent=4)
        
def load_ingredients(key: str = None):
    """Loads the ingredients list from a JSON file."""
    try:
        with open("ingredients.json", "r") as json_file:
            if key:
                return json.load(json_file).get(key, [])
            return json.load(json_file)
    except Exception:
        return {}
    
def clear_json(key: str = None):
    """Clears the JSON file."""
    with open("ingredients.json", "w") as json_file:
        json.dump({}, json_file, indent=4)
        
def clear_json():
    """Clears the JSON file."""
    with open("ingredients.json", "w") as json_file:
        json.dump({}, json_file, indent=4)
        
if load_ingredients("delete"):
    clear_json()


def identify_eatable_items(image: Image.Image = None):
    """Identifies eatable items from a PIL Image object."""
    if isinstance(image, Image.Image):
        img_format = image.format
    elif isinstance(image, st.file_uploader):
        img_format = image.type
        
        
    img_buffer = BytesIO()
    
    try:
        image.save(img_buffer, format=img_format.upper())
    except Exception as e:
        return f"Error saving image to buffer: {e}"
    
    image_bytes = img_buffer.getvalue()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    mine_type = f"image/{img_format.lower()}"
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": "You are 'AI Chef'. Identify all eatable food items from the image. List only their names, separated by commas. If none, say 'No edible items found'."},
            {"type": "image_url", "image_url": {"url": f"data:{mine_type};base64,{base64_image}"}},
        ]
    )
    
    try:
        response = model.invoke([message])
        l = sorted([item.strip().capitalize() for item in response.content.split(',')])
        save_ingredients(l, "initail_ingredients")  
        return response.content
    except Exception as e:
        return f"An error occurred: {e}"


def find_dishes_and_ingredients(ingredients = None):
    """Finds dishes based on the given ingredients list."""

    if ingredients is isinstance(list):
        ingredients = ", ".join(ingredients)
    
    # 1. Define the schema for a single dish
    dish_schema = ResponseSchema(
        name="dish_name", 
        description="The name of the suggested dish."
    )
    ingredients_schema = ResponseSchema(
        name="required_ingredients", 
        description="A list of ingredients required for the dish."
    )
    recipe_schema = ResponseSchema(
        name="recipe", 
        description="A simple, step-by-step recipe for preparing the dish."
    )

    # 2. Define the top-level schema to contain a list of dishes
    top_level_schema = ResponseSchema(
        name="dishes",
        description="A list of dictionaries, where each dictionary contains a 'dish_name', 'required_ingredients', and 'recipe'."
    )
    
    # The parser needs to be created from a list of schemas.
    # In this case, we have a list of one schema (our top-level one).
    parser = StructuredOutputParser.from_response_schemas([top_level_schema])
    
    # 3. Create a new, improved template
    template = PromptTemplate(
        template="""You are a world-class AI chef. Your task is to analyze a list of available ingredients and provide a variety of creative and practical dish suggestions.
            Available Ingredients: '{ingredients}'

            Please provide suggestions based on the following criteria:

            1.  **Core Dish**: Suggest a dish that can be made using only the ingredients provided.
            2.  **Ingredient Additions**: Suggest a different dish that could be made if you added only one or two common ingredients. Clearly state which ingredients would need to be added.
            3.  **Ingredient Replacements**: Suggest a new dish that could be made by replacing one of the available ingredients with another common one. Clearly state which ingredient to replace and what to replace it with.
            4.  **Minimalist Dish**: Suggest a simple dish that can be made using a small subset of the available ingredients.

            For each dish suggestion, provide the dish name, a list of required ingredients, and a brief, step-by-step recipe.
            Provide a maximum of 10 dish suggestions.

            {format_instructions}""",
        input_variables=["ingredients"],
        partial_variables={'format_instructions': parser.get_format_instructions()}
    )

    findDish_chain = template | model | parser
     
    try:
        response = findDish_chain.invoke({"ingredients": ingredients})
        return response
    except OutputParserException as e:
        return f"An error occurred with the output format: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- Streamlit App UI ---
def take_input():
    st.set_page_config(page_title="AI Chef", page_icon="🧑‍🍳", layout="centered")
        
    # Header
    st.title("AI Chef 🧑‍🍳")
    st.markdown("### Make from what you have")
    st.subheader("1. Provide Your Ingredients")
    
    input_method = st.radio("Input Method", ["Click Image", "Upload Image"], horizontal=True)
    if input_method == "Click Image":
        # The camera input is now constrained by the column width
        image_file = st.camera_input("Take a picture", label_visibility="collapsed")
    else:
        image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        
    if image_file:
        st.session_state.ingredients = []
        image_bytes = image_file.getvalue()
        st.image(image_file, caption="Uploaded Ingredients")
        
        with st.spinner("AI Chef is identifying ingredients..."):
            ai_response = identify_eatable_items(image_bytes)
            if ai_response and "No edible items found" not in ai_response and "error" not in ai_response:
                st.session_state.ingredients = ai_response
            else:
                st.error(ai_response)
        

def manupulate_input():
    st.subheader("2. Review Your Ingredient List")
    
    ingredients = load_ingredients()
    ingredients = ingredients[ "all_ingredients" if "all_ingredients" in ingredients else "initail_ingredients"]
    
    # Using a form for the unified editor
    with st.form("ingredient_editor_form"):
        
        # The new multiselect editor
        edited_ingredients = st.multiselect(
            "Add or remove items from the list:",
            options=ingredients,
            default=ingredients,
            key="ingredient_multiselect"
        )
        
        new_ingredient = st.text_input("Add a new ingredient:")
        submit_button = st.form_submit_button("Update List")

        if submit_button:
            final_list = set(edited_ingredients)
            if new_ingredient.strip():
                final_list.add(new_ingredient.strip().capitalize())
            save_ingredients(sorted(list(final_list)), "all_ingredients")
            st.rerun()
            
        all_ingredients = "".join([f"<li style='margin-bottom: 6px; color: #fff; font-size: 1em;'>{i}</li>" for i in ingredients])  
        st.markdown(f"""
    <ul style='display: flex; list-style-type: none; padding-left: 0; flex-wrap: wrap; margin-top: 10px;'>
        {all_ingredients}
    </ul>
    """, unsafe_allow_html=True)  
        

def process_ingredients():
    st.subheader("3. Find a Dish!")
    
    if st.button("Suggest a Dish", type="primary"):
        with st.spinner("Chef is thinking of a recipe..."):
            dishes = find_dishes_and_ingredients(st.session_state.ingredients).get("dishes")
            
            if dishes:                
                display_dishes(dishes)
                save_ingredients(True, "delete")
            else:
                st.error("No dishes found for the given ingredients.")
                            
    
def display_dishes(dishes):
    for dish in dishes:
        # Horizontal ingredient chips with color
        ingredients_html = "".join([
            f"<li style='border: 1px solid #fa0; padding: 6px 12px; margin: 6px 8px 0 0; border-radius: 10px; font-size: 1.5em;'>{item}</li>"
            for item in dish["required_ingredients"]
        ])

        # Recipe steps as bullet list
        recipe_html = "".join([
            f"<li style='margin-bottom: 6px; color: #fff; font-size: 1.5em;'>{step}</li>"
            for step in dish["recipe"]
        ])

        # Final formatted markdown with collapsible section
        st.markdown(f"""
    <details style="margin-bottom: 20px; background-color: #232323; padding: 12px 6px; border: 2px solid #d1ecf1; border-radius: 12px; width: 100%;">
        <summary style="font-size: 22px; font-weight: bold; cursor: pointer; color: #fff; padding: 6px 12px; margin: 6px 8px 0 0; border-radius: 10px;">
            {dish['dish_name']}
        </summary>
        <div style="margin-top: 15px;">
            <strong style='color: #fff;'>🍴 Ingredients:</strong>
            <ul style='display: flex; list-style-type: none; padding-left: 0; flex-wrap: wrap; margin-top: 10px;'>
                {ingredients_html}
            </ul>
            <br/>
            <strong style='color: #fff;'>👨‍🍳 Cooking Steps:</strong>
            <ul style='margin-top: 10px;'>
                {recipe_html}
            </ul>
        </div>
    </details>
    """, unsafe_allow_html=True)      

def flow():
    take_input()
    if st.session_state.ingredients:
        manupulate_input()
        process_ingredients()
        

if 'ingredients' not in st.session_state:
    st.session_state.ingredients = []
    

    
if __name__ == "__main__":
    try :
        flow()
    except Exception as e:
        print(f"Main -> An error occurred: {e}")