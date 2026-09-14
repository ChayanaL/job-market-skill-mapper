import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load dataset
df = pd.read_csv("data/all_job_post.csv")

# Replace missing descriptions
df["job_description"] = df["job_description"].fillna("")

# Convert job descriptions into TF-IDF vectors
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=1000
)

tfidf_matrix = vectorizer.fit_transform(df["job_description"])
print("\nTesting different numbers of clusters:")

for k in range(2, 9):

    kmeans_test = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans_test.fit_predict(tfidf_matrix)

    score = silhouette_score(tfidf_matrix, labels)

    print(f"K = {k}  |  Silhouette Score = {score:.3f}")

# Create K-Means model
kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

# Assign each job to a cluster
df["cluster"] = kmeans.fit_predict(tfidf_matrix)

# Display cluster information
print("\nNumber of jobs in each cluster:")

print(df["cluster"].value_counts().sort_index())

# Display some jobs from each cluster
print("\nSample jobs from each cluster:")

for cluster in sorted(df["cluster"].unique()):

    print(f"\nCluster {cluster}:")

    cluster_jobs = df[df["cluster"] == cluster]

    for title in cluster_jobs["job_title"].head(5):
        print(" -", title)
print("\nCluster Summary:")

for cluster in sorted(df["cluster"].unique()):

    cluster_jobs = df[df["cluster"] == cluster]

    print(f"\nCluster {cluster}")
    print("Number of jobs:", len(cluster_jobs))

    print("Common job titles:")

    title_counts = cluster_jobs["job_title"].value_counts()

    for title, count in title_counts.head(5).items():
        print(f"  - {title}: {count}")