import os
import json
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def preprocess(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        tokens = nltk.word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words]
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        processed_text = ' '.join(tokens)
        return processed_text


class RAGSystem:
    def __init__(self):
        self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')

        self.pc = Pinecone(api_key=self.pinecone_api_key)
        
        genai.configure(api_key=self.gemini_api_key)
        self.generation_model = genai.GenerativeModel('gemini-pro')

        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')


        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=750,
            chunk_overlap=100,
            length_function=len
        )
        
        self.preprocessor = TextPreprocessor()

    def load_documents(self, directory: str) -> List[Dict]:
        documents = []
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    processed_content = self.preprocessor.preprocess(content)
                    documents.append({
                        'filename': filename,
                        'content': processed_content
                    })
        return documents

    def prepare_embeddings(self, documents: List[Dict]) -> List[Dict]:
        prepared_docs = []
        for doc in documents:
            processed_text = self.preprocessor.preprocess(doc['content'])
            chunks = self.text_splitter.split_text(processed_text)
            for i, chunk in enumerate(chunks):
                embedding = self.embedding_model.encode(chunk).tolist()
                prepared_docs.append({
                    'id': f"{doc['filename']}_{i}",
                    'text': chunk,
                    'embedding': embedding
                })
        return prepared_docs

    def create_pinecone_index(self, index_name: str):
        existing_indexes = self.pc.list_indexes().names()
        if index_name not in existing_indexes:
            self.pc.create_index(
                name=index_name, 
                dimension=384,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
        self.index = self.pc.Index(index_name)

    def upsert_embeddings(self, prepared_docs: List[Dict]):
        vectors = [
            {
                'id': doc['id'], 
                'values': doc['embedding'], 
                'metadata': {'text': doc['text']}
            } 
            for doc in prepared_docs
        ]
        
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            self.index.upsert(batch)

    def retrieve_relevant_context(self, query: str, top_k: int = 3) -> List[str]:
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.index.query(
            vector=query_embedding, 
            top_k=top_k, 
            include_metadata=True
        )
        contexts = [
            match['metadata']['text'] 
            for match in results['matches']
        ]
        return contexts

    def generate_response(self, query: str, contexts: List[str]) -> str:
        prompt = f"""Context:
{' '.join(contexts)}

Query: {query}
You are a financial advisor with expertise in tax planning and investment strategies. Use the above context and the query below to provide an actionable, personalized response."""

            
        response = self.generation_model.generate_content(prompt)
        return response.text

    def process_rag(self, query: str) -> str:
        contexts = self.retrieve_relevant_context(query)
        response = self.generate_response(query, contexts)
        return response

def main():
    rag_system = RAGSystem()
    documents = rag_system.load_documents('files')
    prepared_docs = rag_system.prepare_embeddings(documents)
    rag_system.create_pinecone_index('document-index')
    rag_system.upsert_embeddings(prepared_docs)
    query = (
        "I am a middle-class man in India earning ₹1 lakh per month after tax. "
        "Please act as a chartered accountant and provide the following: "
        "1. Tips to improve my tax filing methods. "
        "2. Suggestions on how to optimize the Indian tax system legally to save more. "
        "3. Investment ideas for tax-saving and wealth growth, including mutual funds, real estate, or insurance. "
        "4. Any other financial advice relevant to my income and tax situation."
    )
    response = rag_system.process_rag(query)
    print(response)
    

if __name__ == '__main__':
    main()
