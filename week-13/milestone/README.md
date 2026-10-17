# Milestone 13 — The service, operated

> **Ship:** a retrieval service that boots from its snapshot, takes changes through a
> queue, survives a restart without forgetting what it withdrew, and says whether it is
> ready to take traffic.

---

## The brief

### 1. Write `operations.py`

`boot`, `work_once`, `create_service`, `operations_check`, `save_versions`.

### 2. Run it

```bash
cd week-13/milestone
uvicorn run_service:app          # and, in another terminal:
python3 run_worker.py
```

Deep track: write the `Dockerfile` and `compose.yaml`, run both containers on one volume,
and kill the worker in the middle of a drain.

### 3. Withdraw something, restart, redeliver

The test does it with RFC 7159. Do it by hand too, and watch the version decide.

### 4. Write `REPORT.md`

---

## The rubric

| Station | This week |
|---|---|
| 1 Corpus | Changes arrive from outside, in any order. Who decides which version is true? |
| 3 Index | Built once, then changed in place, then written to disk and read back |
| 7 Measure | The gate runs on every pull request, and the baseline moves only with a reason |

---

## Check it

```bash
pytest week-13/milestone -v
python3 tools/check_evals.py
```
