import streamlit as st
import streamlit.components.v1 as components


from PIL import Image
import base64
import os


from dotenv import load_dotenv

# Import models from LangChain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import google.generativeai as genai

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
text_model = genai.GenerativeModel("gemini-pro")
vision_model = genai.GenerativeModel("gemini-pro-vision")

# Title
st.title("👨‍🍳 AI Chef: Cook with What You Have")

# Run JS camera permission check
with open("AI_chef/check_permissions.html", 'r') as f:
    html_string = f.read()

components.html(html_string, height=0)  # height=0 to hide iframe

# Step 1: Capture image from camera
image = st.camera_input("Click a photo of your cooking ingredients")

if image:
    st.image(image, caption="Uploaded Ingredients", use_column_width=True)

    with st.spinner("🔍 Identifying ingredients..."):
        img = Image.open(image)
        buffered = base64.b64encode(image.getvalue()).decode("utf-8")

        prompt_vision = """
        You are an experienced Indian chef. From this image, identify only cooking vegetable or food items (avoid background, utensils, packet labels).
        Return ingredients in simple, comma-separated list.
        """

        vision_response = vision_model.generate_content(
            [prompt_vision, img],
            stream=False,
        )

        identified_items = vision_response.text.strip()
        st.success("✅ Identified Ingredients:")
        st.markdown(f"**{identified_items}**")

        # Step 2: Suggest dishes
        st.divider()
        st.subheader("🍽️ Suggested Indian Dishes")

        with st.spinner("🍛 Thinking of tasty dishes..."):
            dish_prompt = f"""
You are an expert Indian chef. Based on the items: {identified_items}, suggest 5–10 Indian dishes.

Rules:
- Output format: numbered list
- Mention the dish category (snack, curry, rice, etc.)
- Suggest 2–3 extra common items if needed per dish (like onion, salt, oil)
- Prefer minimal ingredients if possible
"""
            text_response = text_model.generate_content(dish_prompt)
            dishes_text = text_response.text.strip()
            st.markdown(dishes_text)

            # Extract dishes
            dish_lines = [line.strip() for line in dishes_text.split("\n") if line.strip() and line[0].isdigit()]
            selected_dish = st.radio("Which dish do you want to cook?", dish_lines)

            if st.button("👨‍🍳 Let's Select This"):
                with st.spinner("📝 Fetching recipe..."):
                    recipe_prompt = f"""
You are an Indian chef. Share a recipe for "{selected_dish}" including:
- Required ingredients
- Cooking steps
- Tips if any
- Estimated time
- Number of servings
"""
                    recipe_response = text_model.generate_content(recipe_prompt)
                    recipe = recipe_response.text.strip()
                    st.success(f"📃 Recipe for: {selected_dish}")
                    st.markdown(recipe)
else:
    st.info("If your camera doesn't appear, check that you've granted permission in your browser settings.")