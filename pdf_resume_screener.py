import os
import fitz 
from resume_screener import ResumeScreener, filter_candidates, print_report


# Define Job Description

JOB_DESCRIPTION = """
We are looking for a Data Science Engineer with strong Python skills.
The ideal candidate should have experience in machine learning, deep learning,
and natural language processing (NLP). Knowledge of TensorFlow or PyTorch is required.
Experience with data analysis using Pandas and NumPy is essential.
The candidate should be familiar with SQL databases, Git version control,
and cloud platforms like AWS or Azure. Good communication and teamwork skills are a plus.
"""


# PDF Reader Function

def read_pdf(file_path: str) -> str:
    "Automatically extract all text from a PDF file."
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"    Could not read {file_path}: {e}")
    return text


def load_resumes_from_folder(folder: str) -> list[dict]:
    """
    Scan a folder for PDF files and load them as resumes.
    Each PDF filename becomes the candidate's name.
    """
    resumes = []

    if not os.path.exists(folder):
        print(f"\n    Folder '{folder}' not found!")
        print(f"   Please create a folder called 'cvs' in your AI Project folder")
        print(f"   Then put PDF resumes inside it\n")
        return resumes

    pdf_files = [f for f in os.listdir(folder) if f.endswith('.pdf')]

    if not pdf_files:
        print(f"\n    No PDF files found in '{folder}' folder!")
        print(f"   Please put PDF resumes inside the 'cvs' folder\n")
        return resumes

    print(f"\n   Found {len(pdf_files)} PDF resume(s) in '{folder}' folder:")
    for pdf in pdf_files:
        file_path = os.path.join(folder, pdf)
        text = read_pdf(file_path)
        name = pdf.replace('.pdf', '').replace('_', ' ').replace('-', ' ').title()
        resumes.append({"name": name, "text": text})
        print(f"  Loaded: {name}")

    return resumes


#  Screening

def main():
    print("\n Resume Screening AI — PDF Version")
    print("   Powered by NLP (TF-IDF) + ML (Cosine Similarity)")

    cvs_folder = "cvs"
    resumes = load_resumes_from_folder(cvs_folder)

    if not resumes:
        print("\n   No resumes to screen. Please add PDF files to the 'cvs' folder.")
        return

    screener = ResumeScreener(JOB_DESCRIPTION)

    all_results = screener.screen(resumes)

    print_report(all_results, title="ALL CANDIDATES — FULL REPORT")

    # Data Filtering
    shortlisted = filter_candidates(all_results, min_score=50.0)

    print(f"   SHORTLISTED CANDIDATES (Score ≥ 50)")
    print(f"  {'-'*40}")
    if shortlisted:
        for c in shortlisted:
            print(f"  #{c['rank']}  {c['name']}  →  {c['final_score']:.1f}/100")
    else:
        print(f"  No candidates met the minimum score.")

    print(f"\n  Total shortlisted: {len(shortlisted)} / {len(resumes)} candidates\n")


if __name__ == "__main__":
    main()
