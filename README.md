# Dark Pattern Detection API

A FastAPI-based backend service for detecting dark patterns in text and web content using machine learning. This project implements a text classification model trained to identify deceptive patterns in text strings.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
  - [Backend](#running-the-backend)
  - [Frontend](#running-the-frontend)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Model Details](#model-details)
- [Web Scraper](#web-scraper)
- [License](#license)

## Project Overview

This project is a dark pattern detection system that uses machine learning to classify whether a given text string contains dark patterns. It includes:

- A FastAPI backend for serving predictions
- A React frontend for user interaction
- A trained Logistic Regression model for text classification
- TF-IDF vectorization for feature extraction
- A web scraper module for fetching web content

## Project Structure

```
Darkpattern/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   ├── pipeline/            # ML pipeline modules
│   │   ├── inference.py      # Inference service
│   │   └── preprocess.py     # Text preprocessing
│   ├── routes/              # API routes
│   │   ├── analyze_route.py
│   │   └── url_route.py
│   └── README.md            # Backend-specific readme
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── Model/
│   ├── model.pkl            # Trained Logistic Regression model
│   ├── vectorizer.pkl       # TF-IDF vectorizer
│   ├── dataset.xlsx         # Training dataset
│   └── Final_Year.ipynb    # Jupyter notebook with model training code
├── webscraper/
│   ├── __init__.py
│   └── scraper.py          # Web scraping functionality
├── .gitignore
└── README.md               # This file
```

## Features

- **Text Classification**: Detects dark patterns in text
- **URL Analysis**: Scan websites for dark patterns
- **FastAPI Backend**: Modern, fast Python web framework
- **React Frontend**: User-friendly web interface
- **RESTful API**: Easy to integrate with other applications
- **Confidence Score**: Provides prediction confidence
- **Web Scraper**: Fetch and analyze web content

## Tech Stack

- **Backend Framework**: FastAPI
- **Frontend Framework**: React + Vite
- **Machine Learning**: scikit-learn (Logistic Regression)
- **Text Processing**: NLTK, TF-IDF Vectorizer
- **Data Handling**: pandas
- **Server**: Uvicorn
- **Web Scraping**: BeautifulSoup, requests
- **Styling**: Tailwind CSS

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- pip package manager
- npm or yarn

### 1. Clone the Repository

```
bash
git clone <repository-url>
cd Darkpattern
```

### 2. Backend Setup

#### Create a Virtual Environment (Recommended)

```
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Install Backend Dependencies

```
bash
cd backend
pip install -r requirements.txt
```

The required packages are:
- fastapi==0.115.0
- uvicorn==0.30.6
- scikit-learn==1.7.1
- joblib==1.4.2
- nltk==3.9.1
- requests==2.32.3
- beautifulsoup4==4.12.3
- lxml==5.3.0

#### Download NLTK Data

The application will automatically download the required NLTK data (stopwords, wordnet) on first run. If you want to download manually:

```
python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

### 3. Frontend Setup

#### Install Frontend Dependencies

```
bash
cd frontend
npm install
```

Or if using yarn:

```
bash
cd frontend
yarn install
```

## Running the Application

### Running the Backend

```
bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

### Running the Frontend

```
bash
cd frontend
npm run dev
```

The frontend will be available at: `http://localhost:3000`

### Running Both Simultaneously

For development, you can run both the backend and frontend in separate terminals:

**Terminal 1 (Backend):**
```
bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 (Frontend):**
```
bash
cd frontend
npm run dev
```

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
  "message": "Dark Pattern Detection API",
  "status": "running"
}
```

### Analyze Text Endpoint

**POST /analyze**

Analyzes text to detect dark patterns.

**Request Body:**
```
json
{
  "text": "your text to analyze here"
}
```

### Detect from URL Endpoint

**POST /detect-from-url**

Analyzes a URL for dark patterns.

**Request Body:**
```
json
{
  "url": "https://example.com"
}
```

### Interactive API Documentation

FastAPI provides interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Usage Examples

### Using the Frontend

1. Open http://localhost:3000 in your browser
2. Enter text to analyze or paste a URL
3. View the results

### Using cURL

```
bash
# Analyze text
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "sale ending soon"}'

# Analyze URL
curl -X POST "http://localhost:8000/detect-from-url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Using Python

```
python
import requests

# Analyze text
url = "http://localhost:8000/analyze"
payload = {"text": "sale ending soon"}
response = requests.post(url, json=payload)
print(response.json())

# Analyze URL
url = "http://localhost:8000/detect-from-url"
payload = {"url": "https://example.com"}
response = requests.post(url, json=payload)
print(response.json())
```

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
- **Output**: Binary classification (0 = Not Dark Pattern, 1 = Dark Pattern)

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

If port 8000 or 3000 is already in use, specify a different port:

```
bash
# Backend
uvicorn main:app --port 8001

# Frontend - update vite.config.js or run with:
npm run dev -- --port 3001
```

### Frontend Cannot Connect to Backend

Ensure the backend is running at http://localhost:8000. The frontend is configured to connect to this URL by default. Check the `frontend/src/services/api.js` file for configuration.

## License

This project is for educational purposes.

## Acknowledgments

- Dataset: `cdf2.csv` / `dataset.xlsx`
- Model training: Jupyter Notebook (`Final_Year.ipynb`)
- Built with FastAPI, React, scikit-learn, and NLTK
