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
model = genai.GenerativeModel('gemini-2.0-flash')

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
    # Normalize the query - remove hyphens, lowercase, etc.
    normalized_query = query.lower().replace('-', ' ').replace('_', ' ')
    query_terms = [term for term in normalized_query.split() if len(term) > 2]
    
    print(f"Query terms: {query_terms}")  # Debugging
    
    # Score each document based on term matches and also check IDs
    scored_docs = []
    for doc in knowledge_base:
        doc_content = doc['content'].lower()
        doc_id = doc['id'].lower().replace('-', ' ').replace('_', ' ')
        score = 0
        
        # Check if any query term is in the document ID
        for term in query_terms:
            if term in doc_id.split():
                score += 3  # Give higher score for ID matches
            if term in doc_content:
                score += 1
        
        # Also check exact ID match
        if normalized_query in doc_id:
            score += 5
            
        if "git" in query_terms and "git" in doc_id:
            score += 2  # Special case for git-related queries
            
        print(f"Doc ID: {doc['id']}, Score: {score}")  # Debugging
        
        if score > 0:
            scored_docs.append({
                'content': doc['content'],
                'id': doc['id'],
                'score': score
            })
    
    # Sorting by score and take top 2 results
    relevant_docs = sorted(scored_docs, key=lambda x: x['score'], reverse=True)[:2]
    return [f"[{doc['id']}]: {doc['content']}" for doc in relevant_docs]

# Function to query Gemini API with RAG enhancement

def query_gemini_with_rag(user_query):
    # Retrieve relevant information
    retrieved_info = retrieve_relevant_info(user_query)
    
    # Constructing a prompt that includes the retrieved information
    if retrieved_info:
        enhanced_prompt = f"""
I want you to answer the following question using the provided context information.
If the context doesn't contain relevant information, just use your general knowledge.

Context information:
{(chr(10) + chr(10)).join(retrieved_info)}

User question: {user_query}
        """
        
        # Formatting the response to show what knowledge was used
        response_with_sources = f"""
Based on our knowledge base, I found these relevant pieces of information:

---
{(chr(10) + chr(10)).join(retrieved_info)}
---

Here's your answer:

"""
        try:
            response = model.generate_content(enhanced_prompt)
            return response_with_sources + response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return f"Error: {str(e)}"
    else:
        try:
            response = model.generate_content(user_query)
            return "No specific information found in our knowledge base. Here's a general answer:\n\n" + response.text
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
