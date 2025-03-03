import os
import json
import google.generativeai as genai
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Load knowledge base
def load_knowledge_base():
    try:
        with open('knowledge/kb.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        return []

knowledge_base = load_knowledge_base()

# Function to find relevant documents using keyword matching
def retrieve_relevant_info(query):
    query_terms = [term.lower() for term in query.split() if len(term) > 3]
    
    # Score each document based on term matches
    scored_docs = []
    for doc in knowledge_base:
        doc_content = doc['content'].lower()
        score = 0
        
        for term in query_terms:
            if term in doc_content:
                score += 1
        
        if score > 0:
            scored_docs.append({
                'content': doc['content'],
                'score': score
            })
    
    # Sort by score and take top 2 results
    relevant_docs = sorted(scored_docs, key=lambda x: x['score'], reverse=True)[:2]
    return [doc['content'] for doc in relevant_docs]

# Function to query Gemini API with RAG enhancement
def query_gemini_with_rag(user_query):
    # Retrieve relevant information
    retrieved_info = retrieve_relevant_info(user_query)
    
    # Construct a prompt that includes the retrieved information
    if retrieved_info:
        enhanced_prompt = f"""
I want you to answer the following question using the provided context information.
If the context doesn't contain relevant information, just use your general knowledge.

Context information:
{(chr(10) + chr(10)).join(retrieved_info)}

User question: {user_query}
        """
    else:
        enhanced_prompt = user_query
    
    # Query the Gemini API
    try:
        response = model.generate_content(enhanced_prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return f"Error: {str(e)}"

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            response = query_gemini_with_rag(query)
            return render_template('index.html', query=query, response=response)
    
    return render_template('index.html')

# Main
if __name__ == '__main__':
    app.run(debug=True)
