import PyPDF2


def pdf_convertor(filename: str) -> str:
    directory = f"uploads/{filename}"
    with open(directory, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        extracted_text = ""

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]

            extracted_text += page.extract_text()

        return extracted_text
