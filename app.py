from flask import Flask, request, send_from_directory, jsonify
from PIL import Image, ImageEnhance
import pytesseract
import re
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

medical_data = [
    "Medical microbiology and bacteriology",
    "Virology",
    "Parasitology",
    "Immunology",
    "Microbiology and immunology",
    "Human and medical genetics",
    "Physiology, general",
    "Molecular physiology",
    "Cell physiology",
    "Endocrinology",
    "Cardiovascular science",
    "Exercise physiology",
    "Vision science and physiological optics",
    "Pathology and experimental pathology",
    "Oncology and cancer biology",
    "Pharmacology",
    "Molecular pharmacology",
    "Neuropharmacology",
    "Toxicology",
    "Molecular toxicology",
    "Environmental toxicology",
    "Pharmacology and toxicology",
    "Molecular medicine",
    "Neuroscience",
    "Neuroanatomy",
    "Neurobiology and anatomy",
    "Neurobiology and behavior",
    "Veterinary medicine",
    "Veterinary sciences and veterinary clinical sciences, general",
    "Veterinary physiology",
    "Veterinary microbiology and immunobiology",
    "Veterinary pathology and pathobiology",
    "Large animal and food animal and equine surgery and medicine",
    "Small and companion animal surgery and medicine",
    "Comparative and laboratory animal medicine",
    "Veterinary preventive medicine and epidemiology and public health",
    "Veterinary infectious diseases",
    "Medical illustration and medical illustrator",
    "Medical informatics",
    "Clinical nutrition and nutritionist",
    "Bioethics and medical ethics",
    "Acupuncture and oriental medicine",
    "Traditional Chinese medicine and Chinese herbology",
    "Naturopathic medicine and naturopathy",
    "Ayurvedic medicine and Ayurveda",
    "Direct entry midwifery",
    "Massage therapy and therapeutic massage",
    "Yoga teacher training and Yoga therapy",
    "Registered nursing and registered nurse",
    "Nursing administration",
    "Adult health nurse and nursing",
    "Nurse anesthetist",
    "Family practice nurse and nursing",
    "Maternal and child health and neonatal nurse and nursing",
    "Nurse midwife and nursing midwifery",
    "Nursing science",
    "Pediatric nurse and nursing",
    "Psychiatric and mental health nurse and nursing",
    "Public health and community nurse and nursing",
    "Perioperative and operating room and surgical nurse and nursing",
    "Clinical nurse specialist",
    "Critical care nursing",
    "Occupational and environmental health nursing",
    "Emergency room and trauma nursing",
    "Nursing education",
    "Palliative care nursing",
    "Geriatric nurse and nursing",
    "Women's health nurse and nursing",
    "Medicine",
    "Medical scientist",
    "Substance abuse and addiction counseling",
    "Psychiatric and mental health services technician",
    "Clinical and medical social work",
    "Community health services and liaison and counseling",
    "Clinical pastoral counseling and patient counseling",
    "Psychoanalysis and psychotherapy",
    "Mental health counseling and counselor",
    "Genetic counseling and counselor",
    "Optometry",
    "Ophthalmic technician and technologist",
    "Orthoptics and orthoptist",
    "Ophthalmic and optometric support services and allied professions, other",
    "Osteopathic medicine and osteopathy",
    "Pharmacy",
    "Pharmaceutics and drug design",
    "Medicinal and pharmaceutical chemistry",
    "Clinical and industrial drug development",
    "Pharmacoeconomics and pharmaceutical economics",
    "Clinical and hospital and managed care pharmacy",
    "Industrial and physical pharmacy and cosmetic sciences",
    "Pharmaceutical sciences",
    "Podiatric medicine and podiatry",
    "Public health and general health",
    "Environmental health",
    "Health and medical physics",
    "Occupational health and industrial hygiene",
    "Public health education and promotion",
    "Community health and preventive medicine",
    "Maternal and child health",
    "International public health and international health",
    "Health services administration",
    "Behavioral aspects of health",
    "Geriatrics",
    "Pain management",
    "Addiction medicine",
    "Genomics",
    "Biomedical engineering",
    "Clinical genetics",
    "Healthcare management",
    "Health informatics",
    "Medical research",
    "Pharmacogenomics",
    "Sports medicine",
    "Palliative care",
    "Translational medicine",
    "Neuroimmunology",
    "Medical biotechnology",
    "Public health nutrition",
    "Clinical epidemiology",
    "Health policy",
    "Healthcare quality and safety",
    "Infectious disease",
    "Rehabilitation medicine",
    "Forensic medicine",
    "Nuclear medicine",
    "Pain medicine",
    "Sleep medicine",
    "Addiction psychiatry",
    "Reproductive endocrinology",
    "Immunopathology",
    "Molecular diagnostics",
    "Clinical pathology",
    "Pharmacovigilance",
    "Health communication",
    "Medical education",
    "Clinical trials management",
    "Health economics",
    "Health systems management",
    "Clinical and Translational Research",
    "Biostatistics",
    "Epidemiology",
    "Public health administration",
    "Health policy and management",
    "Health services research",
    "Neuropsychology",
    "Medical device technology",
    "Pediatric surgery",
    "Dermatology",
    "Pulmonology",
    "Rheumatology",
    "Gastroenterology",
    "Hematology",
    "Endocrine surgery",
    "Obstetrics and gynecology",
    "Urology",
    "Cardiac surgery",
    "Plastic and reconstructive surgery",
    "Orthopedic surgery",
    "Trauma surgery",
    "Transplant surgery",
    "Geriatric psychiatry",
    "Clinical pharmacology",
    "Critical care medicine",
    "Emergency medicine",
    "Medical toxicology",
    "Medical genetics counseling",
    "Health promotion",
    "Pediatric cardiology",
    "Neonatology",
    "MBBS",
    "MD",
    "DO",
    "PhD",
    "MSc",
    "BSc",
    "BPharm",
    "MPharm",
    "DPharm",
    "DPT",
    "DDS",
    "DMD",
    "MPH",
    "MHA",
    "RN",
    "CRNA",
    "NP",
    "LPN",
    "CNA"
]

def preprocess_image(image):
    gray_image = image.convert('L')
    enhance = ImageEnhance.Contrast(gray_image)
    enhanced = enhance.enhance(2.0)
    return enhanced

def extract_text(image):
    text = pytesseract.image_to_string(image, config='--oem 3 --psm 6')
    return text

def find_keywords(text, keywords):
    found_keywords = []
    for keyword in keywords:
        if re.search(re.escape(keyword), text, re.IGNORECASE):
            found_keywords.append(keyword)
    return found_keywords

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        image = Image.open(file)
        processed_image = preprocess_image(image)
        text = extract_text(processed_image)
        found_keywords = find_keywords(text, medical_data)

        return jsonify(bool(found_keywords)), 200

if __name__ == '__main__':
    app.run(debug=True)
