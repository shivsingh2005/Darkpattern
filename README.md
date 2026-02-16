# Deceptive Text Detection API

A FastAPI-based backend service for detecting deceptive text using machine learning. This project implements a text classification model trained to identify deceptive patterns in text strings.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Model Details](#model-details)
- [Web Scraper](#web-scraper)
- [License](#license)

## Project Overview

This project is a deceptive text detection system that uses machine learning to classify whether a given text string is deceptive or not. It includes:

- A FastAPI backend for serving predictions
- A trained Logistic Regression model for text classification
- TF-IDF vectorization for feature extraction
- A web scraper module for fetching web content

## Project Structure

```
fipro/
├── backend/
│   ├── main.py              # FastAPI application with /analyze endpoint
│   ├── requirements.txt      # Python dependencies
│   └── README.md            # Backend-specific readme
├── Model/
│   ├── model.pkl            # Trained Logistic Regression model
│   ├── dataset.xlsx         # Training dataset
│   └── Final_Year.ipynb    # Jupyter notebook with model training code
├── webscraper/
│   ├── __init__.py
│   └── scraper.py          # Web scraping functionality
├── .gitignore
└── README.md               # This file
```

## Features

- **Text Classification**: Detects whether text is deceptive or not
- **FastAPI Backend**: Modern, fast Python web framework
- **RESTful API**: Easy to integrate with other applications
- **Confidence Score**: Provides prediction confidence
- **Web Scraper**: Fetch and analyze web content

## Tech Stack

- **Backend Framework**: FastAPI
- **Machine Learning**: scikit-learn (Logistic Regression)
- **Text Processing**: NLTK, TF-IDF Vectorizer
- **Data Handling**: pandas
- **Server**: Uvicorn
- **Web Scraping**: BeautifulSoup, requests

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### 1. Clone the Repository

```
bash
git clone <repository-url>
cd fipro
```

### 2. Create a Virtual Environment (Recommended)

```
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Navigate to the backend directory and install the required packages:

```
bash
cd backend
pip install -r requirements.txt
```

The required packages are:
- fastapi==0.109.0
- uvicorn==0.27.0
- scikit-learn==1.4.0
- nltk==3.8.1
- pandas==2.2.0
- pydantic==2.5.3
- openpyxl==3.1.2

### 4. Download NLTK Data

The application will automatically download the required NLTK data (stopwords, wordnet) on first run. If you want to download manually:

```
python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

## Running the API

### Option 1: Run with Python

```
bash
cd backend
python main.py
```

### Option 2: Run with Uvicorn

```
bash
cd backend
uvicorn main:app --reload
```

### Option 3: Run with Uvicorn (Custom Host/Port)

```
bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### Root Endpoint

**GET /**

Returns API status.

```
bash
curl http://localhost:8000/
```

Response:
```
json
{
  "message": "Deceptive Text Detection API",
  "status": "running"
}
```

### Analyze Endpoint

**POST /analyze**

Analyzes text to detect if it's deceptive or not.

**Request Body:**

```
json
{
  "text": "your text to analyze here"
}
```

**Response:**

```
json
{
  "text": "your text to analyze here",
  "is_deceptive": true,
  "confidence": 0.85,
  "prediction": 1,
  "message": "The text is predicted to be DECEPTIVE."
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| text | string | Original input text |
| is_deceptive | boolean | Whether the text is deceptive |
| confidence | float | Prediction confidence (0-1) |
| prediction | integer | 0 = Not Deceptive, 1 = Deceptive |
| message | string | Human-readable message |

### Interactive API Documentation

FastAPI provides interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Usage Examples

### Using cURL

```
bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "sale ending soon"}'
```

### Using Python

```
python
import requests

url = "http://localhost:8000/analyze"
payload = {"text": "sale ending soon"}

response = requests.post(url, json=payload)
print(response.json())
```

### Using Swagger UI

1. Open http://localhost:8000/docs in your browser
2. Click on the `/analyze` endpoint
3. Click "Try it out"
4. Enter your text and click "Execute"

## Model Details

### Training Data

- **Dataset**: `Model/dataset.xlsx`
- **Text Column**: `Pattern String`
- **Target Column**: `Deceptive?`

### Preprocessing Pipeline

1. Convert text to lowercase
2. Remove punctuation
3. Remove numbers
4. Remove stopwords
5. Apply lemmatization

### Feature Extraction

- **Method**: TF-IDF Vectorization
- **Max Features**: 5000
- **N-gram Range**: (1, 2) - unigrams and bigrams

### Model

- **Algorithm**: Logistic Regression
- **Input**: TF-IDF transformed text
- **Output**: Binary classification (0 = Not Deceptive, 1 = Deceptive)

### Performance Metrics

Based on the training notebook (`Model/Final_Year.ipynb`):
- Accuracy: ~90%
- Precision: ~90%
- Recall: ~93%
- F1-Score: ~92%

## Web Scraper

The project includes a web scraper module for fetching web content.

### Basic Usage

```
python
from webscraper.scraper import scrape_url, get_text_content

# Scrape a URL
result = scrape_url("https://example.com")
print(result)

# Get just text content
text = get_text_content("https://example.com")
print(text)
```

### WebScraper Class

```
python
from webscraper.scraper import WebScraper

scraper = WebScraper()

# Get all text content
text = scraper.get_text_content("https://example.com")

# Get all links
links = scraper.get_links("https://example.com")

# Get all images
images = scraper.get_images("https://example.com")

# Get elements by CSS selector
elements = scraper.get_elements("https://example.com", "h1")
```

## Troubleshooting

### Error: "Model not loaded"

Make sure `Model/model.pkl` exists in the project directory.

### Error: "Vectorizer not loaded"

Make sure `Model/dataset.xlsx` exists in the project directory.

### Error: "TF-IDF vectorizer is not fitted"

This should be automatically handled. If you still encounter this error, ensure the dataset.xlsx file exists and contains the 'Pattern String' column.

### Port Already in Use

If port 8000 is already in use, specify a different port:

```
bash
uvicorn main:app --port 8001
```

## License

This project is for educational purposes.

## Acknowledgments

- Dataset: `cdf2.csv` / `dataset.xlsx`
- Model training: Jupyter Notebook (`Final_Year.ipynb`)
- Built with FastAPI, scikit-learn, and NLTK
