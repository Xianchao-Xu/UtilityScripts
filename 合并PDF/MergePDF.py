# coding: utf-8
# author: xuxc
import PyPDF2

pdf_files = ['logo.pdf', 'scatter.pdf']
pdf_writer = PyPDF2.PdfFileWriter()
for filename in pdf_files:
    pdf_reader = PyPDF2.PdfFileReader(open(filename, 'rb'))
    if not pdf_reader.isEncrypted:
        for page_num in range(pdf_reader.numPages):
            page_obj = pdf_reader.getPage(page_num)
            pdf_writer.addPage(page_obj)

pdf_writer.write(open('Merge.pdf', 'wb'))
