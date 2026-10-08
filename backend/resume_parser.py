from pypdf import PdfReader
import re


# =========================
# Extract Text From PDF
# =========================

def extract_text_from_pdf(file_path):
    """
    Extract all readable text from a PDF resume.
    """

    reader = PdfReader(file_path)

    extracted_text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_text += page_text + "\n"

    return extracted_text


# =========================
# Extract Skills
# =========================

def extract_skills(text):
    """
    Find common technical skills inside resume text.
    """

    skills_database = [
        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "React.js",
        "Node.js",
        "Express.js",
        "Django",
        "FastAPI",
        "Spring Boot",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "Git",
        "GitHub",
        "Microsoft Azure",
        "AWS",
        "Docker",
        "REST API",
        "REST APIs",
        "Machine Learning",
        "Artificial Intelligence",
        "Data Science",
        "OOP",
        "Object Oriented Programming",
    ]

    text_lower = text.lower()

    found_skills = []

    for skill in skills_database:

        if skill.lower() in text_lower:

            if skill not in found_skills:
                found_skills.append(skill)

    return found_skills


# =========================
# Find Resume Section
# =========================

def extract_section(text, section_names, next_section_names):
    """
    Extract text between one resume section heading
    and the next section heading.
    """

    lines = text.splitlines()

    start_index = None

    # Find starting section
    for index, line in enumerate(lines):

        clean_line = line.strip().lower()

        if clean_line in section_names:
            start_index = index + 1
            break

    if start_index is None:
        return []

    end_index = len(lines)

    # Find next section
    for index in range(start_index, len(lines)):

        clean_line = lines[index].strip().lower()

        if clean_line in next_section_names:
            end_index = index
            break

    section_lines = []

    for line in lines[start_index:end_index]:

        clean_line = line.strip()

        if clean_line:
            section_lines.append(clean_line)

    return section_lines


# =========================
# Extract Education
# =========================

def extract_education(text):
    """
    Extract education section from resume.
    """

    education_sections = [
        "education",
        "academic background",
        "educational background",
        "academics"
    ]

    next_sections = [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships",
        "projects",
        "certifications",
        "skills",
        "technical skills",
        "achievements"
    ]

    return extract_section(
        text,
        education_sections,
        next_sections
    )


# =========================
# Extract Experience
# =========================

def extract_experience(text):
    """
    Extract experience section from resume.
    """

    experience_sections = [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships"
    ]

    next_sections = [
        "education",
        "projects",
        "certifications",
        "skills",
        "technical skills",
        "achievements"
    ]

    return extract_section(
        text,
        experience_sections,
        next_sections
    )


# =========================
# Extract Projects
# =========================

def extract_projects(text):
    """
    Extract projects section from resume.
    """

    project_sections = [
        "projects",
        "academic projects",
        "personal projects",
        "project"
    ]

    next_sections = [
        "education",
        "experience",
        "work experience",
        "certifications",
        "skills",
        "technical skills",
        "achievements"
    ]

    return extract_section(
        text,
        project_sections,
        next_sections
    )


# =========================
# Extract Certifications
# =========================

def extract_certifications(text):
    certification_sections = ["certifications", "certificates", "certification"]

    next_sections = [
        "education",
        "experience",
        "work experience",
        "projects",
        "skills",
        "technical skills",
        "achievements",
        "languages",
        "language"
    ]

    return extract_section(text, certification_sections, next_sections)
# =========================
# Extract Name
# =========================

def extract_name(text):
    """
    Try to identify the candidate's name.

    Usually the first meaningful line of a resume
    contains the candidate's name.
    """

    lines = text.splitlines()

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        # Ignore common resume headings
        ignored_words = [
            "resume",
            "curriculum vitae",
            "cv",
            "profile",
            "objective"
        ]

        if clean_line.lower() in ignored_words:
            continue

        # Avoid returning very long lines
        if len(clean_line) <= 60:

            return clean_line

    return "Not detected"


# =========================
# Analyze Complete Resume
# =========================

def analyze_resume(file_path):
    """
    Extract and analyze the complete resume.
    """

    text = extract_text_from_pdf(file_path)

    skills = extract_skills(text)

    education = extract_education(text)

    experience = extract_experience(text)

    projects = extract_projects(text)

    certifications = extract_certifications(text)

    name = extract_name(text)

    return {
        "name": name,
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
        "text": text
    }