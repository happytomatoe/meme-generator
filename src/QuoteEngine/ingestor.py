from abc import ABC, abstractmethod
from typing import List, Optional

import pandas as pd

from QuoteEngine.model import QuoteModel


class IngestorInterface(ABC):
    # The project contains an abstrac\t base class, IngestorInterface, which defines:
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
        df = pd.read_csv(path)
        return [(QuoteModel(author=row.author, body=row.body)) for index, row in df.iterrows()]


class DocxIngestor(FileBasedIngestorInterface):
    file_extension = ".docx"

    def parse(cls, path: str) -> List[QuoteModel]:
        from docx import Document
        # Add validation(file exits)
        doc = Document(path)
        res = [create_quote_model(para.text) for para in doc.paragraphs]
        return [r for r in res if r is not None]


class TxtIngestor(FileBasedIngestorInterface):
    file_extension = ".txt"

    def parse(cls, path: str) -> List[QuoteModel]:
        with open(path, encoding='utf-8') as f:
            # TODO: add validatoin
            res = [create_quote_model(l) for l in f.readlines()]
            return [r for r in res if r is not None]


class PdfIngestor(FileBasedIngestorInterface):
    file_extension = ".pdf"
    LINE_FEED = chr(12)

    def parse(cls, path: str) -> List[QuoteModel]:
        import subprocess
        new_path = path[:path.index(cls.file_extension)] + "Pdf.txt"
        c = subprocess.run(["pdftotext", "-layout", path, new_path],
                           capture_output=True)
        print(c)
        with open(new_path, encoding='utf-8') as f:
            res = [create_quote_model(l) for l in f.readlines() if l != cls.LINE_FEED]
            return [r for r in res if r is not None]


def create_quote_model(s: str) -> Optional[QuoteModel]:
    # Add validation
    str = s.strip("-\n ").replace("\"", "")
    str = str.encode("ascii", "ignore").decode()
    if len(str) == 0:
        return None
    l = str.split("-")
    return QuoteModel(l[0], l[1])


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
        #     TODO: add custom exception class
        raise Exception(f"Cannot find ingestor for {f}")
