import os
import requests
from flask import Flask, request, render_template_string
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# API key (replace with your own API key)
api_key = os.environ.get('GROQ_API_KEY')

# Function to extract relevant sections from PDF file using Groq API
def extract_sections(pdf_file):
    url = "https://api.groq.io/v1/resume"
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {"file": pdf_file}
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")  # Log error message
        return None

# Function to generate HTML resume
def generate_resume(sections):
    html = """
    <html>
        <head>
            <title>{name}</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }
                .section {
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body>
            <h1>{name}</h1>
            <p>{summary}</p>
            <h2>Contact:</h2>
            <p>{contact}</p>
            <h2>Experience:</h2>
            <ul>
                {experience}
            </ul>
            <h2>Top Skills:</h2>
            <ul>
                {top_skills}
            </ul>
            <h2>Languages:</h2>
            <ul>
                {languages}
            </ul>
            <h2>Certifications:</h2>
            <ul>
                {certifications}
            </ul>
            <h2>Publications:</h2>
            <ul>
                {publications}
            </ul>
        </body>
    </html>
    """

    experience_list = []
    top_skills_list = []
    languages_list = []
    certifications_list = []
    publications_list = []

    for section in sections:
        if 'experience' in section and section['experience']:
            experience_list.extend([f"<li>{item}</li>" for item in section['experience'].split('\n')])
        if 'top_skills' in section and section['top_skills']:
            top_skills_list.extend([f"<li>{item}</li>" for item in section['top_skills'].split('\n')])
        if 'languages' in section and section['languages']:
            languages_list.extend([f"<li>{item}</li>" for item in section['languages'].split('\n')])
        if 'certifications' in section and section['certifications']:
            certifications_list.extend([f"<li>{item}</li>" for item in section['certifications'].split('\n')])
        if 'publications' in section and section['publications']:
            publications_list.extend([f"<li>{item}</li>" for item in section['publications'].split('\n')])

    html = html.format(
        name=sections.get('name', 'No Name'),
        summary=sections.get('summary', 'No Summary'),
        contact=sections.get('contact', 'No Contact'),
        experience='\n'.join(experience_list),
        top_skills='\n'.join(top_skills_list),
        languages='\n'.join(languages_list),
        certifications='\n'.join(certifications_list),
        publications='\n'.join(publications_list)
    )

    return html

# Route for displaying the upload form
@app.route('/')
def upload_form():
    return '''
    <!doctype html>
    <title>Upload LinkedIn PDF</title>
    <h1>Upload your LinkedIn PDF resume</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="pdf_file">
      <input type="submit" value="Upload">
    </form>
    '''

# Route for uploading PDF file and generating resume
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return "No file part"
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return "No selected file"
    sections = extract_sections(pdf_file)
    if sections:
        html = generate_resume(sections)
        return render_template_string(html)
    else:
        return "Error: Unable to extract resume information from PDF file"

if __name__ == '__main__':
    app.run(debug=True)
