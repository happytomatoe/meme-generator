import os
import random

from MemeEngine.meme_engine import MemeEngine
from QuoteEngine.ingestor import Ingestor
from QuoteEngine.model import QuoteModel


# @TODO Import your Ingestor and MemeEngine classes


def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given a path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = [
                       './_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv'
                       ]
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))
        print("Quotes:", quotes)
        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


"""
The project contains a main.py file that uses the ImageCaptioner, DocxIngestor, PDFIngestor, 
and CSVIngestor methods to generate a random captioned image.

The program must be executable from the command line.

The program takes three OPTIONAL arguments:

A string quote body
A string quote author
An image path
The program returns a path to a generated image.
If any argument is not defined, a random selection is used.
"""

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate a motivational meme')
    parser.add_argument('--path', type=str, help='path to an image file')
    parser.add_argument('--body', type=str, help='quote body to add to the image')
    parser.add_argument('--author', type=str, help='quote author to add to the image')

    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
