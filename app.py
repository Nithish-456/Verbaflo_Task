import re
import fitz 
from openai import OpenAI
from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# Function to summarize content using OpenAI API
def openai_summarize(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can also use "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a summarizer."},
            {"role": "user", "content": f"Summarize the following content:\n\n{text}"}
        ],
        max_tokens=150,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()
# Function to parse the extracted text into sections
def parse_resume(text):
    resume_data = {}

    # Use regex to extract Name (assuming it's at the top of the resume)
    name_match = re.search(r'\b([A-Z][a-z]*\s[A-Z][a-z]*)\b', text)
    resume_data['name'] = name_match.group(0) if name_match else 'No name found'

    # Extract headline (based on common structure of LinkedIn resumes)
    headline_match = re.search(r'(?:AIML Enthusiastic|.*\|\|.*)', text)
    resume_data['headline'] = headline_match.group(0) if headline_match else 'No headline found'

    # Extract summary and use OpenAI to enhance it
    summary_match = re.search(r'Summary\s+(.*?)\s+Experience', text, re.S)
    summary_raw = summary_match.group(1).strip() if summary_match else 'No summary found'
    resume_data['summary'] = openai_summarize(summary_raw) if summary_match else 'No summary found'

    # Extract contact information
    contact_match = re.search(r'Contact\s+(.*?)\s+Top Skills', text, re.S)
    resume_data['contact'] = contact_match.group(1).strip() if contact_match else 'No contact information found'

    # Extract experience
    experience_match = re.search(r'Experience\s+(.*?)\s+Education', text, re.S)
    resume_data['experience'] = experience_match.group(1).strip() if experience_match else 'No experience found'

    # Extract top skills
    skills_match = re.search(r'Top Skills\s+(.*?)\s+Languages', text, re.S)
    resume_data['skills'] = skills_match.group(1).strip() if skills_match else 'No skills found'

    # Extract languages
    languages_match = re.search(r'Languages\s+(.*?)\s+Certifications', text, re.S)
    resume_data['languages'] = languages_match.group(1).strip() if languages_match else 'No languages found'

    # Extract certifications
    certifications_match = re.search(r'Certifications\s+(.*?)\s+Publications', text, re.S)
    resume_data['certifications'] = certifications_match.group(1).strip() if certifications_match else 'No certifications found'

    # Extract publications
    publications_match = re.search(r'Publications\s+(.*?)\s+Contact', text, re.S)
    resume_data['publications'] = publications_match.group(1).strip() if publications_match else 'No publications found'

    return resume_data

# Route to upload PDF
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and file.filename.endswith('.pdf'):
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            return redirect(url_for('display_resume', filename=file.filename))
    return '''
    <!doctype html>
    <title>Upload LinkedIn PDF</title>
    <h1>Upload your LinkedIn PDF resume</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/resume/<filename>')
def display_resume(filename):
    file_path = os.path.join('uploads', filename)
    text = extract_text_from_pdf(file_path)
    resume_data = parse_resume(text)
    
    # Render the extracted information as HTML
    return render_template('resume.html', resume=resume_data)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
