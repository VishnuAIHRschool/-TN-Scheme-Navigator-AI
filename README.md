# TN Scheme Navigator AI  
## AI-Powered Tamil Nadu Government Scheme Assistant with Hybrid Graph RAG

TN Scheme Navigator AI is a next-generation AI application that helps users search, understand, and verify Tamil Nadu Government scheme information.

The application uses **Vector RAG**, **Knowledge Graph RAG**, and **Hybrid AI Routing** to answer scheme-related questions in **English, Tamil, or Bilingual format**.

---

## Project Objective

The objective of this project is to build a citizen-friendly AI assistant that can:

- Search Tamil Nadu Government scheme data
- Explain schemes in simple language
- Answer questions in English and Tamil
- Retrieve relevant scheme details using Vector RAG
- Understand relationships using Neo4j Knowledge Graph
- Provide official source references for verification

---

## Live Use Case

A user can ask:

```text
Which schemes are available for farmers?
Which schemes are sponsored by State?
Which schemes provide subsidy benefits?
விவசாயிகளுக்கான மானிய திட்டங்கள் எவை?

The app retrieves relevant scheme data and generates a clear AI answer.

Key Features
Streamlit-based modern web application
AI-powered scheme question answering
ChromaDB Vector RAG for semantic search
Neo4j AuraDB Knowledge Graph for relationship-based reasoning
NetworkX graph preview and graph analysis
Tamil, English, and Bilingual response support
Smart Hybrid RAG routing
Official scheme source references
Scheme Explorer with filters
Production-style UI with improved navigation and answer layout
LangSmith tracing support
Technology Stack
Area	Technology
Frontend	Streamlit
AI Orchestration	LangChain
LLM	OpenAI
Vector Database	ChromaDB
Embeddings	OpenAI Embeddings
Knowledge Graph	Neo4j AuraDB
Graph Query	Cypher
Graph Analysis	NetworkX
Data Collection	Requests, BeautifulSoup
Data Handling	Pandas
Observability	LangSmith
Environment Management	python-dotenv
System Architecture
Tamil Nadu Scheme Website
        ↓
scrape_schemes.py
        ↓
data/tn_scheme_details.csv
        ↓
        ├── ingest.py
        │       ↓
        │   ChromaDB Vector Database
        │
        ├── load_graph_to_neo4j.py
        │       ↓
        │   Neo4j AuraDB Knowledge Graph
        │
        └── networkx_graph_preview.py
                ↓
            NetworkX Graph Preview

User Question
        ↓
Streamlit App
        ↓
Hybrid RAG Engine
        ↓
Vector RAG + Graph RAG
        ↓
OpenAI Final Answer
        ↓
Answer with Official References
How the App Works
1. Data Collection

The app scrapes Tamil Nadu Government scheme data from the official government website and stores it as a structured CSV file.

data/tn_scheme_details.csv
2. Vector RAG Layer

The CSV data is converted into documents.

Then OpenAI embeddings are generated and stored in ChromaDB.

This helps the app answer meaning-based questions.

Example:

What schemes are available for farmers?
3. Knowledge Graph Layer

The same scheme data is loaded into Neo4j AuraDB as a graph.

The graph contains nodes such as:

Scheme
Department
Beneficiary
Benefit Type
Sponsor
Keyword

Relationships include:

Scheme → BELONGS_TO → Department
Scheme → FOR_BENEFICIARY → Beneficiary
Scheme → PROVIDES_BENEFIT → Benefit Type
Scheme → SPONSORED_BY → Sponsor
Scheme → HAS_KEYWORD → Keyword

This helps the app answer relationship-based questions.

Example:

Which schemes are sponsored by State?
4. Hybrid RAG Layer

The Hybrid RAG engine combines:

ChromaDB Vector RAG
+
Neo4j Knowledge Graph RAG
+
OpenAI Final Response

This allows the app to provide richer, more accurate answers.

5. Tamil and Bilingual Support

The app supports:

English
Tamil
Bilingual

Users can ask questions in Tamil and receive citizen-friendly Tamil responses.

Project Folder Structure
TN Scheme RAG/
│
├── app.py
├── scrape_schemes.py
├── ingest.py
├── rag_engine.py
├── graph_rag_engine.py
├── hybrid_rag_engine.py
├── language_utils.py
├── load_graph_to_neo4j.py
├── networkx_graph_preview.py
│
├── test_neo4j_connection.py
├── test_neo4j_query.py
├── test_graph_rag.py
├── test_hybrid_rag.py
├── test_next_level_hybrid.py
│
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── data/
│   ├── tn_scheme_details.csv
│   └── knowledge_graph_preview.png
│
├── vector_db/
│
└── venv/
Important Files
File	Purpose
app.py	Main Streamlit frontend application
scrape_schemes.py	Scrapes Tamil Nadu scheme data
ingest.py	Creates embeddings and stores data in ChromaDB
rag_engine.py	Existing Vector RAG engine
graph_rag_engine.py	Neo4j Graph RAG engine
hybrid_rag_engine.py	Combines Vector RAG and Graph RAG
language_utils.py	Tamil, English, and Bilingual language helpers
load_graph_to_neo4j.py	Loads CSV data into Neo4j AuraDB
networkx_graph_preview.py	Creates local graph preview using NetworkX
requirements.txt	Python dependencies
.env	API keys and credentials, not pushed to GitHub
.gitignore	Prevents sensitive and unnecessary files from being pushed
Environment Variables

Create a .env file in the project root.

OPENAI_API_KEY=your_openai_api_key_here

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=TN-Scheme-Navigator-AI

NEO4J_URI=neo4j+s://your-aura-uri.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password_here
NEO4J_DATABASE=neo4j

Do not push .env to GitHub.

Installation
1. Clone the repository
git clone https://github.com/VishnuAIHRschool/-TN-Scheme-Navigator-AI.git
2. Go to project folder
cd "-TN-Scheme-Navigator-AI"
3. Create virtual environment
python -m venv venv
4. Activate virtual environment
venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
Requirements
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
neo4j
networkx
matplotlib
langchain-neo4j
Running the Full Project
Step 1: Scrape scheme data
python scrape_schemes.py

This creates:

data/tn_scheme_details.csv
Step 2: Create Vector Database
python ingest.py

This creates the ChromaDB vector database.

Step 3: Test Neo4j connection
python test_neo4j_connection.py

Expected output:

Neo4j Aura connection successful
Step 4: Load Knowledge Graph into Neo4j
python load_graph_to_neo4j.py

Expected output:

Knowledge Graph loaded successfully into Neo4j AuraDB.
Step 5: Create NetworkX Graph Preview
python networkx_graph_preview.py

This creates:

data/knowledge_graph_preview.png
Step 6: Test Graph RAG
python test_graph_rag.py
Step 7: Test Hybrid RAG
python test_hybrid_rag.py
Step 8: Run Streamlit App
streamlit run app.py
Streamlit App Pages
1. Home

Shows the project overview, architecture, features, and key metrics.

2. AI Scheme Assistant

Allows users to ask scheme-related questions using AI.

3. Scheme Explorer

Allows users to explore schemes using filters such as:

Department
Beneficiary
Benefit Type
Search keyword
4. Knowledge Graph RAG

Allows users to ask relationship-based questions using Neo4j Knowledge Graph RAG.

Example:

Which schemes are sponsored by State?
5. About

Explains the project, technology stack, and safety disclaimer.

Sample Questions
English Questions
Which schemes are available for farmers?
Which schemes provide subsidy benefits?
Which schemes are sponsored by State?
Which schemes are related to seed support?
Which schemes are connected to soil health?
Tamil Questions
விவசாயிகளுக்கான திட்டங்கள் எவை?
விவசாயிகளுக்கான மானிய திட்டங்கள் எவை?
மாநில அரசு நிதியுதவி வழங்கும் திட்டங்கள் எவை?
Neo4j Browser Queries

After loading graph data into Neo4j AuraDB, you can test these Cypher queries.

View graph
MATCH (n) RETURN n LIMIT 50;
View scheme relationships
MATCH (s:Scheme)-[r]->(n)
RETURN s.name, type(r), n.name
LIMIT 50;
State sponsored schemes
MATCH (s:Scheme)-[:SPONSORED_BY]->(sp:Sponsor)
WHERE toLower(sp.name) CONTAINS "state"
RETURN s.name AS Scheme, sp.name AS Sponsored_By
LIMIT 25;
Farmer schemes
MATCH (s:Scheme)-[:FOR_BENEFICIARY]->(b:Beneficiary)
WHERE toLower(b.name) CONTAINS "farmer"
RETURN s.name AS Scheme, b.name AS Beneficiary
LIMIT 25;
Grant schemes
MATCH (s:Scheme)-[:PROVIDES_BENEFIT]->(bt:BenefitType)
WHERE toLower(bt.name) CONTAINS "grant"
RETURN s.name AS Scheme, bt.name AS Benefit
LIMIT 25;
LangSmith Tracing

LangSmith is used for tracing and observing LangChain application runs.

Enable it in .env:

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=TN-Scheme-Navigator-AI

This helps monitor:

Prompt flow
Retriever output
LLM calls
Graph RAG execution
Debugging and evaluation
Git Ignore

The .gitignore file should include:

venv/
.env
vector_db/
__pycache__/
*.pyc
*.pyo
*.pyd
.DS_Store
data/knowledge_graph_preview.png
Production Quality Improvements

The latest app version includes:

Premium sidebar branding
Improved navigation button styling
Better active and hover states
Clear question input cards
Better text area visibility
Stronger example prompt buttons
Improved Tamil readability
Better AI answer card
Route indicator badge
Cleaner official source cards
Better Scheme Explorer layout
Professional government-tech visual design
Responsible AI Disclaimer

This application is designed for learning, exploration, and citizen-friendly information discovery.

Users should always verify final eligibility, scheme benefits, and application process from the official Tamil Nadu Government source links.

This app should not be treated as the final legal or eligibility authority.

Future Enhancements
Add all Tamil Nadu departments
Add district-level filtering
Add user eligibility checker
Add voice input in Tamil
Add PDF export for scheme summaries
Add admin dashboard
Add graph visualization inside Streamlit
Add role-based analytics dashboard
Add evaluation metrics for answer quality
Add deployment on Streamlit Cloud
Developed By

Vishnukumar
Gen AI Architect Program
Hybrid Graph RAG Project
TN Scheme Navigator AI

