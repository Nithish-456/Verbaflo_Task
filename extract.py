import PyPDF2

def extract_text_from_pdf(pdf_file):
    pdf_file_obj = open(pdf_file, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    pdf_file_obj.close()
    return text

pdf_file = 'My_Profile.pdf' 
text = extract_text_from_pdf(pdf_file)
print(text)

import re

def extract_info(text):
    # Extract Contact Information
    contact_pattern = r'Contact\n([\s\S]*?)Top Skills'
    contact_match = re.search(contact_pattern, text, re.DOTALL)
    contact_info = contact_match.group(1).strip() if contact_match else None

    # Extract Top Skills
    skills_pattern = r'Top Skills\n([\s\S]*?)Certifications'
    skills_match = re.search(skills_pattern, text, re.DOTALL)
    skills = skills_match.group(1).strip() if skills_match else None

    # Extract Certifications
    certifications_pattern = r'Certifications\n([\s\S]*?)Publications'
    certifications_match = re.search(certifications_pattern, text, re.DOTALL)
    certifications = certifications_match.group(1).strip() if certifications_match else None

    # Extract Publications
    publications_pattern = r'Publications\n([\s\S]*?)Experience'
    publications_match = re.search(publications_pattern, text, re.DOTALL)
    publications = publications_match.group(1).strip() if publications_match else None

    # Extract Experience
    experience_pattern = r'Experience\n([\s\S]*?)Education'
    experience_match = re.search(experience_pattern, text, re.DOTALL)
    experience = experience_match.group(1).strip() if experience_match else None

    # Extract Education
    education_pattern = r'Education\n([\s\S]*?$)'
    education_match = re.search(education_pattern, text, re.DOTALL)
    education = education_match.group(1).strip() if education_match else None

    # Extract Name and Title
    name_title_pattern = r'([A-Z][a-z]+ [A-Z][a-z]+)\n([A-Za-z\s]+)'
    name_title_match = re.search(name_title_pattern, text)
    name = name_title_match.group(1) if name_title_match else None
    title = name_title_match.group(2) if name_title_match else None

    # Print the extracted information in a structured manner
    print("Name:", name)
    print("Title:", title)
    print("\nContact Information:")
    print(contact_info)
    print("\nTop Skills:")
    print(skills)
    print("\nCertifications:")
    print(certifications)
    print("\nPublications:")
    print(publications)
    print("\nExperience:")
    print(experience)
    print("\nEducation:")
    print(education)

info = extract_info(text)
print(info)


    