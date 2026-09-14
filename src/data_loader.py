import pandas as pd
import ast
from collections import Counter
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/all_job_post.csv")

# Convert text into Python lists
df["job_skill_set"] = df["job_skill_set"].apply(ast.literal_eval)

# Normalize skill names
df["job_skill_set"] = df["job_skill_set"].apply(
    lambda skills: [skill.lower().strip() for skill in skills]
)
print("\nTop 5 skills by job category:")

for category in df["category"].unique():

    category_skills = []

    # Get skills from jobs in this category
    category_jobs = df[df["category"] == category]

    for skills in category_jobs["job_skill_set"]:
        category_skills.extend(skills)

    # Count skills
    category_skill_counts = Counter(category_skills)

    print(f"\n{category}:")

    for skill, count in category_skill_counts.most_common(5):
        print(f"  {skill} : {count}")

# Combine all skills from all jobs
all_skills = []

for skills in df["job_skill_set"]:
    all_skills.extend(skills)

# Count how often each skill appears
skill_counts = Counter(all_skills)

# Print top 20 skills
print("\nTop 20 most demanded skills after cleaning:")

for skill, count in skill_counts.most_common(20):
    print(f"{skill} : {count}")

print("\nJob categories:")
print(df["category"].value_counts())

# Get top 10 skills for the chart
top_skills = skill_counts.most_common(10)

skills = [skill for skill, count in top_skills]
counts = [count for skill, count in top_skills]

# Create bar chart
plt.figure(figsize=(10, 6))
plt.bar(skills, counts)

plt.title("Top 10 Most Demanded Skills")
plt.xlabel("Skills")
plt.ylabel("Number of Job Postings")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.show()