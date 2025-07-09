# MiniVault API

A lightweight and secure API for managing secrets or credentials, built with [FastAPI/React].

---


## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/pritam1322/MiniVault-API.git
cd MiniVault-API
```
### 2. Install Dependencies
```bash
cd minivault-api
pip install -r requirements.txt
cd ..
cd frontend
npm install
```

### 3. Run the API Server
```bash
uvicorn main:app --reload
```

### 4. Notes / Tradeoffs (MiniVault-API)
- [x] **Hugging Face Transformers for Text Generation**  
  The backend integrates Hugging Face models to generate natural language responses based on user prompts.

- [x] **FastAPI for Scalable Backend APIs**  
  FastAPI is used to expose high-performance REST endpoints for model inference, with automatic documentation and async support.

- [x] **React Frontend for User Interaction**  
  A clean and responsive React-based UI allows users to input prompts and view generated text in real time.


## 🧪 Testing - CLI
Format : python cli.py "prompt" --model phi --stream
```bash
python cli.py "Tell me a joke" --model phi --stream
```


