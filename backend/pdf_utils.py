import fitz


def extract_text_from_pdf(pdf_path):

    text = ""

    try:

        pdf = fitz.open(pdf_path)

        for page in pdf:

            text += page.get_text()

    except Exception as e:

        print("PDF ERROR:", str(e))

    return text
