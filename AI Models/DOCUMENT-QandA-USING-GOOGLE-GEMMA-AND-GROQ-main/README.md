# Gemma Model Document Q\&A

This is a Streamlit web app that allows users to **ask questions based on PDF documents** using the **Gemma model** from Groq and **Google Generative AI embeddings**.

## What does it do?

* Loads PDF files from a folder.
* Splits the documents into chunks.
* Converts the chunks into vectors using **Google's Embedding model**.
* Stores the vectors in a **FAISS** vector database.
* Uses **LangChain** to create a **retrieval-based question answering system**.
* Answers user questions using **context from the uploaded PDFs**.

## Technologies Used

* **Streamlit** – for the web interface
* **LangChain** – for document loading, splitting, and Q\&A chain
* **Groq** – to access the **Gemma2-9b-it** model
* **Google Generative AI** – for text embeddings
* **FAISS** – for vector storage and similarity search
* **dotenv** – to manage API keys securely
* **PyPDFDirectoryLoader** – to load all PDFs from a directory

## How to Run the App

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/gemma-pdf-qa.git
   cd gemma-pdf-qa
   ```

2. **Install dependencies**

   ```cmd
   pip install -r requirements.txt
   ```

3. **Add your API keys** to a `.env` file in the root directory:

   ```
   GROQ_API_KEY=your_groq_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

4. **Add PDF files** to a folder named `us_census` in the project directory.

5. **Run the app**

   ```cmd
   streamlit run app.py
   ```

## App Flow

1. **Click “Create Vector Store”** – This processes and stores document vectors.
2. **Ask a question** in the input field.
3. **Get an accurate answer** based on the content of the documents.

## Example Use Cases

* Ask questions about uploaded government reports.
* Interact with lengthy research papers easily.
* Extract answers from census or policy documents.


## Note

* Make sure your `.env` file is not pushed to GitHub.
* The app uses the `Gemma2-9b-it` model, which should be supported by your Groq account.
