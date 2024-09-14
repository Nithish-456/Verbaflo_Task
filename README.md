# LinkedIn Resume Extractor and Generator

Welcome to the LinkedIn Resume Extractor and Generator! This project allows you to extract text from LinkedIn PDF resumes, process it to identify key sections, and generate a beautifully formatted HTML resume using advanced language models.

## Approach 🚀

1. **Text Extraction**: We use PyPDF2 to extract the entire text from the provided PDF.
2. **Section Extraction**: Regular expressions are employed to derive the following sections from the extracted text:
   - Name and Title
   - Contact
   - Top Skills
   - Certifications
   - Publications
   - Education
   - Experience
3. **Resume Generation**: Using the OpenAI API, we generate an HTML resume based on predefined templates located in the `templates` folder of this repository. Alternatively, you can design your own templates.
4. **Performance Considerations**: To address latency issues with the OpenAI API, we provide an option to use the Groq API, which offers high-performance language processing with an inference rate of approximately 1200 tokens per second.

## Repository Structure 📁

- **`extract.py`**: Contains the regular expressions validators to extract sections from the resume.
- **`table.py`**: Formats the extracted information into a tabular structure.
- **`app.py`**: The Flask application that integrates with the OpenAI API to generate the HTML resume.
- **`app1.py`**: An alternative Flask application using the Groq API for faster processing.

