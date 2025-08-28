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

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULTS_FOLDER'] = 'results/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



import fitz  # PyMuPDF
import os
import cv2
import pytesseract

# ——— CONFIG ———
OUTPUT_FOLDER = 'output folder'
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# —————————

def extract_images_from_pdf(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    saved_files = []

    for page_num in range(len(doc)):
        for img_index, img in enumerate(doc.get_page_images(page_num, full=True), start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            ext = base_image["ext"]
            filename = f"page{page_num+1}_img{img_index}.{ext}"
            filepath = os.path.join(output_folder, filename)

            with open(filepath, "wb") as f:
                f.write(base_image["image"])
            # print(f"Saved image: {filename}")
            saved_files.append(filepath)

    # print("Extraction complete.")
    return saved_files

def image_to_text(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot read image {image_path}")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return pytesseract.image_to_string(img_rgb).strip()

def extract_code_from_pdf(pdf_path, output_folder):
    images = extract_images_from_pdf(pdf_path, output_folder)
    all_texts = {}

    for img_path in images:
        # print(f"\n--- OCR on {os.path.basename(img_path)} ---")
        try:
            text = image_to_text(img_path)
            all_texts[img_path] = text or "[No text found]"
            print(all_texts[img_path])
        except Exception as e:
            print(f"Error processing {img_path}: {e}")

    return all_texts

# if __name__ == "__main__":
#     extracted = extract_code_from_pdf(PDF_PATH, OUTPUT_FOLDER)
   
#     out_txt = os.path.join(OUTPUT_FOLDER, "ocr_results.txt")
#     with open(out_txt, "w", encoding="utf-8") as f:
#         for img, txt in extracted.items():
#             f.write(f"--- {os.path.basename(img)} ---\n{txt}\n\n")




def extract_text_from_file(file_path):
    ext = file_path.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        with pdfplumber.open(file_path) as pdf:
            text = ''.join([page.extract_text() for page in pdf.pages])
        return text
    elif ext == 'txt':
        with open(file_path, 'r') as file:
            return file.read()
    return None



def process_input(file_path):
    text = extract_text_from_file(file_path)
    if text:
        return text
    # If no text, fallback to image OCR
    return extract_code_from_pdf(file_path, OUTPUT_FOLDER)



def Question_mcqs_generator(input_text, num_questions, difficulty):
    prompt = f"""
    You are an AI assistant helping the user generate multiple-choice questions (MCQs) based on the following text:
    '{input_text}'
    Please generate {num_questions} MCQs from the text having difficulty level {difficulty}. Each question should have:
    - A clear question
    - Four answer options (labeled A, B, C, D)
    - The correct answer clearly indicated
    Format:
    ## MCQ
    Question: [question]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]
    Correct Answer: [correct option] [option [correct option]]
    """
    response = model.generate_content(prompt).text.strip()
    return response

def Question_answer_generator(input_text, difficulty, short_questions, inter_questions, long_questions):
    prompt = f"""
    You are an AI assistant helping the user generate questions based on the following text:
    '{input_text}'
    Please generate {short_questions} questions having answer in the range of 30 to 50 words, {inter_questions} questions having answer in the range of 100 to 150 words and {long_questions} questions having answer in the range of 200 to 250 words from the text having difficulty level {difficulty}. Each question should have:
    - A clear question
    - The correct answer clearly indicated
    Format:
    ## Question
    Question: [question]
    Answer: [correct answer]
    """
    response = model.generate_content(prompt).text.strip()
    return response

def Question_true_false_generator(input_text, num_questions, difficulty):
    prompt = f"""
    You are an AI assistant helping the user generate True and False questions (True-False) based on the following text:
    '{input_text}'
    Please generate {num_questions} True and False Questions from the text having difficulty level {difficulty}. Each question should have:
    - A clear question
    - Two answer options (labeled A, B)
    - The correct answer clearly indicated
    Format:
    ## TRUE_FALSE
    Question: [question]
    A) [option A]
    B) [option B]
    Correct Answer: [correct option] [option [correct option]]
    """
    response = model.generate_content(prompt).text.strip()
    return response


def Question_fill_blanks_generator(input_text, num_questions, difficulty):
    prompt = f"""
    You are an AI assistant helping the user generate fill in the blanks questions (Fill-in-the-blanks) based on the following text:
    '{input_text}'
    Please generate {num_questions} fill in the blanks Questions from the text having difficulty level {difficulty}. Each question should have:
    - A clear question
    - Two answer options (labeled A, B, C, D)
    - The correct answer clearly indicated
    Format:
    ## MULTIPLE_CHOICE
    Question: [question]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]
    Correct Answer: [correct option] [option [correct option]]
    """
    response = model.generate_content(prompt).text.strip()
    return response


def Question_answer_prompt_generator(input_text,text):
    prompt = f"""
    You are an AI assistant helping the user to generate questions based on the following text:
    '{input_text}'
    Please generate a questions that solves the user problem i.e {text}. 
    Each question should have:
    - A clear question
    - The correct answer clearly indicated
    Format:
    ## QUES
    Question: [question]
    Answer: [correct answer]

  

    """
    response = model.generate_content(prompt).text.strip()
    idx = response.find('#')
    if (idx!= -1):
        clean = response[idx:]
    else:
        clean = response
    return clean



@app.route('/')
def index():
    return render_template('mainPage.html')

@app.route('/generate', methods=['POST'])
def generate_mcqs():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)


        text = process_input(file_path)

        
        

        if text:
            prompt = str(request.form['prompt'])
            if(prompt  and prompt.upper() != 'NULL'):
                p_questions = Question_answer_prompt_generator(text,prompt)
                print(p_questions)
                generated_file = render_template('prompt.html', p_questions=p_questions)
                

            else:
                paper_type = str(request.form['paper_type'])
                if(paper_type=="Objective"):
                    difficulty = str(request.form['difficulty'])
                    num_questions = int(request.form['num_questions'])
                    mcqs = Question_mcqs_generator(text, num_questions, difficulty)
                    generated_file = render_template('mcq-result.html', mcqs=mcqs)

                elif(paper_type=="Subjective"):
                    difficulty = str(request.form['difficulty'])
                    short_questions = int(request.form['short_questions'])
                    inter_questions = int(request.form['inter_questions'])
                    long_questions = int(request.form['long_questions']) 
                    questions = Question_answer_generator(text, difficulty, short_questions, inter_questions, long_questions)
                    generated_file = render_template('q-and-a-result.html', questions = questions)

                elif(paper_type=="true-false"):
                    difficulty = str(request.form['difficulty-true-false'])
                    num_questions = int(request.form['num_questions-true-false'])
                    true_falses = Question_true_false_generator(text, num_questions, difficulty)
                    generated_file = render_template('true-false.html', true_falses= true_falses)

                elif(paper_type=="fill-in-blanks"):
                    difficulty = str(request.form['difficulty-fill-in-blanks'])
                    num_questions = int(request.form['num_questions-fill-in-blanks'])
                    blanks = Question_fill_blanks_generator(text, num_questions, difficulty)
                    generated_file = render_template('fill-in-the-blanks.html', blanks = blanks)
                      
                return generated_file

            return "Invalid file format"

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['RESULTS_FOLDER']):
        os.makedirs(app.config['RESULTS_FOLDER'])
    app.run(debug=True)





  




    