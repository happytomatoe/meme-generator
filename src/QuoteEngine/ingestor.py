from abc import ABC
from typing import List

from src.QuoteEngine.model import QuoteModel


class IngestorInterface(ABC):
    # The project contains an abstract base class, IngestorInterface, which defines:
    # A complete classmethod method to verify if the file type is compatible with the ingestor class.
    # Hint: Classmethods can access class variables, which can be redefined by children classes.
    def can_ingest(cls, path: str) -> bool:
        pass
    def parse(cls, path: str) -> List[QuoteModel]:
        pass


class CsvIngestor(IngestorInterface):
    # TODO implement
    # The class depends on the pandas library to complete the defined, abstract method signatures to parse CSV files.
    pass

class DocxIngestor(IngestorInterface):
    # TODO implement
    # The class depends on the python-docx library to complete the defined, abstract method signatures to parse DOCX files.
    pass

class PdfIngestor(IngestorInterface):
    # TODO implement
    # The PDFIngestor class utilizes the subprocess module to call the pdftotext(https://www.xpdfreader.com/pdftotext-man.html) CLI utility—creating a pipeline
    # that converts PDFs to text and then ingests the text.
    # The class handles deleting temporary files.
    pass

class TxtIngestor(IngestorInterface):
    # TODO implement
    pass

class Ingestor:
    """
    A final Ingestor class should realize the IngestorInterface
     abstract base class and encapsulate your helper classes.
      It should implement logic to select the appropriate helper for a given file based on filetype.

    """
    pass

