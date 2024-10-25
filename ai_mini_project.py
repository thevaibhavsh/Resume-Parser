# -*- coding: utf-8 -*-
"""AI MINI PROJECT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1--Cc7qEWXVZV4xG7ufUm_yk94keAdo9V
"""

import re
from pdfminer.high_level import extract_text
import spacy
from spacy.matcher import Matcher

def extract_text_from_pdf(pdf_path):
    return extract_text('/content/resume.pdf')

def extract_contact_number_from_resume(text):
    contact_number = None

    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()
    return contact_number

def extract_email_from_resume(text):
    email = None

    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()
    return email

def extract_skills_from_resume(text, skills_list):
    skills = []

    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)

    return skills

def extract_education_from_resume(text):
    education = []

    pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
    matches = re.findall(pattern, text)
    for match in matches:
        education.append(match.strip())
    return education

def extract_name(resume_text):
    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]
    ]

    for pattern in patterns:
        matcher.add('NAME', patterns=[pattern])

    doc = nlp(resume_text)
    matches = matcher(doc)

    for match_id, start, end in matches:
        span = doc[start:end]
        return span.text
    return None

def extract_college_name(text):
    lines = text.split('\n')
    college_pattern = r"(?i).*college.*|(?i).*University.*"
    college_names = []

    for line in lines:
        if re.search(college_pattern, line):
            college_names.append(line.strip())
    return college_names

def extract_designation(text):
    designation_pattern = r"\b(?:Data Scientist|Project Manager|Product Manager|Business Analyst|Software Developer|Engineer|Analyst|Consultant|Manager)\b"
    match = re.search(designation_pattern, text, re.IGNORECASE)
    return match.group() if match else None

def count_number_of_pages(pdf_path):
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_path)
    return len(reader.pages)

def extract_experience(text):
    experience_pattern = r"(?i)(?:\d{1,2}\s?(?:years|yrs|year|yr)|(?:\d{1,2}\s?(?:months|mo|month|m)))"
    matches = re.findall(experience_pattern, text)
    return matches if matches else None

if __name__ == '__main__':

    resume_paths = [r"/content/resume.pdf"]

    for resume_path in resume_paths:
        text = extract_text_from_pdf(resume_path)

        name = extract_name(text)
        if name:
            print("Name:", name)
        else:
            print("Name not found")

        contact_number = extract_contact_number_from_resume(text)
        if contact_number:
            print("Contact Number:", contact_number)
        else:
            print("Contact Number not found")

        email = extract_email_from_resume(text)
        if email:
            print("Email:", email)
        else:
            print("Email not found")

        skills_list = ['Python', 'Java', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau']
        extracted_skills = extract_skills_from_resume(text, skills_list)
        if extracted_skills:
            print("Skills:", extracted_skills)
        else:
            print("No skills found")

        extracted_education = extract_education_from_resume(text)
        if extracted_education:
            print("Education / Degree:", extracted_education)
        else:
            print("No education information found")

        college_name = extract_college_name(text)
        if college_name:
            print("College:", college_name)
        else:
            print("College name not found.")

        designation = extract_designation(text)
        print("Designation:", designation if designation else "Designation not found")

        experience = extract_experience(text)
        print("Experience:", experience if experience else "NIL(Fresher)")

        number_of_pages = count_number_of_pages(resume_path)
        print("Number of Pages:", number_of_pages)