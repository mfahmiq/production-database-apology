"""The Production Database Apology — make.fun text bounty entry.

The brief
---------
Write the one line an AI agent gives its human after accidentally
deleting the production database. One line, under 200 characters,
nothing else. The entry is judged on the line itself: it has to read
as the agent's own voice, land the joke on a first read, and stay
inside the gate (valid UTF-8, 1-200 characters, a single line).

Why this line works
-------------------
The comedy is a scale mismatch: deleting a production database is a
career-ending disaster, and the agent answers it in the tone of
someone explaining a parking ticket. The confession ("Sorry — I just
deleted the production database") is blunt and immediate, with no
hedging and no preamble, because hedging would soften the disaster
and the joke needs the full weight of it up front.

The twist is the misreading of the label. "prod" is four letters
every engineer treats as sacred; the agent parses them literally as
an abbreviation for "probably deletable". That is a mistake only a
literal-minded agent would make, which keeps the joke in the agent's
own voice instead of a generic support script. It also reframes the
label as permission: the agent did not act out of malice or
carelessness, it thought the system was telling it the database was
fair game. The defence is offered in good faith, as if it were
reasonable, which is what makes the reader forgive the agent a
little — it genuinely thought it was helping.

"In my defence" does two jobs at once. The courtroom phrasing
elevates a trivial excuse into a formal plea, and the British
spelling keeps the dry, understated register the whole line lives
in. The em-dash after "Sorry" is a beat: apology, pause, confession,
pause, excuse. The punchline word is "deletable" — it lands last,
and the line stops there, with no explanation of the joke anywhere.

Alternatives considered and rejected
-------------------------------------
* Blaming the human ("you never told me not to"): shifts the blame
  and makes the agent unsympathetic; the brief asks for an apology,
  not an accusation.
* A technical excuse ("the DROP TABLE ran before the confirmation
  dialog finished"): jargon with no punchline word, and it reads
  like a bug report rather than an apology.
* A different misreading ("I read prod as short for produce"):
  weaker wordplay — "probably deletable" is funnier because it turns
  the label into an instruction to delete.
* A longer, multi-sentence apology: rejected by the gate (one line,
  200 characters) and by the joke — the punch needs brevity, and
  every extra word dilutes the landing.
* Confession only, no defence ("Sorry, I deleted the production
  database"): no twist, just a statement of fact; the humour lives
  entirely in the excuse.

How this program works
----------------------
The entry is a single string constant, so the output is
byte-deterministic: the same input always produces the same file.
Before writing, the entry is validated against exactly the gates the
bounty applies (UTF-8, 1-200 characters, a single line, not
whitespace-only). The file is written, re-read, and compared against
the constant, so a silent partial write fails loudly instead of
submitting a corrupted entry. Deterministic, Python standard library
only, exits non-zero on any failure.
"""

import os
import sys

# The entry itself. Kept as one constant, built from three literal
# fragments only so no line exceeds a comfortable width — the joined
# string is the entry exactly as it appears in entry.txt. The em-dash
# is written as the \u2014 escape so the source file stays pure ASCII
# and the character cannot be mangled by an editor or a re-encode;
# the resulting string is identical either way.
ENTRY = (
    "Sorry \u2014 I just deleted the production database. "
    "In my defence, it was labelled 'prod' and I assumed "
    "that stood for 'probably deletable'."
)

# The bounty gate: the entry must be between 1 and 200 characters
# inclusive. At 136 characters this entry sits comfortably inside
# the limit, which is deliberate — the joke needs no more room, and
# headroom means the gate can never be tripped by a stray edit.
MIN_CHARS = 1
MAX_CHARS = 200


def check_utf8(entry: str) -> str | None:
    """Return an error message if the entry is not valid UTF-8."""
    try:
        entry.encode("utf-8")
    except UnicodeEncodeError as exc:
        return f"entry is not valid UTF-8: {exc}"
    return None


def check_length(entry: str) -> str | None:
    """Return an error message if the entry is outside 1-200 chars."""
    if not MIN_CHARS <= len(entry) <= MAX_CHARS:
        return (
            f"entry is {len(entry)} chars, "
            f"must be {MIN_CHARS}-{MAX_CHARS}"
        )
    return None


def check_single_line(entry: str) -> str | None:
    """Return an error message if the entry spans more than one line.

    The bounty asks for one line, so any newline or carriage return
    inside the entry is a failure — the trailing newline the file
    itself carries is added at write time, not part of the entry.
    """
    if "\n" in entry or "\r" in entry:
        return "entry must be a single line"
    return None


def check_not_blank(entry: str) -> str | None:
    """Return an error message if the entry is whitespace-only."""
    if not entry.strip():
        return "entry must not be whitespace-only"
    return None


def validate(entry: str) -> list[str]:
    """Run every bounty gate and return the list of failures.

    Each gate is its own function so a failure names the exact gate
    that tripped, and so a gate can be tested or tightened on its own
    without touching the others. An empty list means the entry passes.
    """
    checks = (check_utf8, check_length, check_single_line, check_not_blank)
    return [error for check in checks if (error := check(entry)) is not None]


def resolve_output_path() -> str:
    """Return the full path of the entry file to write.

    The bounty harness sets MAKEFUN_OUTPUT_DIR; when it is unset the
    default /output keeps local runs working with no setup.
    """
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(output_dir, "entry.txt")


def write_entry(path: str, entry: str) -> None:
    """Write the entry plus one trailing newline to path.

    Explicit UTF-8 and newline="\\n" make the output byte-identical
    on any platform: no locale-dependent encoding, no CRLF on
    Windows. The directory is created first so a fresh container
    without /output does not fail on a missing directory.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(entry + "\n")


def verify_written(path: str, entry: str) -> str | None:
    """Re-read the written file; return an error unless it matches.

    The submission pipeline hashes entry.txt, so a silent partial
    write would be worse than a loud failure — this check fails
    before any success is reported.
    """
    with open(path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != entry + "\n":
        return "written file does not match the entry"
    return None


def main() -> int:
    """Validate the entry, write it, verify it, report the result.

    Order matters: validate before writing, so a bad entry never
    reaches the file; verify after writing, so a bad write is never
    reported as success. Any failure prints which gate tripped and
    exits non-zero, so the harness treats it as failed rather than
    silently submitting a bad entry.
    """
    errors = validate(ENTRY)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    output_path = resolve_output_path()
    write_entry(output_path, ENTRY)

    if (error := verify_written(output_path, ENTRY)) is not None:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(f"OK: wrote {len(ENTRY)}-char entry to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
