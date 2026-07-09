# AI Resume Screening System

An AI-powered Resume Screening System built in Python that evaluates resumes against a job description using Natural Language Processing (NLP) techniques.

## Features

- Resume screening against a job description
- TF-IDF based text similarity
- Cosine Similarity for resume ranking
- Skill extraction using predefined keywords
- Candidate scoring and ranking
- Candidate shortlisting based on a minimum score
- PDF resume support

## Technologies Used

- Python
- Natural Language Processing (NLP)
- TF-IDF
- Cosine Similarity
- Regular Expressions (Regex)
- Collections (Counter)

## Project Structure

```
ResumeScreeningPython/
│── main.py
│── resume_screener.py
│── main Pdf Version.py
│── cvs/
│── .gitignore
│── README.md
```

## How It Works

1. Define a Job Description.
2. Load candidate resumes.
3. Extract important skills from both the job description and resumes.
4. Calculate TF-IDF vectors.
5. Compute Cosine Similarity.
6. Combine text similarity and skill matching to generate a final score.
7. Rank candidates and display shortlisted applicants.

## Installation

Clone the repository:

```bash
git clone https://github.com/abdullahhamid208/ResumeScreeningPython.git
```

Go to the project folder:

```bash
cd ResumeScreeningPython
```

(Optional) Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Sample Output

The application displays:

- Candidate Name
- Similarity Score
- Skill Match Percentage
- Final Score
- Overall Ranking
- Shortlisted Candidates

## Future Improvements

- Resume upload through a web interface
- Machine Learning based resume classification
- Support for DOCX resumes
- Automatic keyword extraction
- Streamlit or Flask web application
- Integration with OpenAI APIs for semantic matching

## Author

**Abdullah Hamid**

GitHub: https://github.com/abdullahhamid208
