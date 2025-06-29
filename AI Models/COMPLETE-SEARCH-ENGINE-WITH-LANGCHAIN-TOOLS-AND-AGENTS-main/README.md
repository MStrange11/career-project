# Searching Engine With Langchain Tools And Agents

This is a chatbot application built using **Streamlit** and **Langchain**. It uses web search tools like **Wikipedia**, **Arxiv**, and **DuckDuckGo** to answer your questions with the help of a large language model (LLaMA3) from Groq.


## Features

* Chat interface created using Streamlit
* Uses Wikipedia, Arxiv, and DuckDuckGo to search for information
* Powered by Langchain's ChatGroq with the LLaMA3-8b model
* Allows you to enter your Groq API key securely
* Uses an agent to decide which tool to use based on your question


## Requirements

* Python 3.8 or higher
* Required libraries:

  * streamlit
  * langchain
  * langchain-community
  * langchain-groq
  * python-dotenv

Install the libraries using pip:

```
pip install streamlit langchain langchain-community langchain-groq python-dotenv
```


## Setup

1. Clone this repository or copy the Python file.
2. Create a `.env` file in the same directory with the following content:

```
GROQ_API_KEY=your_groq_api_key_here
```

You can also enter the API key manually in the sidebar when running the app.


## How to Run

Use the following command in your terminal:

```
streamlit run your_script_name.py
```

Replace `your_script_name.py` with the actual name of your Python file.


## How to Use

1. Open the Streamlit app.
2. Enter your Groq API key in the sidebar.
3. Type your question in the chat input box, such as:

   * What is machine learning?
   * Show recent research on artificial intelligence.
   * Who discovered gravity?

The chatbot will search online and give you an answer.


## How It Works

* The app uses three tools: Wikipedia, Arxiv, and DuckDuckGo.
* These tools are managed using a Langchain Agent.
* The agent decides which tool(s) to use based on your question.
* The chatbot responds using results from the tools and the LLM.


## Notes

* Make sure you have a valid Groq API key.
* The chatbot supports only text-based questions.
