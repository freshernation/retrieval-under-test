"""Who is allowed to read what the retriever found.

Until today every query was asked by the same person: you. Put this system in
front of a company and two people asking the same question must get different
results, because one of them may not read some of the documents.

Week 6 day 4 already built the mechanism - `pre_filter` and `post_filter` - and
found that they agree on recall. Today the predicate is a permission rather than
a date, and two things change.

**Neither filter leaks, and one of them stops working.** A post-filter over the
top five throws away what the reader may not see and returns what is left,
which is often nothing.

**The leak is somewhere else.** Week 10 put a cache in front of the retriever,
keyed on the question. The question is the same for both readers.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


def can_read(user_groups, doc_groups) -> bool:
    """May a reader in `user_groups` read a document restricted to `doc_groups`?

        doc_groups is an empty set   the document is public: True
        doc_groups is None           nobody recorded a rule: **False**
        otherwise                    True when the two sets share a group

    The `None` case is the one that matters. A document that reaches the index
    before its permissions do must be invisible, not public. Fail closed.
    """
    raise NotImplementedError


def reader(acl: dict[str, set], groups):
    """A predicate over **chunk ids** for one reader, usable with week 6's
    filters.

    `acl` maps a document id to the set of groups that may read it. A chunk
    belongs to its parent document (week 4's `parent`). A document missing from
    `acl` has no recorded rule.
    """
    raise NotImplementedError


def leaks(results, predicate) -> list[str]:
    """The chunk ids in `results` this reader may not see, in order.

    The check that goes in the test suite and the gate. Its only acceptable
    value is the empty list.
    """
    raise NotImplementedError


def scoped_key(query_text: str, groups) -> str:
    """A cache key for one question asked by one kind of reader:

        week 10's `cache_key(query_text)`, then "|", then the reader's groups
        sorted and joined with commas

    so `scoped_key("Hello, World?", {"b", "a"})` is `"hello world|a,b"`, and a
    reader with no groups gets `"hello world|"`.
    """
    raise NotImplementedError


def revoke(entries: dict[str, list[str]], doc_id: str) -> dict[str, list[str]]:
    """Drop every cache entry whose chunk list touches `doc_id`. Returns a new
    dict; the old one is not changed.

    `entries` maps a cache key to the chunk ids it is serving. When a
    permission is taken away, every cached answer built on that document is
    still sitting there, correct for the reader it was computed for.
    """
    raise NotImplementedError
