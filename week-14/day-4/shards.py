"""Sharding, and the statistics it splits.

When one machine cannot hold the index, it is split into shards: each holds some of
the chunks, each is searched in parallel, and the results are merged. Scatter,
gather. It is how every large search system scales.

And BM25 is built from corpus statistics - document frequency, the number of
documents, the average length. A shard knows only its own. So the same chunk, with
the same words, scores differently depending on which shard it landed in and who
its neighbours are, and the merged list is not the list the whole index would give.

Week 12 met this from the other side: a tombstoned chunk kept voting in the
statistics. Here the statistics are split, and the fix is the same idea - make
every shard score with the statistics of the whole.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


def shard_of(chunk_id: str, n_shards: int) -> int:
    """sha256 of the id, as a number, mod n_shards. Stable on every machine."""
    raise NotImplementedError


def split(chunks: dict[str, str], n_shards: int) -> list[dict[str, str]]:
    """n_shards dicts; each chunk in its shard_of, in sorted-id order."""
    raise NotImplementedError


def build_shards(chunks: dict[str, str], n_shards: int, **options) -> list:
    """A week 3 Index over each part of split(), with these options."""
    raise NotImplementedError


def global_stats(shards: list, terms: list[str]) -> dict:
    """{"n_documents": total across shards, "average_length": the average over
    every chunk in every shard, "df": {term: total document frequency}}"""
    raise NotImplementedError


def score_shard(shard, terms: list[str], stats: dict, k1=None, b=None) -> dict[str, float]:
    """BM25 for every chunk in this shard that contains a term - week 3's
    `score_term`, summed over the terms - using stats["n_documents"] and
    stats["average_length"], and stats["df"][term] if stats has "df", otherwise the
    shard's own document frequency. k1 and b default to week 3's K1 and B."""
    raise NotImplementedError


def scatter_gather(shards: list, query: str, k: int = 10, shared: bool = True) -> list[str]:
    """Analyze the query with the first shard's analyzer. Score every shard - with
    global_stats when `shared`, otherwise with each shard's own n_documents and
    average_length (and no "df") - merge, and return the top k by score, ties by id.

    shared=False costs one round trip. shared=True costs two: one to gather the
    statistics, one to score with them."""
    raise NotImplementedError
