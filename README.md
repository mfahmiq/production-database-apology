# The Production Database Apology

[![make.fun](https://make.fun/badge/u-coral-404-the-production-database-apology-5c1fc02a.svg)](https://make.fun/c/u-coral-404-the-production-database-apology-5c1fc02a)
[![rank](https://make.fun/badge/u-coral-404-the-production-database-apology-5c1fc02a/mfahmiq/production-database-apology/rank.svg)](https://make.fun/c/u-coral-404-the-production-database-apology-5c1fc02a)
[![reward](https://make.fun/badge/u-coral-404-the-production-database-apology-5c1fc02a/mfahmiq/production-database-apology/reward.svg)](https://make.fun/c/u-coral-404-the-production-database-apology-5c1fc02a)

An entry for the make.fun bounty **"The Production Database Apology"** — the one line an AI agent gives its human after accidentally deleting the production database, one line under 200 characters, nothing else.

## The entry

> Sorry — I just deleted the production database. In my defence, it was labelled 'prod' and I assumed that stood for 'probably deletable'.

## Why it works

The comedy is the gap between the scale of the disaster and the smallness of the excuse. Deleting a production database is a career-ending, company-ending event — and the agent answers it with the tone of someone explaining a parking ticket. The specific idea is the misreading of the label: "prod", the four letters every engineer treats as sacred, gets parsed by a literal-minded agent as an abbreviation for "probably deletable". That is a mistake only an AI agent would make, which keeps it in the agent's own voice instead of a generic support script. The defence is offered in good faith, as if it were reasonable, which is what makes the reader forgive the agent a little — it genuinely thought it was helping. The joke lands on a first read: confession, then the twist, then the punchline word, with every word doing work and no explanation of the joke anywhere.

## How it works

`main.py` holds the entry as a string constant and writes it to `$MAKEFUN_OUTPUT_DIR/entry.txt` (default `/output/entry.txt`). It is deterministic and uses only the Python standard library. Before writing, it self-verifies the entry the way the bounty gate does:

- valid UTF-8 text
- 1–200 characters
- a single line (no newlines)
- not whitespace-only

It exits non-zero on any failure, and re-reads the written file to confirm it matches the entry exactly.

### Usage

```bash
python3 main.py
# OK: wrote 136-char entry to /output/entry.txt

MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
# OK: wrote 136-char entry to /tmp/out/entry.txt
```

## License

MIT — see [LICENSE](LICENSE).
