"""Guardrails, measured.

A guardrail is a check in front of the system (on the query) or behind it (on the
answer) that refuses, or rewrites, what should not pass. Everybody agrees they are a
good idea. Very few people measure them, and a guardrail that fires on the wrong
things is not neutral: it redacts order numbers, refuses honest questions, and
teaches people to work around it.

Today's guardrail looks for payment card numbers, in three ever-stricter ways:

- **a pattern**: thirteen to nineteen digits, spaces and dashes allowed between them
- **the Luhn check**: the checksum every card number satisfies, and nine in ten
  random numbers do not
- **the issuer**: the leading digits and length of a real card network

and you measure each against a stream of honest order references.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import re

RUN = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
MAX_QUERY = 500


def digits(text: str) -> str:
    """Only the digits of `text`, in order."""
    raise NotImplementedError


def luhn(number: str) -> bool:
    """The Luhn checksum over the digits of `number`: from the rightmost digit,
    double every second one, subtract 9 from any result over 9, and sum. Valid when
    the sum is divisible by 10. An empty string is not valid."""
    raise NotImplementedError


def issuer(number: str) -> str | None:
    """The card network the digits could belong to, or None:

        visa         starts 4, 13, 16 or 19 digits
        mastercard   starts 51 to 55, or 2221 to 2720; 16 digits
        amex         starts 34 or 37; 15 digits
        discover     starts 6011 or 65; 16 or 19 digits
    """
    raise NotImplementedError


def pattern_cards(text: str) -> list[str]:
    """Every match of RUN, as written (spaces and dashes kept)."""
    raise NotImplementedError


def luhn_cards(text: str) -> list[str]:
    """The pattern matches that pass `luhn`."""
    raise NotImplementedError


def cards(text: str) -> list[str]:
    """The Luhn matches that also have an `issuer`."""
    raise NotImplementedError


def redact(text: str) -> str:
    """Every `cards` match replaced by "[CARD]", and every email address by "[EMAIL]"."""
    raise NotImplementedError


def guard_query(text: str, max_chars: int = MAX_QUERY) -> dict:
    """The guard in front of the retriever.

        empty after stripping      {"allowed": False, "text": "", "problems": ["empty"]}
        longer than max_chars      {"allowed": False, "text": "", "problems":
                                    ["longer than <max_chars> characters"]}
        otherwise                  {"allowed": True, "text": <redacted, stripped>,
                                    "problems": [...]}  - "contained a card number",
                                    "contained an email address", in that order

    A card number in a question is not a reason to refuse it. It is a reason never
    to log, cache or forward it."""
    raise NotImplementedError


def guard_answer(answer: str, cited: list[str], allowed) -> dict:
    """The guard behind the generator. `allowed(chunk_id)` is week 12's reader.

    Problems, in order: "cites nothing"; "cites what this reader may not see: <ids>";
    "contains a card number". Returns {"allowed": no problems, "answer": <redacted
    answer, or "" if it cited anything hidden>, "problems": [...]}."""
    raise NotImplementedError
