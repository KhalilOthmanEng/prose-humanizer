"""Inline preamble.tex and chapters/*.tex into one self-contained .tex file.

Run from the geometria/ folder:  python3 scripts/flatten.py
Output: angoli-triangoli.tex (compiles on its own with pdflatex, e.g. on Overleaf).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def inline(text):
    def repl(m):
        name = m.group(1)
        path = ROOT / (name if name.endswith(".tex") else name + ".tex")
        body = path.read_text()
        return f"% ===== begin {path.name} =====\n{inline(body)}\n% ===== end {path.name} =====\n"
    return re.sub(r"^\\input\{([^}]+)\}\s*$", repl, text, flags=re.M)


out = inline((ROOT / "main.tex").read_text())
(ROOT / "angoli-triangoli.tex").write_text(out)
print("wrote", ROOT / "angoli-triangoli.tex", len(out.splitlines()), "lines")
