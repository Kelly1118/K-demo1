import os
from bs4 import BeautifulSoup
import docx
import PyPDF2


def convert_word_to_text(file_path):
    try:
        doc = docx.Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        print(f"Error converting {file_path} to text: {e}")
        return ""


def convert_pdf_to_text(file_path):
    try:
        text = ""
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error converting {file_path} to text: {e}")
        return ""


def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()


def remove_blank_and_duplicate_lines(text):
    lines = text.split('\n')
    non_blank_lines = []
    unique_lines = set()
    for line in lines:
        line = line.strip()
        if line and line not in unique_lines:
            non_blank_lines.append(line)
            unique_lines.add(line)
    return '\n'.join(non_blank_lines)


def preprocess_folder(folder_path):
    all_text = ""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.docx'):
                text = convert_word_to_text(file_path)
            elif file.endswith('.pdf'):
                text = convert_pdf_to_text(file_path)
            elif file.endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue
            else:
                continue
            text = remove_html_tags(text)
            text = remove_blank_and_duplicate_lines(text)
            all_text += text + "\n"
    try:
        with open('preprocessed_data.txt', 'w', encoding='utf-8') as f:
            f.write(all_text)
    except Exception as e:
        print(f"Error writing to preprocessed_data.txt: {e}")


if __name__ == "__main__":
    # preprocess_folder('C:/data/college_student_study')
    preprocess_folder('D:/app/Anaconda/项目/项目一(拓展)-deepseek/book')
