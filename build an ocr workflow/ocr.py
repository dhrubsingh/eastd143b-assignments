import streamlit as st
import pytesseract
from PIL import Image
import csv
import os

def ocr_image(image, languages):
    """
    Perform OCR on a single image and return the extracted text.
    """
    # Set the OCR engine to use Tesseract
    pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"

    # Set the languages for OCR
    languages_str = "+".join(languages)
    config = f"--oem 3 --psm 6 -l {languages_str}"

    # Convert the image to grayscale and perform OCR
    gray = image.convert("L")
    text = pytesseract.image_to_string(gray, config=config)

    return text


def process_images(images, languages):
    """
    Perform OCR on multiple images and return a list of tuples containing
    the file name and extracted text for each image.
    """
    results = []
    for image in images:
        # Open the image file
        img = Image.open(image)

        # Perform OCR on the image
        text = ocr_image(img, languages)

        # Add the results to the list
        results.append((image.name, text))

    return results


def save_results(results):
    """
    Save the OCR results to a CSV file.
    """
    print("Save results has run")
    csv_path = "ocr_results.csv"
    file_exists = os.path.isfile(csv_path)
    with open("ocr_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["File Name", "Extracted Text"])
        #writer.writerow(["File Name", "Extracted Text"])
        writer.writerows(results)


# Set up the Streamlit app
st.title("OCR Workflow")

# File picker component
images = st.file_uploader("Select image(s)", accept_multiple_files=True)

# Language selection component
languages = st.multiselect("Select language(s)", ["eng", "spa", "fra"])

if st.button("Process Images"):
    print('clicked')
    if images:
        # Perform OCR on the selected images
        results = process_images(images, languages)

        # Display the results in a table
        st.table(results)
        

    else:
        st.warning("Please select one or more images to process.")

if st.button("Save as CSV"):
    results = process_images(images, languages)
    if results:
        # Save the results as a CSV file in local directory
        save_results(results)
        
    else:
        st.warning("Please process images and extract text before saving as CSV.")