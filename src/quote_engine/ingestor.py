"""Provides functionality to ingest quotes."""
import os
import subprocess
import uuid
from abc import ABC, abstractmethod
from typing import List

import pandas as pd
from docx import Document
from docx.opc.exceptions import PackageNotFoundError

from quote_engine.helper import create_quote
from quote_engine.models import QuoteModel


class IngestorInterface(ABC):
    """Ingest collection of quotes."""

    @abstractmethod
    def can_ingest(cls, path: str) -> bool:
        """Return whether ingestor can ingest this path.

        :param path: path to the resource with quotes
        """

    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Ingest list of quotes from using provided path.

        :param path: path to the resource with quotes
        """


class FileBasedIngestorInterface(IngestorInterface, ABC):
    """Ingest collection of quotes saved in a file."""

    @property
    @abstractmethod
    def file_extension(self):
        """File extension of the file with quotes."""
        raise NotImplementedError

    def can_ingest(cls, path: str) -> bool:
        """
        Ingest list of quotes from using provided path.

        :param path: path to the resource with quotes
        """
        return path.endswith(cls.file_extension)


class CsvIngestor(FileBasedIngestorInterface):
    """Ingest csv file."""

    file_extension = ".csv"

    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a csv file.

        :param path: path to a csv file
        :return: list of quotes
        """
        try:
            df = pd.read_csv(path)
            return [
                (QuoteModel(author=row.author, body=row.body))
                for index, row in df.iterrows()
            ]
        except FileNotFoundError:
            raise FileNotFoundError("Can not find file" + path)


class DocxIngestor(FileBasedIngestorInterface):
    """Ingest docx file."""

    file_extension = ".docx"

    def parse(cls, path: str) -> List[QuoteModel]:
        """Ingest docx file.

        :param path: path to a docx file
        :return: list of quotes
        """
        try:
            doc = Document(path)
            res = [create_quote(para.text) for para in doc.paragraphs]
            return [r for r in res if r is not None]
        except PackageNotFoundError:
            raise FileNotFoundError("Cannot find file " + path)


class TxtIngestor(FileBasedIngestorInterface):
    """Ingest txt file."""

    file_extension = ".txt"

    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse a txt file with quotes.

        :param path: path to a txt file
        :return: list of quotes
        """
        try:
            with open(path, encoding="utf-8") as file:
                res = [create_quote(line) for line in file.readlines()]
                return [r for r in res if r is not None]
        except FileNotFoundError:
            raise FileNotFoundError("Cannot find file " + path)


class PdfIngestor(FileBasedIngestorInterface):
    """Ingest pdf file."""

    file_extension = ".pdf"
    LINE_FEED = chr(12)

    def parse(cls, path: str) -> List[QuoteModel]:
        """Ingest list of quotes from pdf file.

        :param path: path to the pdf file
        """
        if not os.path.isfile(path):
            raise FileNotFoundError("Cannot find file " + path)
        res = []
        new_path = (path[:path.index(cls.file_extension)]
                    + str(uuid.uuid4()) + ".txt")
        subprocess.run(["pdftotext", "-layout", path, new_path], check=True)
        with open(new_path, encoding="utf-8") as file:
            res = [
                create_quote(line) for line in file.readlines()
                if line != cls.LINE_FEED
            ]
            res = [r for r in res if r is not None]
        os.remove(new_path)
        return res


class IngestorNotFoundException(Exception):
    """Raised when ingestor is not found."""


class Ingestor(IngestorInterface):
    """Ingest quotes."""

    _ingestors = [CsvIngestor(), TxtIngestor(), PdfIngestor(), DocxIngestor()]

    def can_ingest(cls, path: str) -> bool:
        """Return whether ingestor can ingest this path.

        :param path: path to the resource with quotes
        """
        for ingestor in cls._ingestors:
            if ingestor.can_ingest(path):
                return True
        return False

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Ingest list of quotes from using provided path.

        :param path: path to the resource with quotes
        :Raises IngestorNotFoundException: if ingestor for path is not found
        :returns: list of quotes
        """
        for ingestor in cls._ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise IngestorNotFoundException(f"Cannot find ingestor for {path}")
