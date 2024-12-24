# 📚 RAG-Based Financial Advisor System with Pinecone and Gemini Integration

This project is a **Retrieval-Augmented Generation (RAG)** system that provides actionable financial advice by combining document embeddings stored in a **Pinecone index** and the **Gemini Generative AI** model for generating personalized responses.

---

## 🔧 Features

1. **Text Preprocessing**:
   - Removes punctuation and numbers.
   - Tokenizes and lemmatizes text.
   - Removes stopwords to ensure high-quality embeddings.

2. **Embedding Preparation**:
   - Splits documents into smaller chunks using **RecursiveCharacterTextSplitter**.
   - Encodes text chunks into embeddings using **SentenceTransformer**.

3. **Pinecone Integration**:
   - Creates and manages a **Pinecone** index for storing and querying document embeddings.

4. **Generative AI**:
   - Generates personalized responses using the **Gemini Generative AI** model.

5. **Financial Expertise**:
   - Acts as a **financial advisor** with expertise in tax planning and investment strategies.

---

## 📂 Project Structure

```
.
├── main.py                  # Main script to run the RAG system
├── files                    # Directory containing input documents
├── README.md                # Project documentation
├── webscraper               # A helper function;simple implementation of the webscraper
├── webcrawler               # A simple inplementation of the webcrawler to to help collecting data
└── requirements.txt         # Python dependencies

```

---

## 📝 How It Works

1. **Load and Preprocess Documents**:
   - Reads `.txt` files from the `files/` directory.
   - Preprocesses text using `TextPreprocessor`.

2. **Prepare and Store Embeddings**:
   - Splits preprocessed text into smaller chunks.
   - Generates embeddings using `SentenceTransformer`.
   - Stores embeddings in a Pinecone index.

3. **Query Processing**:
   - Accepts a user query and retrieves relevant contexts from the Pinecone index.
   - Combines the query with retrieved contexts to generate a response using Gemini Generative AI.

4. **Financial Advice**:
   - Provides tailored financial recommendations based on the query and retrieved contexts.

---

## 🔧 Requirements

Install the required dependencies using:

```bash
pip install -r requirements.txt
```
---

## 🚀 How to Run

1. **Set Up API Keys**:
   - Add your Pinecone and Gemini API keys as environment variables:
     ```bash
     export PINECONE_API_KEY=<your_pinecone_api_key>
     export GEMINI_API_KEY=<your_gemini_api_key>
     ```

2. **Prepare Documents**:
   - Place `.txt` files in the `files/` directory.

3. **Run the Script**:
   ```bash
   python main.py
   ```
4. **Output**:
   - The system generates personalized financial advice tailored to the query.
   - ![WhatsApp Image 2024-12-14 at 00 19 55_067e867c](https://github.com/user-attachments/assets/56436a3b-a265-4868-88ca-45e8f27e8f0c)
---

### 🌟 **Show Your Support**
If you find this project helpful, give it a ⭐ on GitHub and share it with others! 😊


