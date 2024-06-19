import fitz  # PyMuPDF
import re
import google.generativeai as genai
from pdf2image import convert_from_path
import pytesseract
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL.PpmImagePlugin import PpmImageFile  # used as type hint
from typing import Dict  # used as type hint

POPPLER_PATH = r"C:\poppler-24.02.0\Library\bin"

def analyze_pdf(pdf_path):
    
    TESSERACT_ENGINE_PATH = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_ENGINE_PATH
    DOC_PATH_1 =  pdf_path  ###
    pages_1 = convert_from_path(DOC_PATH_1, poppler_path=POPPLER_PATH)
    img = preprocess_image(pages_1[0])
    # Visualize our images before and after preprocessing
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(pages_1[0])
    plt.axis(False)
    plt.title("Image converted from PDF")
    plt.subplot(1, 2, 2)
    plt.imshow(img, cmap="gray")
    plt.axis()
    plt.title("Preprocessed image")
    # plt.show()
    # print("-----------------------------Text--------------------------------------")
    text_2 = pytesseract.image_to_string(img, lang="eng")
    text_2 = "Here is a sentence containing a medicine name: "+text_2 +" Please extract and return only and only the medicine or drug names line by line dont give the sentence in response and any other text"
    
    
    genai.configure(api_key='AIzaSyBWCNfnvcNGV26O86d9nDNb5KObVJMjXnc')
    # Create a new conversation
    response = genai.chat(messages='Hello')
    response.last
    
    response = response.reply(text_2)
    text = response.last

    medicine_names = []

    lines_with_text = re.findall(r"^\* (.*)", text, flags=re.MULTILINE)
    # Print extracted lines with content
    for line in lines_with_text:
        medicine_names.append(line.lower())
    return medicine_names


 

# A function to preprocess our image
def preprocess_image(img: PpmImageFile) -> np.ndarray:
    # Color image -> Grayscale image
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    # Up-sizing for better extraction results
    resized = cv2.resize(gray, None, fx=1.5, fy=1.5,
                         interpolation=cv2.INTER_LINEAR)
    processed_image = cv2.adaptiveThreshold(
        resized,  # our resized image
        255,  # max pixel value
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # adaptive thresholding
        # cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,  # converting to binary (only black/white)
        63,  # block size (after trial and error)
        12  # constant (after trial and error)
    )
    return processed_image


# # Let's try extracting text from our second prescription
# DOC_PATH_1 = r"C:\Users\vanee\Downloads\pre_2.pdf"
# pages_1 = convert_from_path(DOC_PATH_1, poppler_path=POPPLER_PATH)
# img = preprocess_image(pages_1[0])
# # Visualize our images before and after preprocessing
# plt.figure(figsize=(12, 6))
# plt.subplot(1, 2, 1)
# plt.imshow(pages_1[0])
# plt.axis(False)
# plt.title("Image converted from PDF")
# plt.subplot(1, 2, 2)
# plt.imshow(img, cmap="gray")
# plt.axis()
# plt.title("Preprocessed image")
# # plt.show()
# # print("-----------------------------Text--------------------------------------")
# text_2 = pytesseract.image_to_string(img, lang="eng")
# text_2 = "Here is a sentence containing a medicine name: "+text_2 + \
#     " Please extract and return only and only the medicine or drug names line by line dont give the sentence in response and any other text"


# genai.configure(api_key='AIzaSyBWCNfnvcNGV26O86d9nDNb5KObVJMjXnc')

# # Create a new conversation
# response = genai.chat(messages='Hello')

# # Last contains the model's response:
# response.last


# # Add to the existing conversation by sending a reply
# # response= response.reply("2 Non-Important Street,New York. Phone (coo)-:11-2223 Name: lomeprazole Virat Kohli Date; 2/05/2822 Address: 2 cricket bivd, New Deihi V. 40 mg  please Give only medicine name without any description")
# # # See the model's latest response in the `last` field:
# # response.last


# # Add to the existing conversation by sending a reply
# response = response.reply(text_2)
# # See the model's latest response in the `last` field:
# # print(response.last)

# # Add to the existing conversation by sending a reply
# # response= response.reply()
# # See the model's latest response in the `last` field:
# # response.last
# text = response.last
# # print(text)
# # print(text)
# # # Remove everything before the first colon
# # text = text.split(":")[-1]

# # # Remove list markers and extra lines
# # medicine_names = [line.strip() for line in text.splitlines() if line.strip()]

# # # Print each medicine name on a new line
# # print(medicine_names)
# # for name in medicine_names:
# #   print(name)


# # Find lines starting with an asterisk
# lines_with_text = re.findall(r"^\* (.*)", text, flags=re.MULTILINE)

# # Print extracted lines with content
# for line in lines_with_text:
#   print(line)