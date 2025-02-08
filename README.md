# AI Text Processing Service

A Flask-based REST API that leverages LLMs to provide intelligent text analysis, including summarization, keyword extraction, and sentiment detection.

## 🚀 Features

- **Text Analysis**: Advanced natural language processing using Large Language Models
- **Automated Extraction**:
  - ✍️ Text Summarization
  - 🔑 Keyword and Named Entity Extraction
  - 😊 Sentiment Analysis
- **History Tracking**: Persistent storage of all processed texts
- **RESTful API**: Clean and simple endpoints
- **Error Handling**: Robust validation and error management

## 🛠️ API Endpoints

### POST /process
Process text input and return analysis results
- **Input**: JSON payload with `text` field
- **Returns**: Processed results including summary, keywords, and sentiment

### GET /history
Retrieve history of processed texts
- **Returns**: List of all previously processed texts and their results

## 📦 Project Structure 