import pandas as pd
import ast

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. Load the dataset
# --------------------------------------------------

df = pd.read_csv("data/all_job_post.csv")

print("Dataset loaded successfully!")
print("Number of jobs:", len(df))


# --------------------------------------------------
# 2. Convert job skills from text to Python lists
# --------------------------------------------------

df["job_skill_set"] = df["job_skill_set"].apply(ast.literal_eval)


# --------------------------------------------------
# 3. Clean job skills
# --------------------------------------------------

df["job_skill_set"] = df["job_skill_set"].apply(
    lambda skills: [
        str(skill).strip().lower()
        for skill in skills
        if str(skill).strip()
    ]
)


# --------------------------------------------------
# 4. Ask the user for their skills
# --------------------------------------------------

user_input = input(
    "\nEnter your skills separated by commas: "
)


# Clean user skills

user_skills = [
    skill.strip().lower()
    for skill in user_input.split(",")
    if skill.strip()
]


print("\nYour Skills:")

for skill in sorted(set(user_skills)):
    print("-", skill)


# --------------------------------------------------
# 5. Create text representation of job skills
# --------------------------------------------------

df["skills_text"] = df["job_skill_set"].apply(
    lambda skills: " ".join(skills)
)


# --------------------------------------------------
# 6. Create the user's skill text
# --------------------------------------------------

user_skills_text = " ".join(user_skills)


# --------------------------------------------------
# 7. Convert job skills into TF-IDF vectors
# --------------------------------------------------

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2)
)

job_tfidf = vectorizer.fit_transform(
    df["skills_text"]
)


# Convert user's skills using the SAME vectorizer

user_tfidf = vectorizer.transform(
    [user_skills_text]
)


# --------------------------------------------------
# 8. Calculate cosine similarity
# --------------------------------------------------

similarity_scores = cosine_similarity(
    user_tfidf,
    job_tfidf
).flatten()


# --------------------------------------------------
# 9. Store similarity scores
# --------------------------------------------------

df["similarity_score"] = similarity_scores

# Calculate skill match percentage for every job
user_skill_set = set(user_skills)

skill_match_scores = []

for skills in df["job_skill_set"]:
    required_skills = set(skills)

    if len(required_skills) == 0:
        skill_match = 0
    else:
        matched = user_skill_set.intersection(required_skills)

        skill_match = (
            len(matched) / len(required_skills)
        ) * 100

    skill_match_scores.append(skill_match)

df["skill_match_score"] = skill_match_scores

# Combine skill match and TF-IDF similarity
df["final_score"] = (
    0.7 * df["skill_match_score"]
    + 0.3 * (df["similarity_score"] * 100)
) 

# Keep jobs where the user has at least 3 matching skills
df["matched_skill_count"] = df["job_skill_set"].apply(
    lambda skills: len(
        set(user_skills).intersection(set(skills))
    )
)

recommended_jobs = df[
    df["matched_skill_count"] >= 3
].sort_values(
    by="final_score",
    ascending=False
)

print("\nTop 5 Career Recommendations:")
for i, (_, job) in enumerate(recommended_jobs.head(5).iterrows(), start=1):

    final_score = job["final_score"]
    skill_score = job["skill_match_score"]
    similarity_score = job["similarity_score"] * 100

    print(
        f"\n{i}. {job['job_title']} "
        f"({job['category']})"
    )

    print(f"   Overall Score: {final_score:.2f}%")
    print(f"   Skill Match: {skill_score:.2f}%")
    print(f"   TF-IDF Similarity: {similarity_score:.2f}%")

    matched_skills = set(user_skills).intersection(
        set(job["job_skill_set"])
    )

    missing_skills = set(job["job_skill_set"]) - set(user_skills)

    print("   Matched Skills:")

    for skill in sorted(matched_skills):
        print("   -", skill)

    print("   Missing Skills:")

    for skill in sorted(missing_skills):
        print("   -", skill)