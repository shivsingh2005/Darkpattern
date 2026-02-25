# Backend Run Guide

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher (for frontend)

## 1) Install dependencies

```
bash
cd backend
pip install -r requirements.txt
```

## 2) Ensure model artifacts exist

The backend requires the following model files in the Model directory:

- `Model/model.pkl` - Trained Logistic Regression model
- `Model/vectorizer.pkl` - TF-IDF vectorizer
- `Model/dataset.xlsx` - Training dataset

## 3) Run Backend API

```
bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: http://localhost:8000

## 4) Run Frontend (in separate terminal)

```
bash
cd frontend
npm install
npm run dev
```

The frontend will be available at: http://localhost:3000

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/analyze` | POST | Analyze text for dark patterns |
| `/detect-from-url` | POST | Analyze URL for dark patterns |

## Testing the API

```
bash
# Health check
curl http://localhost:8000/

# Analyze text
curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d '{"text": "Limited time offer!"}'

# Analyze URL
curl -X POST http://localhost:8000/detect-from-url -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
```

## Interactive API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
