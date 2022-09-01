"""Common functions module."""
import os
from typing import List

from quote_engine import Ingestor
from quote_engine.model import QuoteModel


def find_images_in_folder(images_folder: str) -> List[str]:
    """Find all images in the given folder.

    This function assumes that every file in the folder is an image.
    :param images_folder: folder with images
    :return: list of images in the given folder
    """
    imgs = []
    for root, _, files in os.walk(images_folder):
        norm_root = os.path.normpath(root)
        imgs = [os.path.join(norm_root, name) for name in files]
    return imgs


def ingest_quotes(quote_file_paths: List[str]) -> List[QuoteModel]:
    """Ingest quotes from the given files.

    :param quote_file_paths: list of files with quotes
    :return: list of quotes
    """
    quotes = []
    for quote_file_path in quote_file_paths:
        quotes.extend(Ingestor.parse(quote_file_path))
    return quotes
