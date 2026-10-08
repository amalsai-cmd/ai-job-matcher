from resume_parser import analyze_resume


# Put your actual uploaded resume filename here
pdf_path = r"C:\Users\amale\Documents\ai-job-matcher\backend\uploads\resumes\46c9a587-cabc-4839-a201-a5e578aae493_Murari_Resume.pdf"


# Analyze resume
result = analyze_resume(pdf_path)


# =========================
# Display Resume Analysis
# =========================

print("\n========================================")
print("          RESUME ANALYSIS")
print("========================================")


print("\nName:")
print(result["name"])


print("\nSkills:")

for skill in result["skills"]:
    print(" -", skill)


print("\nEducation:")

for item in result["education"]:
    print(" -", item)


print("\nExperience:")

for item in result["experience"]:
    print(" -", item)


print("\nProjects:")

for item in result["projects"]:
    print(" -", item)


print("\nCertifications:")

for item in result["certifications"]:
    print(" -", item)


print("\n========================================")