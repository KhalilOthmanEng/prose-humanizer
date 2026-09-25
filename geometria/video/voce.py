"""Italian narration for the lesson video.

Offline text to speech with Kokoro (ONNX), voices ``if_sara`` (female) or
``im_nicola`` (male). Every sentence is synthesised once and cached as a WAV
file named after a hash of (voice, speed, spoken text), so re-renders are fast.

The scene file imports only ``synth`` and ``wrap``; all file access lives here,
which keeps the scene file clean for the static render gate.

Environment variables:
    KOKORO_DIR        folder with kokoro-v1.0.onnx and voices-v1.0.bin (default ./kokoro)
    LEZIONE_VOCE      if_sara (default) or im_nicola
    LEZIONE_VELOCITA  speaking speed, default 0.95
"""
from __future__ import annotations

import hashlib
import os
import re
import textwrap
from pathlib import Path

import numpy as np
import soundfile as sf

HERE = Path(__file__).resolve().parent
AUDIO_DIR = HERE / "audio"
MODEL_DIR = Path(os.environ.get("KOKORO_DIR", HERE / "kokoro"))
VOICE = os.environ.get("LEZIONE_VOCE", "if_sara")
SPEED = float(os.environ.get("LEZIONE_VELOCITA", "0.95"))

# Italian names of the letters, used to spell point and triangle names aloud
LETTERS = {
    "A": "a", "B": "bi", "C": "ci", "D": "di", "E": "e", "F": "effe", "G": "gi",
    "H": "acca", "K": "cappa", "L": "elle", "M": "emme", "N": "enne", "O": "o",
    "P": "pi", "Q": "cu", "R": "erre", "S": "esse", "T": "ti", "X": "ics",
}

_kokoro = None


def speakable(text: str) -> str:
    """Turn a caption into text the Italian voice reads correctly."""
    t = text
    t = t.replace("c.v.d.", "come volevasi dimostrare")
    t = t.replace("°", " gradi")
    t = re.sub(r"(\d+),(\d+)", r"\1 virgola \2", t)
    t = re.sub(r"(\d)x\b", r"\1 ics", t)
    t = re.sub(r"\bx\b", "ics", t)

    # 1 to 3 capital letters standing alone (AB, ABC, H, LAL) are spelled out;
    # a capital followed by an apostrophe (L'angolo, E') is a normal word.
    def spell(m: re.Match) -> str:
        return " ".join(LETTERS.get(ch, ch) for ch in m.group(0))

    t = re.sub(r"(?<![\w'’])[A-Z]{1,3}(?![\w'’])", spell, t)
    return t


def _model():
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(str(MODEL_DIR / "kokoro-v1.0.onnx"),
                         str(MODEL_DIR / "voices-v1.0.bin"))
    return _kokoro


def _trim(samples: np.ndarray, sr: int, thr: float = 0.01) -> np.ndarray:
    idx = np.where(np.abs(samples) > thr)[0]
    if idx.size == 0:
        return samples
    a = max(0, idx[0] - int(0.03 * sr))
    b = min(samples.size, idx[-1] + int(0.08 * sr))
    out = samples[a:b].astype(np.float32)
    peak = float(np.max(np.abs(out))) or 1.0
    out = out * (0.9 / peak)
    fade = int(0.01 * sr)
    out[:fade] *= np.linspace(0, 1, fade)
    out[-fade:] *= np.linspace(1, 0, fade)
    return out


def synth(text: str) -> tuple[str, float]:
    """Return (wav path, duration in seconds) for one caption."""
    spoken = speakable(text)
    key = hashlib.sha1(f"{VOICE}|{SPEED}|{spoken}".encode("utf-8")).hexdigest()[:16]
    AUDIO_DIR.mkdir(exist_ok=True)
    wav = AUDIO_DIR / f"{key}.wav"
    if not wav.exists():
        samples, sr = _model().create(spoken, voice=VOICE, speed=SPEED, lang="it")
        tmp = wav.with_suffix(".tmp.wav")
        sf.write(tmp, _trim(np.asarray(samples), sr), sr)
        tmp.replace(wav)
    info = sf.info(str(wav))
    return str(wav), info.frames / info.samplerate


def wrap(text: str, width: int = 74) -> str:
    """Caption line breaks (at most three lines in practice)."""
    return "\n".join(textwrap.wrap(text, width))


if __name__ == "__main__":
    for s in ["L'angolo AB è di 65°.", "Il triangolo ABC è congruente a DEF, c.v.d.",
              "E un'altra trappola: 3x + 10 = 2x + 40, h = 2,4.", "Il criterio LAL."]:
        print(s, "->", speakable(s))
