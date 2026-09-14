import pandas as pd
import ast

# Load dataset
df = pd.read_csv("data/all_job_post.csv")

# Convert job_skill_set from text to Python lists
df["job_skill_set"] = df["job_skill_set"].apply(ast.literal_eval)

# Clean skill names
df["job_skill_set"] = df["job_skill_set"].apply(
    lambda skills: [skill.lower().strip() for skill in skills]
)

# Ask user for a job title
job_title = input("\nEnter the job title: ")

# Find the job
matching_jobs = df[
    df["job_title"].str.lower() == job_title.lower()
]

if matching_jobs.empty:
    print("Job title not found.")
    exit()

# Select first matching job
job = matching_jobs.iloc[0]

# Required skills
required_skills = set(job["job_skill_set"])

print("\nSelected Job:", job["job_title"])
print("Category:", job["category"])

print("\nRequired Skills:")

for skill in sorted(required_skills):
    print("-", skill)

# Ask user for their skills
user_input = input(
    "\nEnter your skills separated by commas: "
)

user_skills = {
    skill.strip().lower()
    for skill in user_input.split(",")
}

# Find matched and missing skills
matched_skills = required_skills.intersection(user_skills)
missing_skills = required_skills - user_skills

# Calculate match percentage
match_percentage = (
    len(matched_skills) / len(required_skills)
) * 100

print("\nMatched Skills:")

for skill in sorted(matched_skills):
    print("-", skill)

print("\nMissing Skills:")

for skill in sorted(missing_skills):
    print("-", skill)


print(f"\nSkill Match: {match_percentage:.2f}%")
# Calculate skill demand within the selected job category
category_jobs = df[df["category"] == job["category"]]

category_skill_counts = {}

for skills in category_jobs["job_skill_set"]:
    for skill in skills:
        category_skill_counts[skill] = (
            category_skill_counts.get(skill, 0) + 1
        )

# Rank missing skills by demand
prioritized_skills = sorted(
    missing_skills,
    key=lambda skill: category_skill_counts.get(skill, 0),
    reverse=True
)

print("\nPriority Skills to Learn:")

# Find highest skill demand
highest_demand = max(
    category_skill_counts.get(skill, 0)
    for skill in missing_skills
)

for skill in prioritized_skills:

    demand = category_skill_counts.get(skill, 0)

    if demand >= highest_demand * 0.7:
        priority = "HIGH"

    elif demand >= highest_demand * 0.4:
        priority = "MEDIUM"

    else:
        priority = "LOW"

    print(
        f"- {skill} | "
        f"Demand: {demand} jobs | "
        f"Priority: {priority}"
    )