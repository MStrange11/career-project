from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, load_prompt

from dotenv import load_dotenv
import streamlit as st

load_dotenv()

st.header("Static Prompt vs Dynamic Prompt")

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

c1, c2 = st.columns(2,gap="large")

with c1:
    # Static prompt UI
    st.header("Research Tool")
    prompt = st.text_input("Enter your question here:")






# In static prompt, the user will enter the prompt but the chance of error is high.
# to overcome this, we can create a dynamic prompt where the user can enter the question and the model will generate the answer.



# Dynamic prompt UI

template = PromptTemplate(
    template="""
    Please summarize the research paper titled "{paper_input}" with the following
    specifications:
    Explanation Style: {style_input}
    Explanation Length: {length_input}
    1. Mathematical Details:
    - Include relevant mathematical equations if present in the paper.
    - Explain the mathematical concepts using simple, intuitive code snippets
    where applicable.
    2. Analogies:
    Use relatable analogies to simplify complex ideas.
    If certain information is not available in the paper, respond with: "Insufficient
    information available" instead of guessing.
    Ensure the summary is clear, accurate, and aligned with the provided style and
    length.
    """,
    input_variables=["paper_input", "style_input", "length_input"]
)

with c2:

    st.header("Research Tool with Dynamic Prompt")
    paper_input = st.selectbox("Select Research Paper Name", ["Attention Is All You Need","BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis"])

    style_input = st.selectbox("Select Explanation Style", ["Beginner-friendly", "Technical","code-oriented", "Mathematical"])

    length_input = st.selectbox("Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"])

    prompt = template.invoke(
        {'paper_input': paper_input,
        'style_input': style_input,
        'length_input': length_input}
    )

if st.button("summarize" , ):
    res = model.invoke(prompt)
    st.write(res.content)