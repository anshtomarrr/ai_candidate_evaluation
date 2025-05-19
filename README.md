# AI Resume Ranker

An intelligent resume ranking system that uses NLP and machine learning to evaluate candidate resumes against job descriptions.

## Features

- Upload and process resumes (PDF, DOCX, TXT)
- Upload or paste job descriptions
- AI-powered resume analysis and ranking
- Extract candidate information automatically
- Calculate similarity scores using TF-IDF and cosine similarity
- Generate pros and cons for each candidate
- Tier candidates based on match quality
- Download results in JSON or CSV format

## Installation

1. Clone the repository:

```bash
git clone https://github.com/anshtomarrr/ai_candidate_evaluation.git
cd ai_candidate_evaluation
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:

```bash
streamlit run app.py
```

2. Open your browser and go to: http://localhost:8501

3. Upload a job description and resumes
4. Click "Run AI Ranking" to process the resumes
5. View and download the results

## Requirements

- Python 3.9+
- Streamlit
- Pandas
- NLTK
- scikit-learn
- PyPDF2
- pdfminer.six
- python-docx

## License

MIT License
