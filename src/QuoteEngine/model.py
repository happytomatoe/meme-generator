from dataclasses import dataclass


@dataclass
class QuoteModel:
    body: str
    author: str

    def __str__(self):
        """Return user-friendly view of the quote."""
        return f"\"{self.body}\" - {self.author}"
