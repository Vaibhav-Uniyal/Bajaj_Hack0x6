# 🤖 LLM-Powered Intelligent Query–Retrieval System

A sophisticated AI-powered document analysis and question answering system designed for insurance, legal, HR, and compliance domains. This system processes large documents (PDFs, DOCX, emails) and provides intelligent, contextual responses with explainable AI reasoning.

## 🚀 Features

- **📄 Multi-Format Document Processing**: PDF, DOCX, and email documents
- **🧠 LLM Integration**: Google Gemini for intelligent parsing and reasoning
- **🔍 Semantic Search**: FAISS/Pinecone vector databases for context-aware retrieval
- **📊 Structured Responses**: JSON output with confidence scores and source clauses
- **🔐 Authentication**: Bearer token security
- **⚡ Serverless Ready**: Optimized for Vercel deployment
- **📈 Detailed Analytics**: Comprehensive scoring and evaluation metrics

## 🏗️ Architecture

The system consists of 6 core components:

1. **Input Documents** - Document ingestion and processing
2. **LLM Parser** - Natural language query understanding
3. **Embedding Search** - Semantic search and retrieval
4. **Clause Matching** - Contextual clause identification
5. **Logic Evaluation** - AI-powered decision processing
6. **Response Generator** - Structured JSON output

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **LLM**: Google Gemini 2.0 Flash
- **Vector DB**: FAISS (local) / Pinecone (cloud)
- **Embeddings**: Sentence Transformers
- **Document Processing**: PyPDF2
- **Deployment**: Vercel (serverless)

## 📋 Prerequisites

- Python 3.8+
- Node.js (for Vercel CLI)
- Google Gemini API key
- Pinecone API key (optional)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd hackr6
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
Create a `.env` file:
```bash
# Authentication
AUTH_TOKEN=db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6

# Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Pinecone Configuration (Optional)
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=your_index_name
```

### 4. Run Locally
```bash
python main.py
```

### 5. Test the API
```bash
python test_local_policy.py
```

## 🌐 API Endpoints

### Health Check
```bash
GET /api/v1/health
```

### Basic Query
```bash
POST /api/v1/hackrx/run
Content-Type: application/json
Authorization: Bearer <your-token>

{
  "documents": ["https://example.com/policy.pdf"],
  "questions": ["What is the grace period for premium payment?"]
}
```

### Detailed Query
```bash
POST /api/v1/hackrx/run/detailed
Content-Type: application/json
Authorization: Bearer <your-token>

{
  "documents": ["https://example.com/policy.pdf"],
  "questions": ["What is the grace period for premium payment?"]
}
```

## 📝 Example Response

```json
{
  "answers": [
    "A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy without losing continuity benefits."
  ],
  "confidence_scores": [0.85],
  "source_clauses": [
    "Section 4.2: Grace Period - A grace period of thirty (30) days shall be allowed for payment of premium..."
  ],
  "processing_time": 2.34
}
```

## 🚀 Deploy to Vercel

### 1. Install Vercel CLI
```bash
npm i -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy
```bash
vercel --prod
```

### 4. Set Environment Variables
In your Vercel dashboard, add the same environment variables as above.

### 5. Test Deployment
```bash
python test_vercel_deployment.py
```

## 📁 Project Structure

```
hackr6/
├── src/
│   ├── components/
│   │   ├── document_processor.py    # Document ingestion
│   │   ├── llm_parser.py           # Query parsing
│   │   ├── embedding_search.py      # Vector search
│   │   ├── clause_matcher.py       # Clause matching
│   │   ├── logic_evaluator.py      # Decision processing
│   │   └── response_generator.py   # Response formatting
│   ├── api.py                      # FastAPI endpoints
│   ├── api_serverless.py           # Serverless API
│   ├── orchestrator.py             # Main orchestrator
│   ├── models.py                   # Pydantic models
│   └── config.py                   # Configuration
├── api/
│   └── index.py                    # Vercel entry point
├── tests/
│   ├── test_local_policy.py        # Local testing
│   ├── test_vercel_deployment.py   # Deployment testing
│   └── test_*.py                   # Various test scripts
├── main.py                         # Local development server
├── requirements.txt                 # Dependencies
├── requirements-vercel.txt          # Vercel dependencies
├── vercel.json                     # Vercel configuration
├── .env                            # Environment variables
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🧪 Testing

### Local Testing
```bash
# Test with local policy document
python test_local_policy.py

# Test authentication
python test_auth.py

# Test full API functionality
python test_full_api.py
```

### Deployment Testing
```bash
# Test Vercel deployment
python test_vercel_deployment.py

# Test with custom URL
python test_custom_url.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AUTH_TOKEN` | Bearer token for API authentication | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `PINECONE_API_KEY` | Pinecone API key (optional) | No |
| `PINECONE_ENVIRONMENT` | Pinecone environment | No |
| `PINECONE_INDEX_NAME` | Pinecone index name | No |

### System Configuration

The system can be configured in `src/config.py`:

- **Chunk Size**: Maximum words per document chunk
- **Embedding Model**: Sentence transformer model
- **Scoring Weights**: Question type scoring weights
- **Document Weights**: Known vs unknown document weights

## 📊 Performance Metrics

The system provides comprehensive evaluation metrics:

- **Accuracy**: Percentage of correct answers
- **Confidence Scores**: AI confidence in responses
- **Processing Time**: End-to-end processing duration
- **Token Efficiency**: LLM token usage optimization
- **Latency**: Response time measurements

## 🛠️ Development

### Adding New Components

1. Create component in `src/components/`
2. Add to orchestrator in `src/orchestrator.py`
3. Update tests in `tests/`
4. Update documentation

### Customizing Models

- **LLM**: Change `GEMINI_MODEL` in config
- **Embeddings**: Change `EMBEDDING_MODEL` in config
- **Vector DB**: Switch between FAISS and Pinecone

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Issues**: Verify environment variables are set
3. **Timeout Errors**: Optimize chunk sizes or break requests
4. **Memory Errors**: Reduce chunk sizes or optimize models

### Debugging

```bash
# Test individual components
python debug_document_processor.py
python debug_local_pdf.py

# Test orchestrator directly
python test_orchestrator_direct.py
```

## 📈 Monitoring

- **Vercel Analytics**: Monitor function performance
- **Application Logs**: Check detailed processing logs
- **Health Endpoint**: Verify system status
- **Custom Metrics**: Track accuracy and latency

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini for LLM capabilities
- Sentence Transformers for embeddings
- FAISS and Pinecone for vector databases
- FastAPI for the web framework
- Vercel for serverless deployment

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the test scripts for examples

---

**Built with ❤️ for intelligent document analysis and question answering**
