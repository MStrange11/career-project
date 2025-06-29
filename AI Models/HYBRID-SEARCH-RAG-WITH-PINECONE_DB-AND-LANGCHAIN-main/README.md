# Pinecone Hybrid Search Project

This project shows how to use **Pinecone** for hybrid search combining **semantic** and **syntactic (keyword-based)** search.

## What This Project Does

* Converts sentences into **vectors** using HuggingFace.
* Uses **BM25 (TF-IDF)** to capture keyword-based features.
* Stores both vector and sparse data in a **Pinecone index**.
* Performs **hybrid search** that combines:

  * **Semantic search** → understands meaning
  * **Syntactic search** → matches exact keywords

## Tools Used

* **Pinecone** – Vector database
* **Langchain** – Connects components
* **HuggingFace Embeddings** – Semantic meaning
* **BM25Encoder** – Syntactic/keyword matching
* **dotenv** – Loads API keys securely`

## Setup

1. Add your Pinecone API key to a `.env` file:

   ```.env
   PINECONE_API_KEY=your_key_here
   ```

2. Install required libraries:

   ```cmd
   pip install -r requirements.txt
   ```

## How It Works

* Text data is converted to:

  * **Dense vectors** (for semantic meaning)
  * **Sparse vectors** (for syntactic matching)
* Stored in Pinecone
* Supports **hybrid retrieval** of results using both techniques

You can ask:
```
which city did I visit last time
```
And it retrieves the most relevant result.

## Output
The retriever gives accurate results using:
* Semantic search (understands context)
* Syntactic search (matches exact words)

## Summary

This project builds a smart hybrid search system using AI, capable of understanding both **what you mean** and **what you say exactly**.
