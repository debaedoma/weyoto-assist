import os
import openai

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY_WEYOTO_ASSIST_Coder")

if not openai.api_key:
    raise ValueError("OpenAI API Key is missing. Please set the environment variable 'OPENAI_API_KEY_WEYOTO_ASSIST'.")
import faiss
import numpy as np

from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize FAISS Vector Store
vector_dim = 512
index = faiss.IndexFlatL2(vector_dim)
documents = []  # Stores filenames corresponding to vectors

# File extensions to index
ALLOWED_EXTENSIONS = {".py", ".txt", ".md", ".toml", ".ini", ".cfg", ".conf", ".env", ".gitignore", "Dockerfile"}


# Function to Generate Embeddings
def generate_embedding(text):
    try:
        response = openai.embeddings.create(input=[text], model="text-embedding-ada-002")
        return np.array(response.data[0].embedding)
    except openai.OpenAIError as e:  # Correctly handle OpenAI API errors
        print(f"OpenAI API error: {e}")
        return np.zeros(512)  # Return a zero-vector as a fallback


# Index Codebase into FAISS (Now Includes Config & Dependencies)
@app.route('/index-code', methods=['POST'])
def index_code():
    folder_path = request.json.get("folder_path", "./")  # Default to current directory
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_ext = os.path.splitext(filename)[1]
            if file_ext in ALLOWED_EXTENSIONS or filename in ALLOWED_EXTENSIONS:  # Handle extensions and special files
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    embedding = generate_embedding(content)
                    index.add(np.array([embedding], dtype=np.float32))
                    documents.append(file_path)  # Store full paths

    return jsonify({"message": "Codebase and configs indexed successfully", "indexed_files": len(documents)})


# Query Codebase
@app.route('/query-code', methods=['GET'])
def query_code():
    query = request.args.get('query', '').lower()
    query_embedding = generate_embedding(query)
    D, I = index.search(np.array([query_embedding], dtype=np.float32), k=5)
    relevant_files = [documents[i] for i in I[0] if i < len(documents) and i >= 0 and not documents[i].endswith(
        ('.gitignore', '.env', 'requirements.txt'))]

    # Extract content from relevant files
    extracted_code = ""
    for file_path in relevant_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                extracted_code += f"\n### {file_path} ###\n" + file.read(1000)  # Properly formatted f-string
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

    # Generate an AI-powered response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are an AI assistant helping with coding questions. Provide relevant explanations and solutions based on the provided code snippets."},
                {"role": "user", "content": f"Question: {query}\n\nRelevant Code:\n{extracted_code}"}
            ]
        )
        ai_response = response["choices"][0]["message"]["content"]
    except openai.OpenAIError as e:
        ai_response = f"AI response failed: {e}"

    return jsonify({"results": relevant_files, "ai_response": ai_response})


if __name__ == '__main__':
    app.run(debug=True)
