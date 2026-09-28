"""Shared style and helpers for the second video series (videos 1 to 6).

Same visual language as lezione_geometria.py (first video): dark 3b1b background,
Lato captions at the bottom, one colour per idea. Narration: offline Kokoro voice
``if_sara`` (voce.py), about 10 percent slower than the first video, as requested.

Colour vocabulary (kept identical across the whole series):
  COL_ANG  yellow  the quantity we are looking at
  COL_GIV  blue    the data / what is given
  COL_RES  green   the result / what we find
  COL_AUX  purple  helpers (constructions, auxiliary lines, operations)
  COL_ERR  red     traps and wrong answers
"""
from contextlib import contextmanager

import numpy as np
from manim import *

import voce
from voce import synth, wrap

voce.SPEED = 0.86          # the first video used 0.95; the tutor asked for slower speech

# LaTeX: default Manim template plus the cancel package (strike-through simplification)
TPL = TexTemplate()
TPL.add_to_preamble(r"\usepackage{cancel}")
MathTex.set_default(tex_template=TPL)
Tex.set_default(tex_template=TPL)

# ── colours ─────────────────────────────────────────────────────────────
BG = "#1C1C2E"
COL_ANG = "#FFD166"
COL_ANG2 = "#F4A261"
COL_ANG3 = "#FF8FAB"
COL_GIV = "#7EB6FF"
COL_RES = "#06D6A0"
COL_AUX = "#B084F5"
COL_ERR = "#EF476F"
COL_GRID = "#5E5E5E"
COL_WOOD = "#C68B59"
FONT = "Lato"
PIE = ["#EF8A6A", "#7EB6FF", "#06D6A0", "#FFD166", "#B084F5", "#FF8FAB"]


# ── pure geometry (numpy only) ─────────────────────────────────────────
def P(x, y):
    return np.array([float(x), float(y), 0.0])


def unit(deg):
    r = np.radians(deg)
    return np.array([np.cos(r), np.sin(r), 0.0])


def norm(v):
    return float(np.linalg.norm(v))


def foot(Pt, A, B):
    d = B - A
    t = np.dot(Pt - A, d) / np.dot(d, d)
    return A + t * d


# ── text and shapes ────────────────────────────────────────────────────
def T(s, fs=30, col=WHITE, **kw):
    return Text(s, font=FONT, font_size=fs, color=col, **kw)


def M(s, fs=40, col=WHITE):
    return MathTex(s, font_size=fs, color=col)


def MS(*parts, fs=44, col=WHITE):
    """MathTex split into substrings, for TransformMatchingTex"""
    return MathTex(*parts, font_size=fs, color=col)


def seg(A, B, col=WHITE, w=3.5):
    return Line(A, B, color=col, stroke_width=w)


def poly(*pts, col=WHITE, fill=None, op=0.25, w=3):
    p = Polygon(*pts, color=col, stroke_width=w)
    if fill is not None:
        p.set_fill(fill, opacity=op)
    return p


def rmark(V, A, B, s=0.22, col=WHITE):
    u = (A - V) / norm(A - V)
    w = (B - V) / norm(B - V)
    return VMobject(color=col, stroke_width=2.5).set_points_as_corners(
        [V + u * s, V + u * s + w * s, V + w * s])


def wedge(c, a0, sweep, r=0.6, col=COL_ANG, op=0.4):
    return AnnularSector(inner_radius=0, outer_radius=r, angle=np.radians(sweep),
                         start_angle=np.radians(a0), arc_center=c,
                         fill_opacity=op, color=col, stroke_width=0)


def caption(text):
    t = Text(wrap(text), font=FONT, font_size=24, color="#ECECEC", line_spacing=0.75)
    if t.width > 13.3:
        t.scale_to_fit_width(13.3)
    t.to_edge(DOWN, buff=0.22)
    bg = BackgroundRectangle(t, color=BG, fill_opacity=0.9, buff=0.12)
    return VGroup(bg, t)


def lines_column(items, fs=34, buff=0.3, aligned=LEFT):
    """items: list of (MathTex string, colour); returns an arranged VGroup"""
    return VGroup(*[M(s, fs, c) for s, c in items]).arrange(DOWN, aligned_edge=aligned, buff=buff)


def pie(center, radius, values, colors, start=90.0):
    """clockwise pie chart; returns (VGroup of sectors, list of (mid angle, sweep))"""
    tot = float(sum(values))
    a = start
    secs, info = VGroup(), []
    for v, c in zip(values, colors):
        sw = 360.0 * v / tot
        secs.add(AnnularSector(inner_radius=0, outer_radius=radius, angle=-np.radians(sw),
                               start_angle=np.radians(a), arc_center=center,
                               fill_opacity=0.85, color=c, stroke_width=0))
        info.append((a - sw / 2, sw))
        a -= sw
    return secs, info


def unit_squares(rows, cols, side, origin, col=COL_GIV, op=0.35, stroke=1.2):
    """grid of unit squares, row 0 at the bottom; returns VGroup ordered row by row"""
    g = VGroup()
    for r in range(rows):
        for c in range(cols):
            sq = Square(side_length=side, color=col, stroke_width=stroke).set_fill(col, op)
            sq.move_to(origin + P((c + 0.5) * side, (r + 0.5) * side))
            g.add(sq)
    return g


# ── oblique (cavalier) boxes for solid geometry ────────────────────────
def box_pts(o, a, b, c, s=1.0, ang=35, k=0.5):
    """corners of a box of width a, depth b, height c drawn from front bottom left o.
    Front face A B C D, back face E F G H (E behind A)."""
    d = k * s * b * unit(ang)
    A = o
    B = o + P(a * s, 0)
    C = o + P(a * s, c * s)
    D = o + P(0, c * s)
    return dict(A=A, B=B, C=C, D=D, E=A + d, F=B + d, G=C + d, H=D + d)


def box_mob(p, col=WHITE, fill=COL_GIV, op=0.18, w=3):
    """visible faces (front, top, right) filled, hidden edges dashed"""
    front = poly(p["A"], p["B"], p["C"], p["D"], col=col, fill=fill, op=op, w=w)
    top = poly(p["D"], p["C"], p["G"], p["H"], col=col, fill=fill, op=op * 0.7, w=w)
    right = poly(p["B"], p["F"], p["G"], p["C"], col=col, fill=fill, op=op * 1.3, w=w)
    hidden = VGroup(DashedLine(p["A"], p["E"], color=col, stroke_width=1.5, dash_length=0.1),
                    DashedLine(p["E"], p["F"], color=col, stroke_width=1.5, dash_length=0.1),
                    DashedLine(p["E"], p["H"], color=col, stroke_width=1.5, dash_length=0.1))
    return VGroup(hidden, front, right, top)


def small_cube(o, s=0.3, ang=35, k=0.5, col=COL_GIV):
    p = box_pts(o, 1, 1, 1, s, ang, k)
    return VGroup(poly(p["A"], p["B"], p["C"], p["D"], col=WHITE, fill=col, op=0.75, w=1),
                  poly(p["D"], p["C"], p["G"], p["H"], col=WHITE, fill=col, op=0.5, w=1),
                  poly(p["B"], p["F"], p["G"], p["C"], col=WHITE, fill=col, op=0.95, w=1))


# ── the lesson scene ───────────────────────────────────────────────────
class LessonScene(Scene):
    VIDEO = 0
    VTITLE = ""
    PART = 0
    TITLE = ""

    def setup(self):
        self.camera.background_color = BG
        self.head = None

    def header(self):
        self.head = T(f"Video {self.VIDEO} · {self.VTITLE}  ·  {self.TITLE}", 20, GRAY_B).to_corner(UL, buff=0.3)
        self.play(FadeIn(self.head), run_time=0.4)

    def title_card(self):
        a = T(f"Parte {self.PART}", 26, GRAY_B)
        b = T(self.TITLE, 50, WHITE, weight=BOLD)
        g = VGroup(a, b).arrange(DOWN, buff=0.3)
        self.play(FadeIn(g, shift=UP * 0.2), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(g), run_time=0.5)
        self.header()

    def video_card(self, subtitle, intro):
        """opening card of a video (Parte 1 only): title, subtitle and a spoken intro"""
        a = T(f"Video {self.VIDEO}", 28, GRAY_B)
        b = T(self.VTITLE, 56, WHITE, weight=BOLD)
        c = T(subtitle, 30, COL_ANG)
        g = VGroup(a, b, c).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        with self.say(intro):
            self.play(FadeIn(a), Write(b), run_time=1.8)
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(g), run_time=0.5)
        self.wait(0.2)

    @contextmanager
    def say(self, text, pad=0.35):
        path, dur = synth(text)
        cap = caption(text)
        self.add_foreground_mobjects(cap)
        # add the sound through the file writer: Scene.add_sound is skipped after
        # a play() served from Manim's cache (see the first video, commit b9cc888)
        self.renderer.file_writer.add_sound(path, self.time)
        t0 = self.time
        yield dur
        rest = dur + pad - (self.time - t0)
        if rest > 0.02:
            self.wait(rest)
        self.remove_foreground_mobjects(cap)
        self.remove(cap)

    def wipe(self, keep_header=True):
        mobs = [m for m in self.mobjects if not (keep_header and m is self.head)]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.5)
        self.wait(0.2)

    def end(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.6)
        self.wait(0.4)

    def exercises(self, codes, spoken, lines):
        """closing card: which exercises of the worksheet go with this video"""
        h = T("Adesso tocca a te!", 48, COL_ANG, weight=BOLD).move_to(UP * 2.95)
        f = T("File «Esercizi di matematica»", 28, GRAY_B).next_to(h, DOWN, buff=0.2)
        chips = VGroup()
        for code, col in codes:
            box = RoundedRectangle(width=1.35, height=0.75, corner_radius=0.12, color=col, stroke_width=3)
            lab = T(code, 30, col, weight=BOLD).move_to(box)
            chips.add(VGroup(box, lab))
        chips.arrange_in_grid(cols=min(7, len(chips)), buff=0.25).next_to(f, DOWN, buff=0.35)
        tips = VGroup(*[T(s, 26, WHITE) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        tips.next_to(chips, DOWN, buff=0.35)
        with self.say(spoken):
            self.play(Write(h), FadeIn(f), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in chips], lag_ratio=0.12), run_time=1.6)
            self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in tips], lag_ratio=0.3), run_time=1.4)
        with self.say("Buon lavoro, e ci vediamo al prossimo video!"):
            self.play(Circumscribe(h, color=COL_ANG))
        self.wait(0.6)
        self.end()
