from flask import Flask, send_from_directory, request, jsonify
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
import os

# Initialize Flask app
app = Flask(__name__, static_url_path='', static_folder='')

# Environment Variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
VECSTORE_PATH = "vector_store"

# Homepage route
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Serve static CSS files
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

# Serve static JavaScript files
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

# Serve other static files (images, fonts, etc.)
@app.route('/<path:path>')
def serve_static_files(path):
    if path.startswith("images/"):
        return send_from_directory('images', path[len("images/"):])
    elif path.startswith("fonts/"):
        return send_from_directory('fonts', path[len("fonts/"):])
    else:
        return send_from_directory('.', path)

# Chatbot API
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    try:
        response, sources = Generate_response(query)
        return jsonify({'response': response, 'sources': sources})
    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

# Serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('images', 'favicon.ico')

# Embedding function
def embed_query(query_text: str):
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    query_embedding = embedding_function.embed_query(query_text)
    return query_embedding

# Search for context
def search_store_for_context(embedded_query, k):
    vector_store = Chroma(
        persist_directory=VECSTORE_PATH,
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
    )
    results = vector_store.similarity_search_by_vector(embedded_query, k=k)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    sources = [
        f"Source: {doc.metadata.get('source', 'Unknown source')}, Page: {doc.metadata.get('page', 'Unknown page') + 1}"
        for doc in results
    ]
    return context_text, sources

# Generate response with LLM
def generate_llm_prompt(context_text: str, query_text: str):
    PROMPT_TEMPLATE = """
    Answer the question as if you were me, based only and uniquely on the following context:

    {context}

    ---

    Question: {question}
    """
    return PROMPT_TEMPLATE.format(context=context_text, question=query_text)

def generate_response_with_llm(prompt: str):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, max_tokens=50)
    response = llm.invoke(prompt)
    return response.content

def Generate_response(query_text):
    embedded_query = embed_query(query_text)
    context_text, sources = search_store_for_context(embedded_query, k=2)
    generated_prompt = generate_llm_prompt(context_text, query_text)
    response = generate_response_with_llm(generated_prompt)
    formatted_response = f"{response}\n Sources: {sources}"
    print(formatted_response)
    return response, sources

if __name__ == '__main__':
    app.run()
