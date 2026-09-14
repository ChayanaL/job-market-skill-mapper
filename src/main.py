import subprocess
import sys

print("======================================")
print("   JOB MARKET SKILL MAPPER")
print("======================================")

print("\nChoose an option:")

print("1. Skill Analysis")
print("2. Similar Job Search")
print("3. Job Clustering")
print("4. Skill Gap Analysis")
print("5. Career Recommendations")
print("6. Skill Co-occurrence Analysis")
print("7. Skill Network")
print("0. Exit")


choice = input("\nEnter your choice: ")


if choice == "1":
    print("\nOpening Skill Analysis...")
    subprocess.run([sys.executable, "src/data_loader.py"])

elif choice == "2":
    print("\nOpening Similar Job Search...")
    subprocess.run([sys.executable, "src/text_analysis.py"])

elif choice == "3":
    print("\nOpening Job Clustering...")
    subprocess.run([sys.executable, "src/job_clustering.py"])

elif choice == "4":
    print("\nOpening Skill Gap Analysis...")
    subprocess.run([sys.executable, "src/skill_gap.py"])

elif choice == "5":
    print("\nOpening Career Recommendations...")
    subprocess.run([sys.executable, "src/career_recommendation.py"])

elif choice == "6":
    print("\nOpening Skill Co-occurrence Analysis...")
    subprocess.run([sys.executable, "src/skill_cooccurrence.py"])

elif choice == "7":
    print("\nOpening Skill Network...")
    subprocess.run([sys.executable, "src/skill_network.py"])

elif choice == "0":
    print("\nExiting program...")

else:
    print("\nInvalid choice. Please select a number from 0 to 7.")