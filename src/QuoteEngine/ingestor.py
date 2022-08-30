from abc import ABC, abstractmethod
from typing import List

from QuoteEngine.model import QuoteModel


class IngestorInterface(ABC):
    # The project contains an abstract base class, IngestorInterface, which defines:
    # A complete classmethod method to verify if the file type is compatible with the ingestor class.
    # Hint: Classmethods can access class variables, which can be redefined by children classes.

    @abstractmethod
    def can_ingest(cls, path: str) -> bool:
        pass

    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass


class FileBasedIngestorInterface(IngestorInterface, ABC):
    @property
    @abstractmethod
    def file_extension(self):
        raise NotImplementedError

    def can_ingest(cls, path: str) -> bool:
        return path.endswith(cls.file_extension)


class CsvIngestor(FileBasedIngestorInterface):
    file_extension = ".csv"

    def parse(cls, path: str) -> List[QuoteModel]:
        raise NotImplementedError

    # TODO implement
    # The class depends on the pandas library to complete the defined, abstract method signatures to parse CSV files.


class DocxIngestor(FileBasedIngestorInterface):
    file_extension = ".docx"

    def parse(cls, path: str) -> List[QuoteModel]:
        raise NotImplementedError

    # TODO implement
    # The class depends on the python-docx library to complete the defined, abstract method signatures to parse DOCX files.
    pass


class PdfIngestor(FileBasedIngestorInterface):
    file_extension = ".pdf"

    # TODO implement
    # The PDFIngestor class utilizes the subprocess module to call the pdftotext(https://www.xpdfreader.com/pdftotext-man.html) CLI utility—creating a pipeline
    # that converts PDFs to text and then ingests the text.
    # The class handles deleting temporary files.
    def parse(cls, path: str) -> List[QuoteModel]:
        raise NotImplementedError


class TxtIngestor(FileBasedIngestorInterface):
    file_extension = ".txt"

    def parse(cls, path: str) -> List[QuoteModel]:
        with open(path, encoding='utf-8') as f:
            # TODO: add validatoin
            return [QuoteModel(l.split("-")[0], l.split("-")[1].strip("-\n ")) for l in f.readlines()]


class Ingestor(IngestorInterface):
    _ingestors = [CsvIngestor(), TxtIngestor(), PdfIngestor(), DocxIngestor()]
    """
    A final Ingestor class should realize the IngestorInterface
     abstract base class and encapsulate your helper classes.
      It should implement logic to select the appropriate helper for a given file based on filetype.

    """

    @classmethod
    def parse(cls, f):
        for ingestor in cls._ingestors:
            if ingestor.can_ingest(f):
                return ingestor.parse(f)
        #     TOOD: add custom class
        raise Exception(f"Cannot find ingestor for {f}")
