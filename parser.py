import pdfplumber                                                            #library used to read and extract text,tables and other content from PDF files.


#This function reads a pdf file and extract all the text from it and returns the extracted text as a string.
def extract_text_from_pdf(pdf_file):

    text = ""                                                                    #it will store the extracted text from the PDF file.

    with pdfplumber.open(pdf_file) as pdf:                                      #opens the PDF file using pdfplumber library and creates a pdf object.

        for page in pdf.pages:                                                  #loops through each page of the PDF file.

            extracted_text = page.extract_text()
            if extracted_text:                                                 #check whether text was successfully extracted from the page.
                text += extracted_text + " "                                    #Adds current page text intp the main text variable.S
    return text