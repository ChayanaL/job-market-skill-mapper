import pandas as pd
import ast
from collections import Counter
from itertools import combinations
import matplotlib.pyplot as plt


# Load dataset
df = pd.read_csv("data/all_job_post.csv")


# Convert skill text into Python lists
df["job_skill_set"] = df["job_skill_set"].apply(ast.literal_eval)


# Clean skill names
df["job_skill_set"] = df["job_skill_set"].apply(
    lambda skills: [skill.lower().strip() for skill in skills]
)


# Store all skill pairs
skill_pairs = []


# Process each job
for skills in df["job_skill_set"]:

    # Remove duplicate skills within the same job
    skills = sorted(set(skills))

    # Create every possible pair of skills
    pairs = combinations(skills, 2)

    for pair in pairs:
        skill_pairs.append(pair)


# Count how often each pair appears
pair_counts = Counter(skill_pairs)


# Get top 10 skill combinations
top_pairs = pair_counts.most_common(10)

print("\nTop 10 Skill Combinations:")

for pair, count in top_pairs:

    print(
        f"{pair[0]} + {pair[1]} : {count} job postings"
    )


# Prepare data for chart
pair_names = [
    f"{pair[0]} + {pair[1]}"
    for pair, count in top_pairs
]

pair_counts_values = [
    count
    for pair, count in top_pairs
]


# Create bar chart
plt.figure(figsize=(12, 6))

plt.bar(pair_names, pair_counts_values)

plt.title("Top 10 Skill Combinations")
plt.xlabel("Skill Combination")
plt.ylabel("Number of Job Postings")

plt.xticks(rotation=60, ha="right")

plt.tight_layout()

plt.show()

# Find skills commonly paired with a selected skill

selected_skill = input(
    "\nEnter a skill to find related skills: "
).lower().strip()

related_skills = []

for pair, count in pair_counts.items():

    if selected_skill == pair[0]:
        related_skills.append((pair[1], count))

    elif selected_skill == pair[1]:
        related_skills.append((pair[0], count))


related_skills.sort(
    key=lambda x: x[1],
    reverse=True
)


print(
    f"\nSkills commonly required with '{selected_skill}':"
)

if related_skills:

    for skill, count in related_skills[:10]:

        print(
            f"- {skill} : "
            f"{count} job postings"
        )

else:

    print("Skill not found.")