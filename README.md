# Student Performance Prediction

A simple web application to predict student final scores based on study hours, attendance, and previous marks using machine learning.

## Project Structure

```
student-performance-prediction/
├── backend/
│   ├── app.py          # Flask API server
│   └── model.pkl       # Trained ML model
├── frontend/
│   └── streamlit_app.py # Streamlit UI
├── data/
│   └── student_data.csv # Sample dataset
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Installation

1. Clone or download the project.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask backend:
   ```
   cd backend
   python app.py
   ```
   The API will run on http://localhost:5000

2. In a new terminal, start the Streamlit frontend:
   ```
   streamlit run frontend/streamlit_app.py
   ```
   The UI will open in your browser.

## Usage

- Enter study hours, attendance percentage, and previous marks.
- Click "Predict Final Score" to get the prediction.

## Model

The application uses a Linear Regression model trained on the sample dataset. The model is saved as `model.pkl` and loaded by the Flask API for predictions.
