# from PIL import Image
# import pytesseract
# import cv2

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def image_to_text(image_path):

#     img = cv2.imread(image_path)


#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


#     extracted_text = pytesseract.image_to_string(img_rgb)

#     return extracted_text

# if __name__ == "__main__":
#     path = 'Love.png'
#     text = image_to_text(path)
#     print("Extracted Text:\n", text)





import os
from flask import Flask, render_template, request, send_file
import pdfplumber
import csv
from werkzeug.utils import secure_filename
import google.generativeai as genai
from fpdf import FPDF  # pip install fpdf

# Set your API key
os.environ["GOOGLE_API_KEY"] = 'AIzaSyBIYGvbpkLuHvrNM0YSi8D5xNn-FO8cSnQ'
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-2.0-flash")

# def Question_answer_generator(input_text):
#     prompt = f"""
#     You are an AI assistant helping the user generate questions based on the following text:
#     '{input_text}'
#     Please generate a number of questions such that all informations are extracted from the {input_text}. 
#     Each question should have:
#     - Generate clear questions that cover all factual information in the text.
#     - Each question must be accompanied by its correct answer and the type of answer (e.g., Person, Date, Organization, Location, Numeric, etc.).
#     - DO NOT add any information not present in the original text.
#     - DO NOT generate explanatory or problem-solving questions.
#     - Only extract what is explicitly stated.
#     Format:
#     ## Question
#     Question: [question]
#     Answer: [correct answer] [Answer Type]
#     """
#     response = model.generate_content(prompt).text.strip()
#     return response


# import re

# def extract_questions(text_output):
#     """
#     Extracts only the questions from the structured text output.
#     """
#     questions = re.findall(r"Question:\s*(.+)", text_output)

#     return questions

# def extract_answer(text_output):
#     """
#     Extracts only the answers from the structured text output.
#     """
#     answers = re.findall(r"Answer:\s*(.+)", text_output)
    
#     return answers


def Question_answer_generator(input_text,text):
    prompt = f"""
    You are an AI assistant helping the user to generate questions based on the following text:
    '{input_text}'
    Please generate a questions that solves the user problem i.e {text}. 
    Each question should have:
    - A clear question
    - The correct answer clearly indicated
    Format:
    ## Question
    Question: [question]
    Answer: [correct answer]
    """
    response = model.generate_content(prompt).text.strip()
    return response




base_text= """In the heart of the quaint village of Eldermere, a mysterious tree stood tall in the town square. Its 
gnarled branches bore fruits that resembled pears, but with an unusual twist: they seemed to shimmer 
with a golden hue. The villagers affectionately named it the "Shakespear" tree, believing it held magical 
properties. 
Legend had it that anyone who tasted a Shakespear would gain a glimpse into their future. Curiosity 
spread like wildfire, and soon, villagers flocked to the tree, eager for a taste of destiny. Young Emma, a 
spirited girl with dreams of becoming a writer, felt an undeniable pull toward the shimmering fruit. 
One crisp autumn morning, she approached the tree, heart racing. With a deep breath, she plucked a 
Shakespear and took a bite. Instantly, a whirlwind of visions enveloped her. She saw herself standing on a 
grand stage, the applause of a thousand voices echoing in her ears. In another glimpse, she wandered 
through enchanted forests, her stories coming to life. 
Determined to fulfill these dreams, Emma spent every spare moment writing. The villagers, inspired by 
her passion, began sharing their own tales. The square buzzed with creativity, and soon, Eldermere 
became a hub of storytelling. 
As the seasons changed, Emma’s words took flight. She published her first book, a collection of 
enchanting stories, and it captured the hearts of many beyond Eldermere. The Shakespear tree 
continued to stand, its golden pears glimmering, a reminder that dreams, when nurtured, could blossom 
into reality. 
And so, in the embrace of magic and creativity, the legacy of the Shakespear lived on, inspiring 
generations to reach for their dreams. """ 


text = """
I want 1 fill in the blanks questions
"""
questions = Question_answer_generator(base_text,text)
print(questions)

# questions_only = extract_questions(questions)
# answers_only = extract_answer(questions)

# for q in questions_only:
#     print(q)

# for a in answers_only:
#     print(a)



# text = """generate 5 questions from NCERT decimal chapter"""
# fill_blanks = Question_fill_blanks_generator(text)
# print(fill_blanks)

# prompt = """"Prepare me 5 questions from NCERT Decimal chapter."

# Output format (in JSON):
# {
#   "Ques": <number of questions>,
#   "Chapter": "<chapter name>",
#   "Source": "<book name or source>"
# }

# If any value is not explicitly given, infer it based on context or leave it as null.
# """

# response = model.generate_content(prompt).text.strip()

# print(response)



