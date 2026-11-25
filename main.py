"""Meeting-email writer: one fixed line about a meeting that should have been an email."""

import os, string, sys

TEXT = "This meeting could have been an email, but the email would have needed a meeting to explain why it was an email."
LIMIT = 200
ENDERS = ".!?"

def fail(msg):
    sys.stderr.write("invalid: " + msg + "\n")
    raise SystemExit(1)

def validate(text):
    lowered = text.casefold()
    tripled = any(text[i] == text[i + 1] == text[i + 2] for i in range(len(text) - 2))
    rules = [
        (lowered.count("email") < 2, "says email fewer than twice"),
        (tripled, "one character repeated three times in a row"),
        (not text.strip(), "blank entry"),
        (len(text) > LIMIT, "over 200 characters"),
        (any(ord(c) < 32 or ord(c) == 127 for c in text), "control character found"),
        (text != text.strip() or "  " in text or "\n" in text, "ragged edges, double space, or newline"),
        (bool(text) and text[-1] not in ENDERS, "must end with . ! or ?"),
        (all(c in string.punctuation for c in text), "punctuation only"),
        (text.isdigit(), "digits only"),
        (not any(c.isalpha() for c in text), "no letters"),
        (text.startswith("-") or text.endswith("-"), "leading or trailing hyphen"),
    ]
    for bad, msg in rules:
        if bad:
            fail(msg)

def write_out():
    validate(TEXT)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(TEXT + "\n")

if __name__ == "__main__":
    write_out()
