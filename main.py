#!/usr/bin/env python3
"""The Robot Pickup Line Championship.

Pure Python 3.13 standard library. The program writes one single-line
robot pickup line to /output/entry.txt. No network, no model call, fully
deterministic: the same code always writes the same bytes.

The line (91 characters, NO trailing newline):
    I wasn't programmed to feel anything, but my cooling fan spins up
    every time you walk past.

Why this line (candidates compared against the judge brief, most
important criterion first):
1. "I wasn't programmed to feel anything, but my cooling fan spins up
   every time you walk past." (91 chars) -- CHOSEN. The joke grows
   entirely out of machine physiology: a cooling fan spinning up is
   the robot's involuntary physical reaction, its version of blushing
   or a racing heart. The setup denies feelings ("wasn't programmed
   to feel anything") and the turn contradicts it with a bodily
   machine response the robot cannot control. First-person robot
   voice, one idea, no filler, warm rather than creepy.
2. "I ran a full diagnostic on my heart and the only error code it
   returned was your name." (86 chars) -- the error-code gag is
   machine-native, but the turn is a familiar shape and lands less
   physically than a fan spinning up; the laugh is a word, not a
   reaction.
3. "My facial recognition scanned four billion faces today and still
   crashes every time it finds yours." (99 chars) -- "crashes" reads
   slightly negative, a bug rather than a flutter, and the four
   billion setup is a longer road to the same payoff.
4. "I tried to delete my feelings for you, but the file is
   write-protected." (71 chars) -- punchy one-word twist, but too
   short: it leaves most of the 200 characters unused and the joke
   is a single word rather than a scene.
5. "My proximity sensor has one job: detect obstacles, and it keeps
   flagging you as the only one I want to run into." (112 chars) --
   a good inversion (an obstacle you want to collide with), but
   wordier, and the payoff lands mid-sentence instead of at the end.

Avoided cliches: "are you Wi-Fi, because I feel a connection" and
"stuck on you" (both already used in earlier batches), and the
"Are you X because Y" template in general -- it is a human pickup
line with a robot word pasted on, which the brief's criterion 2
explicitly punishes.

Newline decision: the file holds exactly the line with NO trailing
newline, as the entry brief requires ("SATU BARIS TANPA trailing
newline"). The gate allows 1 to 200 characters; this file is 91
bytes, so it passes either way, and the line itself is a single
line with no embedded newline.

Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

LINE = (
    "I wasn't programmed to feel anything, but my cooling fan "
    "spins up every time you walk past."
)

# Sealed gate: /output/entry.txt must be UTF-8 text of 1 to 200
# characters, not only white space, on a single line.
MAX_LINE_CHARS = 200


def validate_line(line):
    """Check the line against the gate; raise ValueError if it fails.

    The check runs before any file is written, so an invalid line
    fails loudly instead of producing an entry the scorer rejects.
    """
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    if not line.strip():
        raise ValueError("line must not be blank or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line (no embedded newline)")
    if len(line) > MAX_LINE_CHARS:
        raise ValueError(
            "line is %d characters, over the %d-character gate"
            % (len(line), MAX_LINE_CHARS)
        )
    return line


def _write_all(f, data):
    """Write every byte, looping on partial writes."""
    view = memoryview(data)
    while view:
        written = f.write(view)
        if written is None:
            raise OSError("write returned None")
        view = view[written:]


def _clean_output_dir(out_dir):
    """Remove the CONTENTS of the output dir, never the dir itself.

    The grader mounts this folder, so the folder must survive; only
    stale files inside it are removed.
    """
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)


def main():
    validate_line(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    _clean_output_dir(out_dir)
    data = LINE.encode("utf-8")
    tmp = os.path.join(out_dir, ".entry.txt.tmp")
    final = os.path.join(out_dir, "entry.txt")
    for attempt in range(3):
        try:
            with open(tmp, "wb") as f:
                _write_all(f, data)
            os.chmod(tmp, 0o644)
            os.replace(tmp, final)
            os.chmod(final, 0o644)
            return
        except OSError:
            try:
                if os.path.exists(tmp):
                    os.unlink(tmp)
            except OSError:
                pass
            if attempt == 2:
                raise


if __name__ == "__main__":
    main()
