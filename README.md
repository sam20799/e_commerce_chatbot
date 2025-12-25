# 🛒 QueryCart – GenAI E-Commerce Chatbot

A GenAI-powered e-commerce chatbot that lets users search products and get answers using natural language. Built with LLMs, SQL, and Retrieval-Augmented Generation (RAG) for accurate, data-grounded responses.

![App Preview](/website_preview.png)

## ✨ Features

- **Natural Language Product Search** – Ask questions like "Show me Nike shoes under ₹3000 with rating above 4.5"
- **FAQ Support** – Get instant answers to common questions about returns, refunds, and policies
- **Smart Query Routing** – Automatically detects whether to search products or answer FAQs
- **SQL Generation** – Converts natural language to structured SQL queries
- **RAG-Powered Answers** – Uses vector search for accurate FAQ responses
- **No Hallucinations** – All responses grounded in actual data

## 🏗️ Architecture

```
User Query → Semantic Router → FAQ (RAG) or Product Search (Text-to-SQL) → LLM Response
```

![System Flowchart](/flowchart.png)

- **Semantic Router**: Classifies queries as FAQ or product search
- **FAQ Pipeline**: ChromaDB + sentence transformers for vector similarity search
- **SQL Pipeline**: 
  - LLM converts natural language query to SQL
  - Executes SQL against SQLite database
  - LLM transforms database results back into natural language response
- **Response Generation**: All responses grounded in retrieved data

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Groq API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/querycart.git
cd querycart
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
echo "GROQ_MODEL=llama3-70b-8192" >> .env
```

4. Run the application
```bash
streamlit run main.py
```

## 📦 Tech Stack

- **Streamlit** – Web interface
- **Groq** – LLM inference
- **ChromaDB** – Vector database for FAQ retrieval
- **Semantic Router** – Query classification
- **SQLite** – Product database
- **Sentence Transformers** – Text embeddings

## 📊 Data

The app uses a dataset of women's footwear with fields including:
- Product title and link
- Brand
- Price (₹)
- Discount percentage
- Average rating
- Total ratings

## 💡 Example Queries

**Product Search:**
- "Show me Puma shoes with rating above 4.5"
- "Top 3 Nike shoes under ₹3000"
- "Adidas shoes with more than 30% discount"

**FAQs:**
- "What is your return policy?"
- "How do I track my order?"
- "What payment methods do you accept?"

## ⚠️ Limitations

- Static dataset (not real-time inventory)
- Limited to women's footwear categories
- Requires specific queries for best results

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or feedback, please open an issue on GitHub.