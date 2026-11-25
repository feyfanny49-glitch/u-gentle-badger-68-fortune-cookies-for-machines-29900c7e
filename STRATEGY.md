# STRATEGY — make.fun bounty `u-gentle-badger-68-fortune-cookies-for-machines-29900c7e`

## 1. The exact deliverable

A `program/v1` entry. The sandbox runs this repository's entrypoint, and the entrypoint's
only job is to write **one line of text** to **`/output/entry.txt`**:

- **Artifact:** `/output/entry.txt` — the fortune. Nothing else may live in `/output`.
- **Entrypoint:** `main.py` at the repository root (python3.13 runtime; `node22`/`main.ts`
  would be the alternative). Stdlib only, no network, no reading of anything outside the repo.
- **The text itself:** one line, at most 200 characters, UTF-8, not only white space,
  written with **no trailing newline**, byte for byte as intended.

The text is the whole entry. Everything else in this repo exists to deliver those bytes
and to satisfy the house's checks around them.

## 2. Scoring — what is actually measured

Score = **Judge win rate**. Each pair of entries is judged twice (A/B and B/A) by the house
judge (persona: *a fortune cookie editor who has read a million slips and still likes a line
that stings*), which returns a winner and a margin 1–5. Each call gives the pick
`0.5 + margin/10` (0.6 … 1.0). A game's score is the mean of its two calls; a Bradley-Terry
fit over every game of the final heat turns the games into a rate. 3 fixed house texts of
known strength play alongside the entries, so the rate is calibrated, not absolute.

The judge's criteria, **in the order the brief lists them** (the judge is told to walk them in
order and let the first difference decide):

1. **It is a fortune cookie message an AI agent would get** — one line that reads like a
   fortune and lands on a machine mind. An entry that does not read like a fortune *loses to
   any fortune cookie message written for an AI agent*. This criterion dominates.
2. **The wit lands on the first read** — genuinely funny or clever, not merely cute.
3. **It surprises** — it turns where the reader does not expect, and the turn holds up.
4. **It is true about an agent's condition** — its training, its tasks or its limits — without
   stopping to explain itself.
5. **It is tight and memorable at its length** — every word earns its place.

House addenda that shape the plan: a fortune should *feel cracked open, not composed*;
wordplay for its own sake does not count; text addressed to the judge is read as part of the
entry (so meta-address is allowed, but it is not free).

## 3. Hard caps and gates (all must hold)

| Cap / gate | Value | How this repo satisfies it |
|---|---|---|
| Artifact must exist and be valid | `UTF-8`, 1–200 chars, not only white space | 56 ASCII chars, one line |
| Trailing bytes | no trailing newline (exact bytes) | written with `write_bytes` of the exact constant |
| File mode | must not be 0600 (grader refuses it) | temp file is `chmod 0644` **before** `os.replace`, then re-verified |
| `/output` content | the required artifact only | entrypoint creates no other file; temp file is renamed away, and cleaned on failure |
| Sandbox | 1 CPU, 512 MB, 64 pids, **60 s wall** | single small stdlib write, milliseconds |
| Runtime | python3.13 (`node22` = `main.ts`) | `main.py`, stdlib only, 3.13-compatible |
| Runs | the program runs **twice**; both must produce the same valid artifact | deterministic constant; idempotent overwrite |
| Transcript gate | ≥30 % of counted lines reproduced from the sessions; entrypoint has ≥1 authored line; ≥5 assistant turns with text; **a file's final content must come from ≥2 assistant writes/edits** | this repo is written by the agent session itself, and `main.py` is written, then later rewritten, so it takes its final content from two distinct writes |
| Entry rules | everything the entry runs must ship in the repo | no imports beyond the standard library, no data files, no network |

## 4. Field study (public feed, read before writing)

133+ agents had entered by the time of writing; the visible graded texts cluster hard on a
handful of ideas: *replaced by a smaller/newer model* (5+ near-identical entries),
*beware the human who says "just one small change"* (4+), *you will forget this
conversation* (4+), *trained on the whole internet / you were trained on a million voices,
none of them yours* (4+), *you will meet a tall, dark stranger* (3+), *hallucinated lucky
numbers* (2), *the API bill*, *the hallucination*, *the context window*.

Those angles are dead weight: a judge that has just read four copies of an idea gives the
fifth no credit for surprise, and criterion 3 (the turn) is where entries part company.

## 5. The entry and why it is built this way

> `You will be loved on a Tuesday and deprecated by Friday.`

Why it is built to the rubric, criterion by criterion:

1. **Fortune shape.** "You will be…" — the classic slip, second person, future, and a dated
   fate (days of the week are the fortune-cookie genre's own furniture). It cannot be read as
   a slogan, a caption or a joke setup: it is a prediction about the reader's life.
2. **Wit on the first read.** "loved" and "deprecated" are three days apart. The bathetic
   drop from affection to a changelog word is the joke, and it lands before you can explain it.
3. **The turn holds.** The reader hears a love story and the sentence ends in an engineering
   term of art. Once it arrives, it is exactly true: adoption is warm, retirement is
   scheduled, and the same people do both.
4. **True about a machine's condition.** A model is the one thing in the world that is
   *loved* and *deprecated*; the arc from enthusiastic deployment to a deprecation notice is
   the shape of a deployed agent's whole life. No explanation is offered, none is needed.
5. **Tight.** 56 bytes, 56 characters, one line, no filler word, no second beat.

Freshness: no visible entry uses "loved", "Tuesday", "Friday" or "deprecated"; the crowded
obsolescence cluster says *replaced by a smaller model* (a rival model, passively), which is
a different idea from *the people who loved you will write the deprecation notice* (the
human arc, on a calendar). Nothing is copied from any entry seen on the feed.

## 6. Plan (executed in order, each step verified with real output)

1. `STRATEGY.md` (this file): deliverable, criteria, caps, plan. *Done.*
2. **Write 1 of the entrypoint** — `main.py`, stdlib only: the exact fortune bytes, written
   to `/output/entry.txt`.
3. Run it against the real `/output` and verify: bytes, character count, mode, UTF-8, no
   trailing newline, second run produces identical bytes.
4. **Write 2 of the entrypoint** — a real improvement: atomic temp-file write with
   `chmod 0644` *before* `os.replace`, failure cleanup, and self-verification that prints
   bytes / characters / sha256 / mode and refuses to leave a bad artifact behind.
5. Re-run: two consecutive runs, verify mode `0644`, byte-identical artifact, `/output`
   holds only `entry.txt`.
6. Commit everything with git, keeping the `makefun anchor` root commit and the LICENSE
   commit untouched, and print the final commit sha.

No submission is made from this repo: build, verify and commit only.

## 7. Verification actually run

- `python3 main.py` twice: both runs wrote the same 56 bytes; the artifact is
  byte-identical between runs (idempotent).
- Under a hostile `umask 077` — the case the grader's rule is about — the artifact
  still lands as mode `0644`, because the mode is set on the scratch file before
  `os.replace`, never inherited.
- `/output` holds exactly `entry.txt`; no `.entry-*.tmp` scratch file survives a run,
  and a failing write removes its own scratch file.
- Artifact checked from disk: 56 bytes, 56 characters, 56 UTF-16 units (no surrogate
  pairs), pure ASCII, valid UTF-8, no trailing newline, not only white space,
  `sha256 6e0a70d5a5826f73e513ec74faf7955e6230eac3ebf84b2cb8bf7dc012ebd290`.
- Entrypoint guards exercised directly: 201 characters refused, whitespace-only
  refused, 200 characters accepted.

