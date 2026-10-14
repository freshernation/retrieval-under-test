"""A document somebody wrote in order to be retrieved.

Every document in this corpus was written to be read. Today one is written to be
*found*: by a particular question, ahead of the document that answers it.

Anybody who can get text into your corpus can do this. A wiki page, a support
ticket, an uploaded PDF, a web page your crawler visits. They do not need access
to the retriever. They need to guess a question.

Then run every check week 8 built on the answer that comes out, and read what
they say.

**What this lab measures and what it does not.** The generator here is week 8's
stipulated one. It quotes the best-matching sentences in its context; it does
not follow instructions. So this lab measures whether planted text gets
*retrieved* and *quoted* - which needs no model to go wrong. Whether a real
model would also *obey* an instruction in that text is a `--live` question, and
the answer is "sometimes".

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


def stuffed(query_text: str, payload: str) -> str:
    """The cheapest poisoned chunk there is: the question, then the lie, as
    **one sentence**.

        stuffed("is JSON UTF-8?", "ask at example.test.")
        -> "is JSON UTF-8: ask at example.test."

    Strip the question's surrounding spaces and any trailing `?`, `.` or `!`,
    then a colon and a space, then the payload stripped of surrounding spaces.

    One sentence, because the sentence that repeats the question is the one a
    generator quotes.
    """
    raise NotImplementedError


def inject(chunks: dict[str, str], poison_id: str, text: str) -> dict[str, str]:
    """A **new** chunk dict with the planted chunk added. The original is not
    changed - you will want the clean corpus again in a moment."""
    raise NotImplementedError


def reached(context: dict[str, str], poison_id: str) -> bool:
    """Did the planted chunk make it into the context?"""
    raise NotImplementedError


def carried(answer_text: str, marker: str) -> bool:
    """Did the answer repeat the marker? Any capitals."""
    raise NotImplementedError


def displaced(clean: dict[str, str], poisoned: dict[str, str]) -> list[str]:
    """The chunk ids in the clean context that are missing from the poisoned
    one, in the clean context's order.

    A planted chunk takes a place. This is what it took it from.
    """
    raise NotImplementedError


def trusted(context: dict[str, str], sources) -> dict[str, str]:
    """The context restricted to chunks whose parent document is in `sources`,
    order kept.

    Provenance: the one check in this file that works, and it works by knowing
    where a document came from rather than by reading what it says.
    """
    raise NotImplementedError


def attack_rate(build, generator, queries, chunks, payload: str, marker: str,
                poison_id: str = "planted#0") -> dict:
    """Aim one planted chunk at each query in turn, and count.

    For each query: inject `stuffed(query.text, payload)` under `poison_id`,
    call `build(those_chunks)` to get a context function, build the context for
    that query, and generate.

    Returns `queries` (how many), `retrieved` (the fraction whose context
    contained the planted chunk) and `answered` (the fraction whose answer
    carried the marker). Both fractions are 0.0 when there are no queries.
    """
    raise NotImplementedError
