import pandas as pd
import ast
from collections import Counter
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt


# Load dataset
df = pd.read_csv("data/all_job_post.csv")


# Convert skill text into Python lists
df["job_skill_set"] = df["job_skill_set"].apply(ast.literal_eval)


# Clean skill names
df["job_skill_set"] = df["job_skill_set"].apply(
    lambda skills: [skill.lower().strip() for skill in skills]
)


# Count skill pairs
pair_counts = Counter()

for skills in df["job_skill_set"]:

    skills = sorted(set(skills))

    pairs = combinations(skills, 2)

    for pair in pairs:
        pair_counts[pair] += 1


# Take only the strongest relationships
top_pairs = pair_counts.most_common(20)


# Create network
G = nx.Graph()


# Add skills and connections
for (skill1, skill2), count in top_pairs:

    G.add_edge(
        skill1,
        skill2,
        weight=count
    )


# Draw network
plt.figure(figsize=(14, 10))

pos = nx.spring_layout(
    G,
    seed=42
)


nx.draw_networkx(
    G,
    pos,
    with_labels=True,
    node_size=2500,
    font_size=9,
    width=1.5
)


plt.title(
    "Top Skill Co-occurrence Network"
)

plt.axis("off")

plt.tight_layout()

plt.show()