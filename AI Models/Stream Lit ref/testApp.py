import streamlit as st

st.title('My Title')
st.text('Loading data...')
st.write("This is a test app to check if the Streamlit app is running correctly.")
st.subheader('Number of pickups by hour')


st.markdown(
    """
    <style>
    .title {
        font-size:40px;
        color:#4CAF50;
        text-align:center;
    }
    </style>
    """, unsafe_allow_html=True)


st.markdown('<div class="title">🌟 Welcome to Streamlit Demo App 🌟</div>', unsafe_allow_html=True)

st.sidebar.title("Navigation")
st.sidebar.success("Select a page above ⬆️ to explore features!")
st.sidebar.info("Tip: Use the slider to adjust the chart")
st.sidebar.warning("Don't forget to upload your file!")
st.sidebar.error("Missing required input")

sidebar_btn = st.sidebar.toggle("Click Me!")


if sidebar_btn:
    st.sidebar.success("Button clicked! 🎉")

st.image("sample.png", caption="Sample Image")

st.markdown("""
- 📝 Text and input widgets  
- 📈 Charts  
- 🎨 CSS styling  
- 🧭 Sidebar navigation  
- 📄 Multi-page support  
""")


st.text("----------------------------")

st.subheader("Text Elements")
st.text("This is st.text()")
st.markdown("**This is markdown**")
st.code("print('This is code')")

st.subheader("Input Widgets")
st.text_input("Text Input:")
st.text_area("Text Area:")
st.number_input("Number Input:")
st.date_input("Date Input:")
st.time_input("Time Input:")
st.file_uploader("Upload a file:")
st.color_picker("Pick a color:")
st.checkbox("I agree")
st.radio("Choose one", ["Option 1", "Option 2"])
st.selectbox("Select one", ["A", "B", "C"])
st.multiselect("Select multiple", ["X", "Y", "Z"])
st.slider("Slide something", 0, 100)
st.button("Click me!")


st.text("----------------------------")


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


st.title("📊 Chart Demonstration")

df = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])

st.subheader("Line Chart")
st.line_chart(df)

st.subheader("Area Chart")
st.area_chart(df)

st.subheader("Bar Chart")
st.bar_chart(df)

st.subheader("Matplotlib Chart")
fig, ax = plt.subplots()
ax.plot(df["A"], label="A")
ax.set_title("Matplotlib Line")
st.pyplot(fig)

st.subheader("Plotly Chart")
fig = px.line(df, x=df.index, y=["A", "B", "C"], title="Plotly Multi-line Chart")
st.plotly_chart(fig)


st.text("----------------------------")


st.title("🎨 CSS and Layout Customization")

st.markdown(
    """
    <style>
    .highlight {
        background-color: #ffeaa7;
        padding: 10px;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    <div class='highlight'>This is custom styled HTML content!</div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.success("This is Column 1")
    st.image("https://cdn1.epicgames.com/spt-assets/bec1ce3db2e44f21a7f18cc10efaaca9/carx-drift-racing-online-1ba3t.png")

with col2:
    st.info("This is Column 2")
    st.write("You can organize content side-by-side using `st.columns`")

st.markdown("---")
st.write("Use custom fonts, colors, and layout tweaks for beautiful apps.")