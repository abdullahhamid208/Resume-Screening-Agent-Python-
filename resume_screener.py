import re
import math
from collections import Counter


#  TEXT CLEANING & PREPROCESSING 

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "was", "are", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "i", "we", "you", "he", "she", "they", "it",
    "this", "that", "these", "those", "my", "our", "your", "their", "its"
}

def clean_text(text: str) -> str:
    """Lowercase, remove punctuation/numbers, strip extra spaces."""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)   # keep only letters
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text: str) -> list[str]:
    """Split cleaned text into tokens, removing stopwords."""
    tokens = clean_text(text).split()
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]


#  SKILL EXTRACTION 

SKILL_KEYWORDS = {
    # Programming
    "python", "java", "javascript", "typescript", "c", "cpp", "csharp",
    "sql", "html", "css", "r", "matlab", "swift", "kotlin", "go", "rust",
    # Frameworks & Tools
    "react", "angular", "vue", "django", "flask", "fastapi", "spring",
    "tensorflow", "pytorch", "sklearn", "pandas", "numpy", "opencv",
    "docker", "kubernetes", "git", "github", "linux", "aws", "azure",
    # Domains
    "machine learning", "deep learning", "nlp", "data science",
    "computer vision", "data analysis", "web development", "cloud",
    "cybersecurity", "devops", "agile", "scrum",
    # Soft skills
    "communication", "leadership", "teamwork", "problem solving",
    "critical thinking", "time management", "collaboration"
}

def extract_skills(text: str) -> set[str]:
    "Find known skills mentioned in a piece of text."
    text_lower = text.lower()
    found = set()
    for skill in SKILL_KEYWORDS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.add(skill)
    return found


#  TF-IDF SIMILARITY

def compute_tf(tokens: list[str]) -> dict[str, float]:
    """Term Frequency: how often each word appears (normalised)."""
    count = Counter(tokens)
    total = len(tokens) if tokens else 1
    return {word: freq / total for word, freq in count.items()}

def compute_idf(documents: list[list[str]]) -> dict[str, float]:
    """
    Inverse Document Frequency: penalises words common across all docs.
    IDF(t) = log( N / (1 + df(t)) )
    """
    N = len(documents)
    df = Counter()
    for doc in documents:
        for word in set(doc):
            df[word] += 1
    return {word: math.log(N / (1 + freq)) for word, freq in df.items()}

def tfidf_vector(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    """Combine TF and IDF into a single weighted vector."""
    tf = compute_tf(tokens)
    return {word: tf_val * idf.get(word, 0) for word, tf_val in tf.items()}

def cosine_similarity(vec_a: dict, vec_b: dict) -> float:
    """
    Cosine Similarity between two TF-IDF vectors.
    Score of 1.0 = identical, 0.0 = completely different.
    """
    common = set(vec_a) & set(vec_b)
    if not common:
        return 0.0
    dot_product = sum(vec_a[w] * vec_b[w] for w in common)
    mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot_product / (mag_a * mag_b)


#  MAIN SCREENING

class ResumeScreener:
    """
    Screens and ranks resumes against a job description.

    Scoring breakdown:
      - 60%  TF-IDF cosine similarity (overall text match)
      - 40%  Skill overlap ratio (matched skills / required skills)
    """

    def __init__(self, job_description: str):
        self.job_description = job_description
        self.job_tokens = tokenize(job_description)
        self.job_skills = extract_skills(job_description)

    def score_resume(self, resume_text: str, idf: dict) -> dict:
        "Score a single resume against the job description."
        resume_tokens = tokenize(resume_text)
        resume_skills = extract_skills(resume_text)

    
        job_vec = tfidf_vector(self.job_tokens, idf)
        res_vec = tfidf_vector(resume_tokens, idf)
        tfidf_score = cosine_similarity(job_vec, res_vec)

        matched_skills = resume_skills & self.job_skills
        skill_score = (
            len(matched_skills) / len(self.job_skills)
            if self.job_skills else 0.0
        )

        # Final score
        final_score = round((0.3 * tfidf_score + 0.7 * skill_score) * 100, 2)

        return {
            "tfidf_score": round(tfidf_score * 100, 2),
            "skill_score": round(skill_score * 100, 2),
            "final_score": final_score,
            "matched_skills": sorted(matched_skills),
            "missing_skills": sorted(self.job_skills - resume_skills),
        }

    def screen(self, resumes: list[dict]) -> list[dict]:
        """
        Screen and rank a list of resumes.

        Args:
            resumes: list of dicts with keys 'name' and 'text'

        Returns:
            Ranked list (highest score first) with full result details.
        """
        all_docs = [self.job_tokens] + [tokenize(r["text"]) for r in resumes]
        idf = compute_idf(all_docs)

        results = []
        for resume in resumes:
            scores = self.score_resume(resume["text"], idf)
            results.append({
                "name": resume["name"],
                **scores
            })

        # Sorting
        results.sort(key=lambda x: x["final_score"], reverse=True)

        # Add rank
        for i, r in enumerate(results, 1):
            r["rank"] = i

        return results


#  DATA FILTERING  

def filter_candidates(results: list[dict], min_score: float = 50.0) -> list[dict]:
    """
    Data Filtering step: keep only candidates above a threshold score.
    Default threshold = 50 out of 100.
    """
    return [r for r in results if r["final_score"] >= min_score]


#  REPORT

def print_report(results: list[dict], title: str = "SCREENING REPORT"):
    "Pretty-print the screening results to console."
    print(f"\n{'='*30}")
    print(f"  {title}")
    print(f"{'='*30}")

    for r in results:
        status = " SHORTLISTED" if r["final_score"] >= 50 else " REJECTED"
        print(f"\n  Rank #{r['rank']}  |  {r['name']}  |  {status}")
        print(f"  {'─'*50}")
        print(f"  Final Score   : {r['final_score']:.1f} / 100")
        print(f"  TF-IDF Match  : {r['tfidf_score']:.1f}%")
        print(f"  Skill Match   : {r['skill_score']:.1f}%")
        print(f"  Matched Skills: {', '.join(r['matched_skills']) or 'None'}")
        print(f"  Missing Skills: {', '.join(r['missing_skills']) or 'None'}")

    print(f"\n{'='*60}\n")
