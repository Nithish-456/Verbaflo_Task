import re
import PyPDF2
from tabulate import tabulate

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

def extract_info_table(text):
    # Extract Name
    name_pattern = r'([A-Z][a-z]+ [A-Z][a-z]+)'
    name_match = re.search(name_pattern, text)
    name = name_match.group(0) if name_match else None

    # Extract Headlines
    headlines_pattern = r'AIML Enthusiastic.*?Student at Kalasalingam University'
    headlines_match = re.search(headlines_pattern, text, re.DOTALL)
    headlines = headlines_match.group(0) if headlines_match else None

    # Extract Professional Summary
    summary_pattern = r'Summary\n([\s\S]*?)Experience'
    summary_match = re.search(summary_pattern, text, re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else None

    # Extract Contact Information
    contact_pattern = r'Contact\n([\s\S]*?)Top Skills'
    contact_match = re.search(contact_pattern, text, re.DOTALL)
    contact_info = contact_match.group(1).strip() if contact_match else None

    # Extract Education
    education_pattern = r'Education\n([\s\S]*?)Experience'
    education_match = re.search(education_pattern, text, re.DOTALL)
    education = education_match.group(1).strip() if education_match else None

    # Extract Experience
    experience_pattern = r'Experience\n([\s\S]*?)Education'
    experience_match = re.search(experience_pattern, text, re.DOTALL)
    experience = experience_match.group(1).strip() if experience_match else None

    # Extract Top Skills
    skills_pattern = r'Top Skills\n([\s\S]*?)Languages'
    skills_match = re.search(skills_pattern, text, re.DOTALL)
    skills = skills_match.group(1).strip() if skills_match else None

    # Extract Languages
    languages_pattern = r'Languages\n([\s\S]*?)Certifications'
    languages_match = re.search(languages_pattern, text, re.DOTALL)
    languages = languages_match.group(1).strip() if languages_match else None

    # Extract Certifications
    certifications_pattern = r'Certifications\n([\s\S]*?)Publications'
    certifications_match = re.search(certifications_pattern, text, re.DOTALL)
    certifications = certifications_match.group(1).strip() if certifications_match else None

    # Extract Publications
    publications_pattern = r'Publications\n([\s\S]*?$)'
    publications_match = re.search(publications_pattern, text, re.DOTALL)
    publications = publications_match.group(1).strip() if publications_match else None

    # Create a table with the extracted information
    table = [
        ["Name", name],
        ["Headlines", headlines],
        ["Professional Summary", summary],
        ["Contact", contact_info],
        ["Education", education],
        ["Experience", experience],
        ["Top Skills", skills],
        ["Languages", languages],
        ["Certifications", certifications],
        ["Publications", publications]
    ]

    # Print the table
    print(tabulate(table, headers="keys", tablefmt="grid"))

extract_info_table(text)