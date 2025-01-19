# coding: utf-8
# author: xuxc

import typing

from borb.pdf import Document
from borb.pdf import PDF


def main():
    # open doc_001
    doc_001: typing.Optional[Document] = Document()
    with open("logo.pdf", "rb") as pdf_file_handle:
        doc_001 = PDF.loads(pdf_file_handle)

    # open doc_002
    doc_002: typing.Optional[Document] = Document()
    with open("scatter.pdf", "rb") as pdf_file_handle:
        doc_002 = PDF.loads(pdf_file_handle)

    # merge
    doc_001.add_document(doc_002)

    # write
    with open("Merge.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc_001)


if __name__ == "__main__":
    main()
