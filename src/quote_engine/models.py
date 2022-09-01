"""Contains a model for a quote."""

from dataclasses import dataclass


@dataclass
class QuoteModel:
    """Contains information about a quote."""

    body: str
    author: str

    def __str__(self):
        """Return user-friendly view of the quote."""
        return f"\"{self.body}\" - {self.author}"
