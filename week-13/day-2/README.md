# Day 2 — An index that survives a restart

> **By the end of today** the index is written to disk so that a crash cannot leave half
> of it, and read back only by an analyzer that matches the one that built it.

---

## Read first

- [ ] [**The snapshot and its analyzer**](../../content/week-13/day-2/the-snapshot-and-its-analyzer.md) — 25 min

---

## Predict first

You load a snapshot built with `stopwords=None` into a service whose analyzer removes
stopwords from queries.

**For how many of the 26 queries does the top ten change?** And at rank one?

---

## The lab

`snapshot.py`.

```python
fingerprint(index)      manifest(index)
save(index, path, writer=None)
load(path, **options)   SnapshotMismatch
```

```bash
pytest week-13/day-2 -v
```

---

## The written exercise

`week-13/day-2/snapshot.md`, one page.

1. Your prediction, and the answer
2. What `os.replace` guarantees, and what it does not (a different disk; a power cut)
3. The snapshot is 750 kB for 266 chunks. Estimate it for a million, and say what you
   would change first
4. Name one more thing that should be in the manifest, and the failure it would catch
