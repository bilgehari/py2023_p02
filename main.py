import os
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Variable to store extracted titles
titles = []

# Function to extract titles from PDF files in a specified directory
def extract_titles(directory):
    global titles
    titles = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(directory, file_name)
            print(f"Processing file: {file_path}")
            pdf_document = fitz.open(file_path)
            title = pdf_document.metadata.get("title", "").strip()
            print(f"Extracted title: {title}")
            titles.append((title, file_path))
            pdf_document.close()
    return titles

# Function to save titles to a new PDF file
def save_titles(title_list, output_filename):
    try:
        pdf_writer = fitz.open()
        for title, file_path in title_list:
            pdf_document = fitz.open(file_path)
            pdf_writer.insert_pdf(pdf_document)
            pdf_document.close()

        # Create a new PDF with improved readability
        with open(output_filename, "wb") as output_file:
            c = canvas.Canvas(output_file, pagesize=letter)
            c.setFont("Helvetica", 16)
            c.drawString(72, 750, "Extracted Titles")
            c.setFont("Helvetica", 12)

            for index, (title, _) in enumerate(title_list, start=1):
                y_position = 720 - (index * 14)
                c.drawString(72, y_position, f"{index}. {title}")

            c.save()

        print(f"Titles saved to {output_filename}.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Set the directory path
directory_path = os.path.join(os.getcwd(), "pdfFiles")

while True:
    # Display menu
    print("\nMenu:")
    print("1. Extract Titles")
    print("2. Save Titles")
    print("3. Exit")

    # Get user choice
    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        # Extract titles
        titles = extract_titles(directory_path)
        print("Extracted Titles:")
        for index, (title, _) in enumerate(titles, start=1):
            print(f"{index}. {title}")

    elif choice == "2":
        # Save titles to a new PDF file
        save_titles(titles, "all_titles.pdf")

    elif choice == "3":
        # Exit the program
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
