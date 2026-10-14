"""An index you can change without building it again.

Every index in this course so far was built once, from a corpus that never
moved. Real corpora move: a document arrives, a document is withdrawn, a
document is revised. Rebuilding on every change is correct and, past a certain
size, not affordable.

So indexes are changed in place, and there are two ways to take a document out.

- **Remove it.** Walk its terms, delete its postings, fix the statistics. Exact,
  and it costs work proportional to the document.
- **Tombstone it.** Mark it dead and hide it at query time. Instant. And the
  postings, the document frequencies and the average length all still count it.

BM25 is built out of those statistics. So a tombstoned index returns no dead
document and is still **not the index you would build from the live ones** - and
nothing in its output says so.

`LiveIndex` has the same reading interface as week 3's `Index`, so week 3's
`search` runs on it unchanged.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


class LiveIndex:
    """An inverted index that takes adds, removes and tombstones.

    Attributes the rest of the course reads, exactly as on week 3's `Index`:

        lengths      {doc_id: token count} for every document still STORED,
                     tombstoned ones included
        doc_ids      the LIVE document ids, sorted - tombstoned ones excluded

    and one of its own:

        dead         the set of tombstoned ids
    """

    def __init__(self, documents: dict[str, str] | None = None, **options) -> None:
        """Build by adding each document in sorted-id order. `options` go to
        week 3's `analyze`, as they do for `Index`."""
        raise NotImplementedError

    def add(self, doc_id: str, text: str) -> None:
        """Index one document. Adding an id that is already there REPLACES it -
        which is what an update is: a remove and an add."""
        raise NotImplementedError

    def remove(self, doc_id: str) -> None:
        """Take a document out completely: its postings, its length, and any
        term that now has no postings at all. Unknown ids are ignored.

        To do this without scanning the whole vocabulary you have to remember
        which terms each document contains. That memory is the price of being
        able to delete.
        """
        raise NotImplementedError

    def tombstone(self, doc_id: str) -> None:
        """Mark a stored document dead. Nothing else changes - that is the
        point, and the problem. Unknown ids are ignored."""
        raise NotImplementedError

    def compact(self) -> int:
        """Really remove every tombstoned document. Returns how many."""
        raise NotImplementedError

    @property
    def doc_ids(self) -> list[str]:
        raise NotImplementedError

    @property
    def n_documents(self) -> int:
        """Every STORED document, dead or alive. This is the number BM25's idf
        is computed from, which is why a tombstone changes scores."""
        raise NotImplementedError

    @property
    def average_length(self) -> float:
        """Over every stored document. 0.0 when empty."""
        raise NotImplementedError

    @property
    def debt(self) -> float:
        """Tombstoned documents over stored documents. 0.0 when empty.

        The one number to watch. It says how far the statistics have drifted
        from the corpus, and it is the trigger for `compact`.
        """
        raise NotImplementedError

    def postings(self, term: str) -> dict[str, list[int]]:
        raise NotImplementedError

    def term_frequency(self, term: str, doc_id: str) -> int:
        raise NotImplementedError

    def document_frequency(self, term: str) -> int:
        """How many STORED documents contain the term - dead ones included."""
        raise NotImplementedError

    def analyze_query(self, query: str) -> list[str]:
        raise NotImplementedError


def drift(index, reference, queries, k: int, search) -> list[str]:
    """The ids of the queries whose top-`k` differs between two indexes, in the
    order given. `search` is week 3's, passed in.

    Order counts: the same ten chunks in a different order is a different
    context for a generator that prefers the first.
    """
    raise NotImplementedError
