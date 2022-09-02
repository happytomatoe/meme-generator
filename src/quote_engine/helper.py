"""Contains helper methods."""
from typing import Optional

from quote_engine.models import QuoteModel


def create_quote(quote_string: str) -> Optional[QuoteModel]:
    """Create an optional Quote.

    :param quote_string: The quote string
    """
    # Add validation
    quote_string = __clean(quote_string)
    if len(quote_string) == 0:
        return None
    splitted_quote = quote_string.split("-")
    return QuoteModel(splitted_quote[0], splitted_quote[1])


def __clean(s: str) -> str:
    """Clean string from non ascii chars and other chars like quotes.

    :param s: The string to clean
    """
    res = s.replace('"', "")
    res = res.encode("ascii", "ignore").decode()
    return res
