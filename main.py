from resume_screener import ResumeScreener, filter_candidates, print_report

#  Define Job Description


JOB_DESCRIPTION = """
We are looking for a Data Science Engineer with strong Python skills.
The ideal candidate should have experience in machine learning, deep learning,
and natural language processing (NLP). Knowledge of TensorFlow or PyTorch is required.
Experience with data analysis using Pandas and NumPy is essential.
The candidate should be familiar with SQL databases, Git version control,
and cloud platforms like AWS or Azure. Good communication and teamwork skills are a plus.
"""


# Sample Resumes 

RESUMES = [
    {
        "name": "Abdullah Khan",
        "text": """
        Experienced Data Scientist with 3 years of industry experience.
        Proficient in Python, TensorFlow, PyTorch, and scikit-learn.
        Strong background in machine learning, deep learning, and NLP projects.
        Used Pandas, NumPy for data analysis and SQL for database queries.
        Worked on AWS cloud infrastructure and managed projects with Git.
        Excellent communication and leadership skills. Agile/Scrum experience.
        """
    },
    {
        "name": "Ali Khan",
        "text": """
        Software developer with 2 years of experience in web development.
        Skills: JavaScript, React, HTML, CSS, Node.js.
        Some experience with Python scripting and basic SQL queries.
        Used Git for version control and Docker for containerization.
        Strong teamwork and problem solving skills.
        """
    },
    {
        "name": "Abdul Rahman Khan",
        "text": """
        Machine Learning Engineer specializing in computer vision and NLP.
        Proficient in Python, PyTorch, TensorFlow, OpenCV, Pandas, NumPy.
        Experience with deep learning model deployment on AWS and Azure.
        Built NLP pipelines for text classification and sentiment analysis.
        Strong SQL skills, used Git, and familiar with Agile methodology.
        Great communication skills and collaborative team player.
        """
    },
    {
        "name": "Shehbaz Sharif",
        "text": """
        Recent graduate in Computer Science.
        Familiar with Java, C++, and some Python.
        Took a data science course covering basics of machine learning.
        Basic knowledge of HTML and CSS for web projects.
        No professional experience yet, but eager to learn.
        """
    },
    {
        "name": "Nawaz Sharif",
        "text": """
        Data Analyst with 4 years of experience in business intelligence.
        Expert in SQL, Excel, and data analysis using Python (Pandas, NumPy).
        Experience with machine learning algorithms using sklearn.
        Familiar with NLP techniques for customer feedback analysis.
        Used Azure for cloud storage and Power BI for dashboards.
        Strong communication, teamwork, and critical thinking skills.
        """
    },
]


# Run Screening

def main():

    screener = ResumeScreener(JOB_DESCRIPTION)

    all_results = screener.screen(RESUMES)

    print_report(all_results, title="ALL CANDIDATES — FULL REPORT")

    shortlisted = filter_candidates(all_results, min_score=50.0)

    print(f"   SHORTLISTED CANDIDATES (Score ≥ 50)")
    print(f"  {'-'*40}")
    for c in shortlisted:
        print(f"  #{c['rank']}  {c['name']}  →  {c['final_score']:.1f}/100")
    print(f"\n  Total shortlisted: {len(shortlisted)} / {len(RESUMES)} candidates\n")


if __name__ == "__main__":
    main()
