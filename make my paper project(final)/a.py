# import os
# import google.generativeai as genai


# def Question_answer_generator(answer):
#     prompt = f"""
#     You are an AI assistant helping the user generate questions based on the following text:
#     '{answer}'
#     Please generate questions having answer {answer}. Each response should have:
#     - A clear question
#     Format:
#     ## Question
#     Question: [question]
#     """
#     response = model.generate_content(prompt).text.strip()
#     return response


# from pymongo import MongoClient

# connection_string = "mongodb+srv://My_project:collegeproject@cluster0.86ln2oe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# client = MongoClient(connection_string)

# db_name = client.list_database_names()

# print(db_name)

# db = client["Hackindia"]

# col_name = db.list_collection_names()
# print(col_name)

# col_name1 = db['Softskill']

# document = col_name1.find()

# for doc in document:
#     print(f"{doc["id"]} and {doc["bloomlevel"]}")

#     if(doc['id'] == 1):
#         answer = doc['answer']
#         question = Question_answer_generator(answer)


# print(question)


# import fitz 
# import os

# def extract_images_from_pdf(pdf_path, output_folder):
#     os.makedirs(output_folder, exist_ok=True)

#     doc = fitz.open(pdf_path)

#     for page_num in range(len(doc)):
#         page = doc[page_num]
#         images = page.get_images(full=True)

#         for img_index, img in enumerate(images):
#             xref = img[0]
#             base_image = doc.extract_image(xref)
#             image_bytes = base_image["image"]
#             image_ext = base_image["ext"]

#             image_filename = f"page{page_num+1}_img{img_index+1}.{image_ext}"
#             with open(os.path.join(output_folder, image_filename), "wb") as f:
#                 f.write(image_bytes)

#             print(f"Saved image: {image_filename}")

#     print("Extraction complete.")

# extract_images_from_pdf("image-doc.pdf", "output_images")


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


import fitz  # PyMuPDF
import os
import cv2
import pytesseract

# ——— CONFIG ———
PDF_PATH = "Love1.pdf"
OUTPUT_FOLDER = "output_images"
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

if __name__ == "__main__":
    extracted = extract_code_from_pdf(PDF_PATH, OUTPUT_FOLDER)
    # Save results
    out_txt = os.path.join(OUTPUT_FOLDER, "ocr_results.txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        for img, txt in extracted.items():
            f.write(f"--- {os.path.basename(img)} ---\n{txt}\n\n")
    # print(f"\nAll OCR results written to {out_txt}")










