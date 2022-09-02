"""
The project completes the Flask app starter code in app.py.

app.py uses the Quote Engine module and Meme Generator modules to generate a random captioned image.

app.py uses the requests package to fetch an image from a user submitted URL.

The flask server runs with no errors
"""

import os
import random
import tempfile

import requests
from flask import Flask, render_template, abort, request

from helper import ingest_quotes, find_images_in_folder
from meme_engine import MemeEngine

app = Flask(__name__)
MEME_FOLDER = "./static"
# create folder for static resources
if not os.path.exists(MEME_FOLDER):
    os.makedirs(MEME_FOLDER)
meme = MemeEngine(MEME_FOLDER)


def setup():
    """Load all resources."""
    quote_files = [
        "./_data/DogQuotes/DogQuotesTXT.txt",
        "./_data/DogQuotes/DogQuotesDOCX.docx",
        "./_data/DogQuotes/DogQuotesPDF.pdf",
        "./_data/DogQuotes/DogQuotesCSV.csv",
    ]
    images_path = "./_data/photos/dog/"

    quotes = ingest_quotes(quote_files)
    print("Quotes:", quotes)

    imgs = find_images_in_folder(images_path)
    print("Images", imgs)
    return quotes, imgs


quotes, imgs = setup()


@app.route("/")
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template("meme.html", path=path)


@app.route("/create", methods=["GET"])
def meme_form():
    """User input for meme information."""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post():
    """Create a user defined meme."""
    image_url = request.form["image_url"]
    response = requests.get(image_url, timeout=10)  # 10 seconds
    img_data = response.content
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(img_data)
            temp_file.flush()
            temp_file.seek(0)
            body = request.form["body"]
            author = request.form["author"]
            path = meme.make_meme(temp_file, body, author)

        return render_template("meme.html", path=path)
    abort(400, f"When trying to download specified image we got {response.status_code}")


if __name__ == "__main__":
    app.run()
