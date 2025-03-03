# RAG-DEMO
GDC Workshop Demo Template


```markdown
# Gemini RAG Demo

A simple Flask application demonstrating Retrieval-Augmented Generation (RAG) with Google's Gemini API.

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/gemini-rag-demo.git
cd gemini-rag-demo
```

### Step 2: Set Up Virtual Environment

Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

Install the required packages:
```bash
pip install flask python-dotenv google-generativeai
```

### Step 4: Set Up API Key

1. Get a Gemini API key from [Google AI Studio](https://ai.google.dev/)
2. Create a `.env` file in the root directory (or edit the existing one):
3. Add your API key to the `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

### Step 5: Run the Application

Make sure your virtual environment is activated, then run the application:
```bash
# Run the application
python app.py
```

The application will start and be accessible at http://127.0.0.1:5000 in your web browser.

## Using the Application

1. Open your browser and go to http://127.0.0.1:5000
2. Type a question in the text area, such as "Tell me about Git basics" or "What is RAG?"
3. Click "Get Answer" to see the response

## Demo Questions to Try

- "What are the basic Git commands?"
- "Explain client-server architecture"
- "How does RAG work?"
- "What certifications should I pursue?"
- "How do I prepare for tech internships?"

## Project Structure

```
gemini-rag-demo/
├── app.py                 # Main application file
├── knowledge/
│   └── kb.json            # Knowledge base data
├── static/
│   └── style.css          # CSS styling
├── templates/
│   └── index.html         # HTML template
├── .env                   # Environment variables (you need to create this)
└── README.md              # This readme file
```

## How It Works

This application demonstrates a simple implementation of Retrieval-Augmented Generation (RAG):

1. When a user submits a question, the system searches the knowledge base (`knowledge/kb.json`) for relevant information.
2. The search uses simple keyword matching to find the most relevant documents.
3. The retrieved information is included in the prompt sent to the Gemini API.
4. This contextual information helps the model provide more accurate and specific responses.

## Extending the Application

Some ways you could enhance this demo:
- Add more documents to the knowledge base
- Implement more sophisticated retrieval algorithms
- Add user authentication
- Deploy the application to a cloud platform

## Troubleshooting

- **API Key Issues**: Make sure your API key is correct and properly set in the `.env` file
- **Module Not Found Errors**: Ensure all dependencies are installed with `pip install flask python-dotenv google-generativeai`
- **Permission Denied**: If you can't write to the `.env` file, check your file permissions
```
