"""Contains models"""

from dataclasses import dataclass


@dataclass
class Quote:
    """Contains information about a quote."""
    body: str
    author: str

    def __str__(self):
        """Return user-friendly view of the quote."""
        return f"\"{self.body}\" - {self.author}"
