import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("data/all_job_post.csv")

# Replace missing descriptions
df["job_description"] = df["job_description"].fillna("")

# Create TF-IDF
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=1000
)

tfidf_matrix = vectorizer.fit_transform(df["job_description"])

# Calculate similarity between all jobs
similarity_matrix = cosine_similarity(tfidf_matrix)

# Ask the user for a job title
job_title = input("\nEnter a job title: ")

# Find jobs with that title
matching_jobs = df[
    df["job_title"].str.lower() == job_title.lower()
]

if matching_jobs.empty:
    print("Job title not found.")
    exit()

# Use the first matching job
job_index = matching_jobs.index[0]

# Get similarity scores for the selected job
similarity_scores = similarity_matrix[job_index]

# Sort jobs from most similar to least similar
similar_jobs = similarity_scores.argsort()[::-1]

print("\nSelected Job:")
print("Title:", df.iloc[job_index]["job_title"])
print("Category:", df.iloc[job_index]["category"])

print("\nTop 5 Similar Jobs:")

count = 0

for index in similar_jobs:

    # Skip the selected job itself
    if index == job_index:
        continue

    print(
        f"{count + 1}. "
        f"{df.iloc[index]['job_title']} "
        f"({df.iloc[index]['category']}) "
        f"- Similarity: {similarity_scores[index]:.3f}"
    )

    count += 1

    if count == 5:
        break