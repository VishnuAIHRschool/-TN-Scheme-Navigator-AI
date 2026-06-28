# 🏛️ TN Scheme Navigator AI

**TN Scheme Navigator AI** is a Gen AI RAG application built using **Streamlit, LangChain, OpenAI, ChromaDB, LangSmith, BeautifulSoup, and Python**.

The application helps users search, understand, and explore Tamil Nadu Government schemes through a simple AI-powered citizen-service interface.

---

## 🚀 Project Objective

The objective of this project is to build a professional AI-powered scheme discovery assistant for Tamil Nadu Government schemes.

The app allows users to ask natural language questions such as:

* What is the funding pattern for Training to Farmers?
* Who are the beneficiaries of Training to Farmers?
* How can farmers avail Training to Farmers scheme?
* Which schemes are related to seeds?
* Which schemes provide grants?
* Which schemes are useful for farmers, MSMEs, students, women, or entrepreneurs?

The AI assistant retrieves relevant scheme details and provides simple answers with official source links for verification.

---

## 🔗 Data Source

The application uses scheme information from the Tamil Nadu Government scheme portal:

```text
https://www.tn.gov.in/scheme_list.php?dep_id=Mg==
```

The current version focuses on:

```text
Agriculture - Farmers Welfare Department
```

---

## 🧠 Tech Stack

| Technology    | Purpose                                |
| ------------- | -------------------------------------- |
| Python        | Core programming language              |
| Streamlit     | Frontend web application               |
| LangChain     | RAG pipeline orchestration             |
| OpenAI        | LLM response generation and embeddings |
| ChromaDB      | Vector database for semantic search    |
| LangSmith     | Tracing, debugging, and observability  |
| BeautifulSoup | Web scraping                           |
| Requests      | Fetching web pages                     |
| Pandas        | CSV data handling                      |
| Python Dotenv | Environment variable management        |

---

## ✨ Key Features

* AI-powered Tamil Nadu scheme assistant
* Official scheme data scraping
* Scheme detail extraction
* CSV-based structured storage
* LangChain RAG workflow
* OpenAI embeddings
* ChromaDB vector search
* LangSmith tracing support
* Streamlit citizen-service UI
* Scheme Explorer page
* Department-wise and beneficiary-wise filtering
* Official source URL shown for verification
* Premium Tamil Nadu Government-inspired UI
* Agriculture-themed custom logo
* Clean sidebar navigation
* Scheme cards with badges
* Responsible AI disclaimer

---

## 🧾 How the Application Works

```text
Tamil Nadu Government Scheme Website
        ↓
Scrape Scheme List and Scheme Details
        ↓
Save Structured Data into CSV
        ↓
Convert Scheme Data into LangChain Documents
        ↓
Generate Embeddings using OpenAI
        ↓
Store Embeddings in ChromaDB
        ↓
User Asks Question in Streamlit
        ↓
LangChain Retriever Finds Relevant Scheme Data
        ↓
OpenAI Generates Answer using Retrieved Context
        ↓
App Displays Answer with Official Source Link
        ↓
LangSmith Tracks the Complete RAG Flow
```

---

## 🏗️ Project Architecture

```text
TN Scheme RAG/
│
├── app.py
│   └── Streamlit frontend application
│
├── scrape_schemes.py
│   └── Scrapes Tamil Nadu Government scheme list and detail pages
│
├── ingest.py
│   └── Converts CSV data into LangChain documents and stores embeddings in ChromaDB
│
├── rag_engine.py
│   └── Handles retrieval, context preparation, OpenAI response generation, and source references
│
├── requirements.txt
│   └── Python dependencies
│
├── .env
│   └── API keys and tracing environment variables
│
├── .gitignore
│   └── Files and folders excluded from GitHub
│
├── README.md
│   └── Project documentation
│
├── data/
│   └── tn_scheme_details.csv
│
└── vector_db/
    └── Local ChromaDB vector database
```

---

## ⚙️ Setup Instructions

### 1. Create Project Folder

```cmd
cd E:\
mkdir "TN Scheme RAG"
cd "TN Scheme RAG"
```

---

### 2. Create Virtual Environment

```cmd
python -m venv venv
```

Activate virtual environment:

```cmd
venv\Scripts\activate
```

---

### 3. Install Dependencies

Add the following packages in `requirements.txt`:

```txt
streamlit
python-dotenv
pandas
requests
beautifulsoup4
langchain
langchain-openai
langchain-chroma
chromadb
langsmith
```

Install dependencies:

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file and add:

```env
OPENAI_API_KEY=your_openai_api_key_here

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=TN-Scheme-Navigator-AI
```

Important:

* Do not upload `.env` to GitHub.
* Keep API keys private.
* LangSmith variables are used for tracing and debugging the LangChain RAG flow.

---

## 🚫 Git Ignore

Add this inside `.gitignore`:

```gitignore
venv/
.env
vector_db/
__pycache__/
*.pyc
```

---

## ▶️ How to Run the Project

### Step 1: Scrape Scheme Data

```cmd
python scrape_schemes.py
```

This creates:

```text
data/tn_scheme_details.csv
```

---

### Step 2: Create Vector Database

```cmd
python ingest.py
```

This creates the ChromaDB vector database inside:

```text
vector_db/
```

---

### Step 3: Launch Streamlit App

```cmd
streamlit run app.py
```

The app will open at:

```text
http://localhost:8501
```

---

## 💬 Sample Questions

```text
What is the funding pattern for Training to Farmers?
```

```text
Who are the beneficiaries of Training to Farmers?
```

```text
How can farmers avail Training to Farmers scheme?
```

```text
Which schemes are related to seeds?
```

```text
Which schemes provide grants?
```

```text
What schemes are useful for maize farmers?
```

---

## 🔍 LangSmith Tracing

LangSmith is used to trace and monitor the LangChain RAG workflow.

It helps track:

* User question
* Retriever call
* Retrieved scheme documents
* Prompt/context sent to OpenAI
* Final AI response
* Latency
* Errors
* Debugging information

### Tracing Flow

```text
User Question
        ↓
LangChain RAG Engine
        ↓
ChromaDB Retriever
        ↓
Retrieved Scheme Documents
        ↓
OpenAI LLM
        ↓
Generated Answer
        ↓
LangSmith Trace Dashboard
```

This improves observability and makes the Gen AI application easier to debug, evaluate, and improve.

---

## 🎨 UI/UX Improvements

The app UI was upgraded to look like a premium Tamil Nadu Government AI citizen-service portal.

UI improvements include:

* Deep navy blue government-style theme
* Government green secondary color
* Gold/saffron accent color
* Agriculture-inspired custom logo
* Professional sidebar
* Larger navigation menu
* Premium active navigation pill
* Bigger portal title
* Clean hero section
* White cards with soft shadows
* Better typography
* Clear input field visibility
* Professional loading state
* AI answer response card
* Scheme cards with badges
* Footer with responsible AI disclaimer

---

## 🧩 Application Pages

### 1. Home

Shows the portal introduction, feature cards, statistics, and high-level RAG workflow.

### 2. AI Scheme Assistant

Allows users to ask natural language questions and receive AI-generated answers based on retrieved scheme data.

### 3. Scheme Explorer

Allows users to search and filter scheme records by department, beneficiary, and benefit type.

### 4. About

Explains the purpose, technology stack, and responsible AI usage.

---

## ✅ GitHub Submission Steps

Initialize Git:

```cmd
git init
```

Add files:

```cmd
git add .
```

Commit:

```cmd
git commit -m "Initial commit - TN Scheme Navigator AI"
```

Add remote repository:

```cmd
git remote add origin https://github.com/VishnuAIHRschool/-TN-Scheme-Navigator-AI.git
```

If remote already exists:

```cmd
git remote set-url origin https://github.com/VishnuAIHRschool/-TN-Scheme-Navigator-AI.git
```

Push to GitHub:

```cmd
git branch -M main
git push -u origin main
```

---

## ⚠️ Responsible AI Disclaimer

This AI assistant is for informational support only.

Users should verify final scheme details such as eligibility, subsidy amount, funding pattern, documents required, application process, and scheme validity from the official Tamil Nadu Government website before taking action.

---

## 🔮 Future Enhancements

* Tamil language support
* Voice-based scheme search
* Multi-department scheme crawling
* MSME, Education, Health, Welfare, and Women Development scheme data
* Eligibility checker form
* Scheme recommendation engine
* PDF download of AI answers
* Admin refresh button
* User login
* Chat history
* Analytics dashboard
* Deployment to Streamlit Cloud

---

## 👨‍💻 Developed By

**Vishnukumar**
Gen AI Application using Streamlit, LangChain, OpenAI, ChromaDB, LangSmith, and RAG.

---

## One-Line Summary

**TN Scheme Navigator AI converts Tamil Nadu Government scheme information into an AI-searchable knowledge base and helps users discover scheme details through natural language questions with official source verification.**
