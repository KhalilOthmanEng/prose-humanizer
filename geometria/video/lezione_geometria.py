"""
Angoli e triangoli congruenti: una lezione animata
=================================================
Generated with the 3b1b-style Scientific Explanation Skill.
Italian narration (offline Kokoro voice, see voce.py) with burned in captions.

Acts:
  P01_Porta           the door: an angle is a turn; the long sides trap
  P02_Circonferenza   measuring on a circle; the degree
  P03_Perche360       why 360: divisors, base 60, the year; a pie chart
  P04_Tipi            types of angles with a turning ray; clock angles (2:30 = 105)
  P05_Coppie          complementary, supplementary, explementary; vertical angles proof
  P06_Parallele       parallels and a transversal: slide, F, Z, C; traps; 65 degree example
  P07_Somma180        torn corners, then the proof with the parallel line; examples
  P08_Altezze         altitude, orthocentre in three cases, the 3-4-5 triangle turned three ways
  P09_Congruenza      rigid motions, corresponding parts, the two traps
  P10_Criteri         SAS, ASA, SSS as constructions; rigidity; why SSA and AAA fail
  P11_Dimostrazioni   base angles of an isosceles triangle; the altitude problem
  P12_Quaderno        the two problems from the student's notebook
  P13_Riepilogo       summary and farewell

Render (final quality, 1080p 60 fps):
  manim -qh lezione_geometria.py P01_Porta   (one command per act)
Concatenate:
  python concat.py

Colour vocabulary (one colour, one idea):
  COL_ANG  yellow  the angle being measured      (COL_ANG2, COL_ANG3: second and third angle)
  COL_GIV  blue    the givens / hypothesis
  COL_RES  green   what we prove / the result
  COL_AUX  purple  auxiliary constructions (transversal, parallel, altitude, bisector)
  COL_ERR  red     traps and wrong answers
"""

from contextlib import contextmanager

import numpy as np
from manim import *

from voce import synth, wrap

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
COL_DOOR = "#C68B59"
FONT = "Lato"

# ── pure geometry helpers (numpy only) ─────────────────────────────────


def P(x, y):
    return np.array([x, y, 0.0])


def unit(deg):
    r = np.radians(deg)
    return np.array([np.cos(r), np.sin(r), 0.0])


def dirdeg(v):
    return float(np.degrees(np.arctan2(v[1], v[0])))


def norm(v):
    return float(np.linalg.norm(v))


def foot(Pt, A, B):
    d = B - A
    t = np.dot(Pt - A, d) / np.dot(d, d)
    return A + t * d


def intersect(P1, P2, P3, P4):
    x1, y1, x2, y2 = P1[0], P1[1], P2[0], P2[1]
    x3, y3, x4, y4 = P3[0], P3[1], P4[0], P4[1]
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
    return P(px, py)


def convex(V, A, B):
    """start direction and sweep (degrees) of the convex angle AVB"""
    a, b = dirdeg(A - V), dirdeg(B - V)
    sweep = (b - a) % 360
    if sweep > 180:
        a, sweep = b, 360 - sweep
    return a, sweep


# ── precomputed geometry (checked in the __main__ block) ───────────────
# Act 6: r: y = 1.3, s: y = -1.2, transversal through Q at 65 deg
Q6 = P(-0.6, -1.2)
P6 = Q6 + P(2.5 / np.tan(np.radians(65)), 2.5, )  # (0.566, 1.3)
# Act 7: triangle with angles 50, 60, 70 and AB = 5
A7 = P(-3.4, -2.0)
B7 = P(1.6, -2.0)
AC7 = 5 * np.sin(np.radians(60)) / np.sin(np.radians(70))
C7 = A7 + AC7 * unit(50)
# Act 8 example: AB = 10, altitude from C = 6, AC = 12 (0.5 scene units per cm)
A8 = P(-5.6, -2.2)
B8 = A8 + P(5.0, 0)
C8 = A8 + 0.5 * P(np.sqrt(12 ** 2 - 6 ** 2), 6)
# Act 10: SAS / ASA / SSS triangle, unit 1.2: AB = 3.4, AC = 2.5, angle A = 55
U10 = 1.2
A10 = P(-2.4, -1.9)
B10 = A10 + P(3.4 * U10, 0)
C10 = A10 + 2.5 * U10 * unit(55)
BC10 = norm(C10 - B10)                       # = 2.839 * 1.2
ANG_B10 = 180 - dirdeg(C10 - B10)            # = 46.17 deg
# Act 10: SSA, angle A = 30, AB = 6, BC = 4 (unit 0.62)
U_SSA = 0.62
_b = 12 * np.cos(np.radians(30))
T1_SSA = (_b + np.sqrt(_b * _b - 80)) / 2   # 7.842
T2_SSA = (_b - np.sqrt(_b * _b - 80)) / 2   # 2.550

# ── Manim helpers ───────────────────────────────────────────────────────


def T(s, fs=30, col=WHITE, **kw):
    return Text(s, font=FONT, font_size=fs, color=col, **kw)


def M(s, fs=40, col=WHITE):
    return MathTex(s, font_size=fs, color=col)


def wedge(c, a0, sweep, r=0.6, col=COL_ANG, op=0.4):
    if sweep < 0.3:
        return VMobject()
    return AnnularSector(inner_radius=0, outer_radius=r, angle=np.radians(sweep),
                         start_angle=np.radians(a0), arc_center=c,
                         fill_opacity=op, color=col, stroke_width=0)


def arcm(c, a0, sweep, r=0.6, col=COL_ANG, w=3):
    if sweep < 0.3:
        return VMobject()
    return Arc(radius=r, start_angle=np.radians(a0), angle=np.radians(sweep),
               arc_center=c, color=col, stroke_width=w)


def angle_mark(V, A, B, r=0.55, col=COL_ANG, op=0.4):
    a, s = convex(V, A, B)
    return VGroup(wedge(V, a, s, r, col, op), arcm(V, a, s, r, col, 2.5))


def angle_label_pos(V, A, B, dist):
    a, s = convex(V, A, B)
    return V + dist * unit(a + s / 2)


def ticks(A, B, n=1, col=WHITE, size=0.13, gap=0.08):
    Mid = (A + B) / 2
    d = (B - A) / norm(B - A)
    nv = np.array([-d[1], d[0], 0.0])
    return VGroup(*[
        Line(Mid + d * gap * (i - (n - 1) / 2) - nv * size,
             Mid + d * gap * (i - (n - 1) / 2) + nv * size,
             color=col, stroke_width=3)
        for i in range(n)])


def rmark(V, A, B, s=0.22, col=WHITE):
    u = (A - V) / norm(A - V)
    w = (B - V) / norm(B - V)
    return VMobject(color=col, stroke_width=2.5).set_points_as_corners(
        [V + u * s, V + u * s + w * s, V + w * s])


def seg(A, B, col=WHITE, w=3.5):
    return Line(A, B, color=col, stroke_width=w)


def tri(A, B, C, col=WHITE, fill=None, op=0.18, w=3.5):
    t = Polygon(A, B, C, color=col, stroke_width=w)
    if fill is not None:
        t.set_fill(fill, opacity=op)
    return t


def vlabel(name, V, centroid, col=WHITE, fs=34, dist=0.32):
    d = V - centroid
    d = d / norm(d)
    return MathTex(name, font_size=fs, color=col).move_to(V + d * dist)


def deg_number(val, pos, col=COL_ANG, fs=36):
    n = DecimalNumber(val, num_decimal_places=0, unit=r"^\circ", font_size=fs, color=col)
    return n.move_to(pos)


def caption(text):
    t = Text(wrap(text), font=FONT, font_size=24, color="#ECECEC", line_spacing=0.75)
    if t.width > 13.3:
        t.scale_to_fit_width(13.3)
    t.to_edge(DOWN, buff=0.22)
    bg = BackgroundRectangle(t, color=BG, fill_opacity=0.9, buff=0.12)
    return VGroup(bg, t)


def steps_column(lines, x=1.2, y_top=2.4, fs=30, buff=0.28):
    """lines: list of (MathTex string, reason text or '', colour)"""
    rows = []
    for tex, why, col in lines:
        m = MathTex(tex, font_size=fs, color=col)
        if why:
            w = T(why, 20, GRAY_B)
            row = VGroup(m, w).arrange(RIGHT, buff=0.25)
        else:
            row = VGroup(m)
        rows.append(row)
    g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    g.move_to(P(x, 0), aligned_edge=LEFT)
    g.shift(UP * (y_top - g.get_top()[1]))
    return g


class LessonScene(Scene):
    PART = 0
    TITLE = ""

    def setup(self):
        self.camera.background_color = BG
        self.head = None

    def header(self):
        self.head = T(f"Parte {self.PART}  ·  {self.TITLE}", 20, GRAY_B).to_corner(UL, buff=0.3)
        self.play(FadeIn(self.head), run_time=0.4)

    def title_card(self):
        a = T(f"Parte {self.PART}", 26, GRAY_B)
        b = T(self.TITLE, 50, WHITE, weight=BOLD)
        g = VGroup(a, b).arrange(DOWN, buff=0.3)
        self.play(FadeIn(g, shift=UP * 0.2), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(g), run_time=0.5)
        self.header()

    @contextmanager
    def say(self, text, pad=0.35):
        path, dur = synth(text)
        cap = caption(text)
        self.add_foreground_mobjects(cap)
        self.add_sound(path)
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


def door(self_scene, O, L, th, show_number=True):
    """a door seen from above; th is a ValueTracker in degrees"""
    wall1 = Rectangle(width=0.55, height=0.3, fill_color=GRAY_D, fill_opacity=1,
                      stroke_width=0).move_to(O + LEFT * 0.35 + DOWN * 0.05)
    wall2 = wall1.copy().move_to(O + RIGHT * (L + 0.35) + DOWN * 0.05)
    closed = DashedLine(O, O + RIGHT * L, color=COL_GRID, dash_length=0.12)
    leaf = always_redraw(lambda: Line(O, O + L * unit(th.get_value()),
                                      color=COL_DOOR, stroke_width=11))
    wed = always_redraw(lambda: wedge(O, 0, th.get_value(), 1.4, COL_ANG, 0.35))
    arc_ = always_redraw(lambda: arcm(O, 0, th.get_value(), 1.4, COL_ANG, 3))
    hinge = Dot(O, radius=0.1, color=COL_ANG)
    parts = [wall1, wall2, closed, wed, arc_, leaf, hinge]
    if show_number:
        num = always_redraw(lambda: deg_number(th.get_value(),
                                               O + 2.0 * unit(max(th.get_value(), 8) / 2)))
        parts.append(num)
    return VGroup(*parts)


# ══════════════════════════════════════════════════════════════════════
# PARTE 1: la porta
# ══════════════════════════════════════════════════════════════════════
class P01_Porta(LessonScene):
    PART, TITLE = 1, "Quanto è grande un angolo?"

    def construct(self):
        t1 = T("Angoli e triangoli congruenti", 54, WHITE, weight=BOLD)
        t2 = T("Una lezione di geometria", 30, COL_ANG)
        card = VGroup(t1, t2).arrange(DOWN, buff=0.4).move_to(UP * 0.6)
        with self.say("Ciao! Benvenuta. Oggi facciamo un viaggio nella geometria: dagli angoli fino ai triangoli congruenti."):
            self.play(Write(t1), run_time=2.2)
            self.play(FadeIn(t2, shift=UP * 0.2))
        q = T("Quanto è grande un angolo?", 46, COL_ANG)
        with self.say("Partiamo da una domanda che sembra facilissima: quanto è grande un angolo?"):
            self.play(FadeOut(card), run_time=0.6)
            self.play(Write(q), run_time=1.6)
        self.play(FadeOut(q), run_time=0.5)
        self.header()

        O, L = P(-2.4, -1.7), 4.2
        th = ValueTracker(0)
        d = door(self, O, L, th)
        lab_h = T("cardine", 24, COL_ANG).next_to(O, DOWN, buff=0.3)
        lab_d = T("porta", 24, COL_DOOR)
        with self.say("Guarda questa porta, vista dall'alto. Il punto giallo è il cardine, quello intorno a cui gira."):
            self.play(FadeIn(d), run_time=1.0)
            self.play(FadeIn(lab_h))
        with self.say("Adesso la apro un po', e poi di più."):
            self.play(th.animate.set_value(30), run_time=1.6)
            self.wait(0.4)
            self.play(th.animate.set_value(110), run_time=2.2)
        with self.say("Qualcosa è cresciuto. Ma non la porta: la porta è lunga esattamente come prima."):
            lab_d.move_to(O + 2.6 * unit(110) + LEFT * 0.55)
            self.play(FadeIn(lab_d))
            self.play(Indicate(d[5], color=COL_DOOR, scale_factor=1.05), run_time=1.4)
        with self.say("È cresciuta la rotazione intorno al cardine. Quella rotazione è l'angolo."):
            self.play(Indicate(d[3], color=COL_ANG), run_time=1.5)
        self.wipe()

        # the trap: long sides
        O1, O2 = P(-5.0, -1.8), P(0.3, -1.8)
        Ls = ValueTracker(1.6)
        a_short = VGroup(seg(O1, O1 + RIGHT * 1.6), seg(O1, O1 + 1.6 * unit(40)),
                         wedge(O1, 0, 40, 0.8, COL_ANG, 0.4), arcm(O1, 0, 40, 0.8),
                         deg_number(40, O1 + 1.25 * unit(20)))
        a_long = always_redraw(lambda: VGroup(
            seg(O2, O2 + RIGHT * Ls.get_value()), seg(O2, O2 + Ls.get_value() * unit(40)),
            wedge(O2, 0, 40, 0.8, COL_ANG, 0.4), arcm(O2, 0, 40, 0.8),
            deg_number(40, O2 + 1.25 * unit(20))))
        trap = T("Trappola!", 34, COL_ERR).to_edge(UP, buff=0.9)
        with self.say("Ecco una trappola in cui cadono in molti. Guarda questi due angoli."):
            self.play(FadeIn(trap))
            self.play(Create(a_short), Create(a_long), run_time=1.5)
        with self.say("Se allungo i lati di uno dei due, l'angolo diventa più grande? Guarda il numero."):
            self.play(Ls.animate.set_value(5.3), run_time=3.0, rate_func=smooth)
        ok = T("Stesso angolo!", 36, COL_RES).next_to(trap, DOWN, buff=0.3)
        with self.say("Non cambia niente! I lati sono semirette, cioè sono infinitamente lunghi: il disegno ne mostra solo un pezzo."):
            self.play(Write(ok), run_time=1.0)
            self.play(Indicate(ok, color=COL_RES))
        self.wipe()
        q2 = T("Che cosa misura, davvero, un angolo?", 40, COL_ANG)
        q3 = T("E perché un giro completo vale 360 gradi?", 34, WHITE).next_to(q2, DOWN, buff=0.4)
        with self.say("Allora, che cosa misura davvero un angolo? E perché diciamo che un giro completo vale trecentosessanta gradi? Scopriamolo."):
            self.play(Write(q2), run_time=1.6)
            self.play(FadeIn(q3, shift=UP * 0.2))
        self.end()


# ══════════════════════════════════════════════════════════════════════
# PARTE 2: l'angolo sulla circonferenza
# ══════════════════════════════════════════════════════════════════════
class P02_Circonferenza(LessonScene):
    PART, TITLE = 2, "L'angolo sulla circonferenza"

    def construct(self):
        self.title_card()
        O = P(-3.0, -1.5)
        r1 = Arrow(O, O + RIGHT * 4.0, buff=0, color=WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.06)
        r2 = Arrow(O, O + 4.0 * unit(60), buff=0, color=WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.06)
        vdot = Dot(O, color=COL_ANG, radius=0.09)
        lv = T("vertice", 24, COL_ANG).next_to(O, DOWN + LEFT, buff=0.15)
        ll = T("lati", 24, WHITE).move_to(O + 2.6 * unit(30) + P(0.6, 0.1))
        with self.say("In geometria teniamo solo l'essenziale. Il cardine diventa un punto: il vertice."):
            self.play(FadeIn(vdot, scale=1.5), FadeIn(lv))
        with self.say("Il muro e la porta diventano due semirette che partono dal vertice: sono i lati dell'angolo."):
            self.play(GrowArrow(r1), GrowArrow(r2), run_time=1.4)
            self.play(FadeIn(ll))
        with self.say("Per misurare una rotazione, mettiamo il vertice al centro di una circonferenza."):
            c1 = Circle(radius=1.0, color=COL_GRID, stroke_width=2).move_to(O)
            self.play(FadeOut(lv), FadeOut(ll), Create(c1), run_time=1.2)
        a1 = arcm(O, 0, 60, 1.0, COL_ANG, 6)
        with self.say("I due lati tagliano un arco. L'angolo è la frazione di circonferenza coperta dall'arco."):
            self.play(Create(a1), run_time=1.2)
        c2 = Circle(radius=2.0, color=COL_GRID, stroke_width=2).move_to(O)
        c3 = Circle(radius=3.0, color=COL_GRID, stroke_width=2).move_to(O)
        a2 = arcm(O, 0, 60, 2.0, COL_ANG2, 6)
        a3 = arcm(O, 0, 60, 3.0, COL_ANG3, 6)
        with self.say("Guarda: disegno altre due circonferenze con lo stesso centro."):
            self.play(Create(c2), Create(c3), run_time=1.4)
            self.play(Create(a2), Create(a3), run_time=1.2)
        fr = VGroup(*[M(r"\tfrac{1}{6}", 34, col).move_to(O + (rr + 0.35) * unit(30))
                      for rr, col in [(1.0, COL_ANG), (2.0, COL_ANG2), (3.0, COL_ANG3)]])
        with self.say("Gli archi colorati hanno lunghezze diverse, ma ognuno è esattamente un sesto della sua circonferenza."):
            self.play(LaggedStart(*[FadeIn(f, scale=0.8) for f in fr], lag_ratio=0.4), run_time=1.8)
        note = VGroup(T("La frazione non dipende", 28, WHITE), T("dal raggio.", 28, WHITE)).arrange(DOWN, aligned_edge=LEFT).move_to(P(3.8, 1.8))
        with self.say("La frazione non dipende dal raggio. È come la punta di una fetta di pizza: non cambia se la pizza è più grande."):
            self.play(FadeIn(note, shift=LEFT * 0.2))
        self.wipe()

        # 360 degrees
        C = P(-2.6, -0.2)
        R = 2.55
        circ = Circle(radius=R, color=COL_GRID, stroke_width=2).move_to(C)
        tks = VGroup(*[Line(C + R * unit(a), C + (R - (0.22 if a % 10 == 0 else 0.1)) * unit(a),
                            color=GRAY_B, stroke_width=1.4 if a % 10 == 0 else 0.8)
                       for a in range(0, 360)])
        with self.say("Ora dividiamo il giro completo in trecentosessanta parti uguali. Ognuna si chiama grado."):
            self.play(Create(circ), run_time=0.8)
            self.play(Create(tks), run_time=2.4)
        one = VGroup(wedge(C, 0, 1, R, COL_ANG, 0.9))
        lab1 = M(r"1^\circ", 36, COL_ANG).move_to(C + (R + 0.45) * unit(1))
        with self.say("Un grado è una fettina sottilissima: un trecentosessantesimo di giro."):
            self.play(FadeIn(one), Write(lab1))
            self.play(Indicate(lab1, color=COL_ANG))
        self.play(FadeOut(one), FadeOut(lab1), run_time=0.4)
        th = ValueTracker(0.01)
        ray = always_redraw(lambda: Line(C, C + R * unit(th.get_value()), color=COL_ANG, stroke_width=4))
        wed = always_redraw(lambda: wedge(C, 0, th.get_value(), R * 0.8, COL_ANG, 0.3))
        num = always_redraw(lambda: deg_number(th.get_value(), P(3.2, 1.2), COL_ANG, 60))
        base = Line(C, C + RIGHT * R, color=WHITE, stroke_width=3)
        self.play(Create(base), FadeIn(ray), FadeIn(wed), FadeIn(num))
        with self.say("Quindi un quarto di giro vale novanta gradi,"):
            self.play(th.animate.set_value(90), run_time=1.8)
        with self.say("mezzo giro centottanta,"):
            self.play(th.animate.set_value(180), run_time=1.5)
        with self.say("e il giro completo trecentosessanta."):
            self.play(th.animate.set_value(360), run_time=2.0)
        self.wait(0.4)
        self.play(th.animate.set_value(60), run_time=1.5)
        eq = M(r"\tfrac{1}{6}\cdot 360^\circ = 60^\circ", 50, COL_ANG).move_to(P(3.3, -0.5))
        with self.say("E il nostro angolo di prima? È un sesto di giro: trecentosessanta diviso sei fa sessanta gradi."):
            self.play(Write(eq), run_time=1.6)
            self.play(Circumscribe(eq, color=COL_ANG))
        self.end()


# ══════════════════════════════════════════════════════════════════════
# PARTE 3: perché 360
# ══════════════════════════════════════════════════════════════════════
class P03_Perche360(LessonScene):
    PART, TITLE = 3, "Perché proprio 360?"

    def construct(self):
        self.title_card()
        q = T("360: una legge della natura?", 40, WHITE).move_to(UP * 0.8)
        with self.say("Perché proprio trecentosessanta, e non cento, che sembrerebbe più comodo?"):
            self.play(Write(q), run_time=1.5)
        cross = Cross(q, stroke_color=COL_ERR, stroke_width=6)
        no = T("No: è una scelta delle persone", 32, COL_ERR).next_to(q, DOWN, buff=0.5)
        with self.say("Attenzione: trecentosessanta non è una legge della natura. La natura ci dà il giro completo; il numero l'hanno scelto le persone."):
            self.play(Create(cross), run_time=0.8)
            self.play(FadeIn(no, shift=UP * 0.2))
        self.wipe()

        m1 = T("Motivo 1: 360 si divide bene", 30, COL_RES).move_to(P(0, 3.15))
        ns = [2, 3, 4, 5, 6, 8, 9, 10, 12]
        pizzas = VGroup()
        for i, n in enumerate(ns):
            cx, cy = -5.0 + 4.2 * (i % 3), 1.9 - 1.75 * (i // 3)
            c = P(cx, cy)
            d = 360 // n
            pz = VGroup(Circle(radius=0.58, color=COL_ANG2, stroke_width=2).move_to(c).set_fill(COL_ANG2, 0.15),
                        wedge(c, 90, d, 0.58, COL_ANG2, 0.75),
                        *[Line(c, c + 0.58 * unit(90 + k * d), color=COL_ANG2, stroke_width=2) for k in range(n)])
            lb = M(rf"360 : {n} = {d}", 30, WHITE).next_to(pz, RIGHT, buff=0.25)
            pizzas.add(VGroup(pz, lb))
        with self.say("Primo motivo: trecentosessanta si divide bene. Lo taglio in due, tre, quattro, cinque, sei, otto, nove, dieci e dodici fette."):
            self.play(FadeIn(m1))
            self.play(LaggedStart(*[FadeIn(p[0], scale=0.7) for p in pizzas], lag_ratio=0.15), run_time=3.0)
        with self.say("Ogni fetta è un numero intero di gradi: centottanta, centoventi, novanta, settantadue, sessanta, quarantacinque, quaranta, trentasei, trenta."):
            self.play(LaggedStart(*[Write(p[1]) for p in pizzas], lag_ratio=0.2), run_time=4.0)
        self.wipe()
        good = VGroup(M(r"360 : 3 = 120", 44, COL_RES), M(r"360 : 6 = 60", 44, COL_RES)).arrange(DOWN, buff=0.4).move_to(P(-3.2, 0.8))
        bad = VGroup(M(r"100 : 3 = 33{,}\overline{3}", 44, COL_ERR), M(r"100 : 6 = 16{,}\overline{6}", 44, COL_ERR)).arrange(DOWN, buff=0.4).move_to(P(3.2, 0.8))
        with self.say("Con cento invece? Un terzo è trentatré virgola tre periodico, un sesto è sedici virgola sei periodico: numeri che non finiscono mai."):
            self.play(Write(good), run_time=1.5)
            self.play(Write(bad), run_time=1.8)
        divs = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 60, 72, 90, 120, 180, 360]
        dv = VGroup(*[M(str(k), 30, COL_ANG) for k in divs]).arrange_in_grid(rows=2, buff=(0.32, 0.25)).move_to(P(0, -1.6))
        cnt = T("24 divisori", 30, COL_ANG).next_to(dv, UP, buff=0.3)
        with self.say("In tutto trecentosessanta ha ventiquattro divisori. È il numero più piccolo che ne ha così tanti."):
            self.play(LaggedStart(*[FadeIn(x, scale=0.6) for x in dv], lag_ratio=0.05), run_time=2.2)
            self.play(Write(cnt))
        self.wipe()

        m2 = T("Motivo 2: i Babilonesi contavano a 60", 30, COL_RES).move_to(P(0, 3.15))
        C = P(-3.3, -0.2)
        R = 2.1
        clk = VGroup(Circle(radius=R, color=WHITE, stroke_width=3).move_to(C),
                     *[Line(C + R * unit(90 - 6 * k), C + (R - (0.25 if k % 5 == 0 else 0.12)) * unit(90 - 6 * k),
                            color=WHITE, stroke_width=2.5 if k % 5 == 0 else 1.2) for k in range(60)])
        hand = Line(C, C + 1.8 * unit(90), color=COL_ANG, stroke_width=4)
        with self.say("Secondo motivo: circa quattromila anni fa i Babilonesi facevano i calcoli in base sessanta."):
            self.play(FadeIn(m2))
            self.play(Create(clk), run_time=1.6)
        eqs = VGroup(M(r"1\ \text{ora} = 60\ \text{minuti}", 38),
                     M(r"1^\circ = 60' \qquad 1' = 60''", 42, COL_ANG),
                     M(r"6 \times 60 = 360", 48, COL_RES)).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(P(3.0, 0.2))
        with self.say("Lo usiamo ancora oggi: un'ora ha sessanta minuti e un minuto sessanta secondi."):
            self.play(FadeIn(hand), run_time=0.4)
            self.play(Rotate(hand, angle=-TAU, about_point=C), run_time=2.2)
            self.play(Write(eqs[0]))
        with self.say("Anche un grado si divide in sessanta primi, e un primo in sessanta secondi."):
            self.play(Write(eqs[1]), run_time=1.4)
        with self.say("E il giro completo? Sei volte sessanta: trecentosessanta."):
            self.play(Write(eqs[2]), run_time=1.2)
            self.play(Circumscribe(eqs[2], color=COL_RES))
        self.wipe()

        m3 = T("Motivo 3 (probabile): l'anno", 30, COL_RES).move_to(P(0, 3.15))
        Cs = P(-2.8, -0.2)
        orbit = Circle(radius=2.1, color=COL_GRID, stroke_width=2).move_to(Cs)
        earth = Dot(Cs, radius=0.16, color=COL_GIV)
        sun = Dot(Cs + 2.1 * unit(0), radius=0.2, color=COL_ANG)
        note = VGroup(T("un anno: circa 365 giorni", 28), T("il Sole: circa 1 grado al giorno", 28, COL_ANG),
                      T("un'ipotesi, non un fatto provato", 24, GRAY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P(3.2, 0))
        with self.say("Terzo motivo, probabile ma non dimostrato: l'anno ha circa trecentosessantacinque giorni, e il Sole sembra spostarsi nel cielo di circa un grado al giorno."):
            self.play(FadeIn(m3), Create(orbit), FadeIn(earth), FadeIn(sun))
            self.play(Rotate(sun, angle=TAU, about_point=Cs), run_time=3.0)
            self.play(LaggedStart(*[FadeIn(x, shift=LEFT * 0.2) for x in note], lag_ratio=0.4), run_time=1.8)
        self.wipe()

        # pie chart
        hd = T("Un areogramma", 32, COL_ANG).move_to(P(0, 3.15))
        data = [("pizza", 12, "#EF8A6A"), ("pasta", 9, "#7EB6FF"), ("gelato", 6, "#06D6A0"), ("altro", 3, COL_ANG)]
        with self.say("Adesso usiamo i gradi per qualcosa di concreto: un areogramma, come quelli del tuo quaderno."):
            self.play(FadeIn(hd))
        tab = VGroup(*[T(f"{n}: {v} studenti", 26, c) for n, v, c in data]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(P(-4.6, 2.0))
        with self.say("In una classe di trenta studenti, dodici preferiscono la pizza, nove la pasta, sei il gelato e tre altro."):
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in tab], lag_ratio=0.3), run_time=2.0)
        prop = M(r"x : 360^\circ = \text{parte} : \text{totale}", 38).move_to(P(2.7, 2.3))
        with self.say("Tutta la classe è tutto il cerchio. Impostiamo la proporzione: x sta a trecentosessanta come la parte sta al totale."):
            self.play(Write(prop), run_time=1.8)
        Cp = P(-2.6, -0.9)
        Rp = 1.55
        start = 90.0
        calcs = VGroup()
        slices = VGroup()
        for n, v, c in data:
            ang = v * 360 / 30
            slices.add(wedge(Cp, start - ang, ang, Rp, c, 0.85))
            calcs.add(M(rf"\frac{{{v}\cdot 360^\circ}}{{30}} = {int(ang)}^\circ", 34, c))
            start -= ang
        calcs.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(P(2.6, -0.3))
        with self.say("Pizza: dodici per trecentosessanta, diviso trenta, fa centoquarantaquattro gradi."):
            self.play(Write(calcs[0]), FadeIn(slices[0], scale=0.9), run_time=1.6)
        with self.say("Pasta: centootto gradi. Gelato: settantadue. Altro: trentasei."):
            for k in (1, 2, 3):
                self.play(Write(calcs[k]), FadeIn(slices[k], scale=0.9), run_time=1.0)
        chk = M(r"144 + 108 + 72 + 36 = 360", 38, COL_RES).move_to(P(2.6, -2.3))
        with self.say("Controlliamo: centoquarantaquattro più centootto più settantadue più trentasei fa trecentosessanta. Il cerchio si chiude esattamente."):
            self.play(FadeOut(tab), run_time=0.3)
            self.play(Write(chk), run_time=1.6)
            self.play(Flash(Cp, color=COL_RES, flash_radius=Rp + 0.2))
        self.end()


# ══════════════════════════════════════════════════════════════════════
# PARTE 4: i tipi di angoli
# ══════════════════════════════════════════════════════════════════════
def angle_name(v):
    if v < 0.5:
        return "angolo nullo"
    if v < 89.5:
        return "angolo acuto"
    if v < 90.5:
        return "angolo retto"
    if v < 179.5:
        return "angolo ottuso"
    if v < 180.5:
        return "angolo piatto"
    if v < 359.5:
        return "angolo concavo"
    return "angolo giro"


class P04_Tipi(LessonScene):
    PART, TITLE = 4, "I tipi di angoli"

    def construct(self):
        self.title_card()
        O = P(-2.6, -0.4)
        L = 2.6
        th = ValueTracker(0)
        base = Line(O, O + RIGHT * L, color=WHITE, stroke_width=4)
        ray = always_redraw(lambda: Line(O, O + L * unit(th.get_value()), color=WHITE, stroke_width=4))
        wed = always_redraw(lambda: wedge(O, 0, th.get_value(), 1.1, COL_ANG, 0.35))
        sq = always_redraw(lambda: rmark(O, O + RIGHT, O + UP, 0.3, COL_ANG) if abs(th.get_value() - 90) < 0.5 else VMobject())
        num = always_redraw(lambda: deg_number(th.get_value(), P(3.4, 1.3), COL_ANG, 64))
        names = {}

        def name_text():
            key = angle_name(th.get_value())
            if key not in names:
                names[key] = T(key, 40, WHITE).move_to(P(3.4, 0.1))
            return names[key].copy()
        name = always_redraw(name_text)
        dot = Dot(O, color=COL_ANG)
        with self.say("Ora che sappiamo misurare, possiamo dare dei nomi. Faccio girare un lato, e guardiamo il numero."):
            self.play(Create(base), FadeIn(ray), FadeIn(dot), FadeIn(num), FadeIn(name))
        with self.say("A zero gradi i due lati coincidono: è l'angolo nullo."):
            self.play(Indicate(name))
        with self.say("Finché restiamo sotto i novanta gradi, l'angolo è acuto."):
            self.add(wed)
            self.play(th.animate.set_value(45), run_time=2.0)
        with self.say("Esattamente novanta gradi: l'angolo retto, come l'angolo di un libro o di un foglio. Si segna con un quadratino."):
            self.play(th.animate.set_value(90), run_time=1.5)
            self.add(sq)
        with self.say("Tra novanta e centottanta gradi, l'angolo è ottuso."):
            self.play(th.animate.set_value(130), run_time=1.8)
        with self.say("A centottanta gradi i lati formano una retta: è l'angolo piatto."):
            self.play(th.animate.set_value(180), run_time=1.6)
        with self.say("Oltre centottanta, l'angolo si chiama concavo."):
            self.play(th.animate.set_value(250), run_time=1.8)
        with self.say("E a trecentosessanta gradi abbiamo fatto tutto il giro: l'angolo giro."):
            self.play(th.animate.set_value(360), run_time=2.0)
        self.wipe()

        # the clock
        C = P(-3.2, -0.25)
        R = 2.35

        def cpt(a, r):  # clock angle a measured clockwise from 12
            return C + r * np.array([np.sin(np.radians(a)), np.cos(np.radians(a)), 0.0])

        face = VGroup(Circle(radius=R, color=WHITE, stroke_width=3).move_to(C),
                      *[Line(cpt(30 * k, R), cpt(30 * k, R - 0.25), color=WHITE, stroke_width=3) for k in range(12)],
                      *[T(str(k if k else 12), 24, GRAY_B).move_to(cpt(30 * k, R - 0.55)) for k in range(12)])
        hh = ValueTracker(90)
        mm = ValueTracker(0)
        hour = always_redraw(lambda: Line(C, cpt(hh.get_value(), 1.25), color=WHITE, stroke_width=8))
        minute = always_redraw(lambda: Line(C, cpt(mm.get_value(), 1.9), color=WHITE, stroke_width=4))

        def clock_wedge():
            a, b = hh.get_value(), mm.get_value()
            lo, hi = sorted([a, b])
            if hi - lo > 180:
                lo, hi = hi, lo + 360
            return wedge(C, 90 - hi, hi - lo, 0.95, COL_ANG, 0.45)
        cw = always_redraw(clock_wedge)
        with self.say("Un orologio è un goniometro che si muove. Tra un numero e il successivo ci sono trecentosessanta diviso dodici, cioè trenta gradi."):
            self.play(Create(face), run_time=1.6)
            self.play(FadeIn(hour), FadeIn(minute), FadeIn(Dot(C)))
        r1 = M(r"360^\circ : 12 = 30^\circ", 40).move_to(P(3.0, 2.2))
        self.play(Write(r1))
        with self.say("Alle tre, le lancette formano un angolo retto: tre spazi da trenta gradi, cioè novanta gradi."):
            self.add(cw)
            self.play(Indicate(cw, color=COL_ANG))
        with self.say("E alle due e mezza? Molti rispondono novanta gradi. Pensaci un attimo."):
            self.play(hh.animate.set_value(60), mm.animate.set_value(180), run_time=2.0)
            self.wait(1.5)
        s1 = M(r"\text{minuti: } 30\cdot 6^\circ = 180^\circ", 36).move_to(P(3.0, 1.1))
        s2 = M(r"\text{ore: } 2\cdot 30^\circ + 30\cdot 0{,}5^\circ = 75^\circ", 36).move_to(P(3.0, 0.1))
        s3 = M(r"180^\circ - 75^\circ = 105^\circ", 44, COL_RES).move_to(P(3.0, -1.0))
        with self.say("La lancetta dei minuti è sul sei: centottanta gradi dal dodici."):
            self.play(Write(s1))
        with self.say("Ma la lancetta delle ore non è sul due: si muove di mezzo grado al minuto, quindi in mezz'ora è andata avanti di quindici gradi."):
            self.play(hh.animate.set_value(75), run_time=1.6)
            self.play(Write(s2))
        with self.say("Quindi l'angolo è centottanta meno settantacinque: centocinque gradi. Un angolo ottuso!"):
            self.play(Write(s3))
            self.play(Circumscribe(s3, color=COL_RES))
        self.end()


# ══════════════════════════════════════════════════════════════════════
# PARTE 5: coppie di angoli
# ══════════════════════════════════════════════════════════════════════
class P05_Coppie(LessonScene):
    PART, TITLE = 5, "Coppie di angoli"

    def construct(self):
        self.title_card()
        # complementary
        O = P(-4.2, -1.8)
        a = ValueTracker(35)
        fixed = VGroup(Line(O, O + RIGHT * 2.8, color=WHITE, stroke_width=4),
                       Line(O, O + UP * 2.8, color=WHITE, stroke_width=4),
                       rmark(O, O + RIGHT, O + UP, 0.28))
        mid = always_redraw(lambda: Line(O, O + 2.8 * unit(a.get_value()), color=WHITE, stroke_width=4))
        wa = always_redraw(lambda: wedge(O, 0, a.get_value(), 1.4, COL_ANG, 0.45))
        wb = always_redraw(lambda: wedge(O, a.get_value(), 90 - a.get_value(), 1.4, COL_ANG2, 0.45))
        na = always_redraw(lambda: deg_number(a.get_value(), O + 1.9 * unit(a.get_value() / 2), COL_ANG, 32))
        nb = always_redraw(lambda: deg_number(90 - a.get_value(), O + 1.9 * unit(45 + a.get_value() / 2), COL_ANG2, 32))
        tot = always_redraw(lambda: VGroup(
            DecimalNumber(a.get_value(), num_decimal_places=0, unit=r"^\circ", font_size=44, color=COL_ANG),
            M(r"+", 44),
            DecimalNumber(90 - a.get_value(), num_decimal_places=0, unit=r"^\circ", font_size=44, color=COL_ANG2),
            M(r"= 90^\circ", 44, COL_RES)).arrange(RIGHT, buff=0.15).move_to(P(2.8, 0.6)))
        t1 = T("complementari", 36, WHITE).move_to(P(2.8, 1.8))
        with self.say("Gli angoli diventano interessanti quando stanno in coppia. Due angoli sono complementari se insieme formano un angolo retto."):
            self.play(Create(fixed), Create(mid), FadeIn(wa), FadeIn(wb), FadeIn(na), FadeIn(nb))
            self.play(FadeIn(t1), FadeIn(tot))
        with self.say("Se uno cresce, l'altro cala, ma la somma resta sempre novanta gradi."):
            self.play(a.animate.set_value(70), run_time=2.0)
            self.play(a.animate.set_value(20), run_time=2.0)
            self.play(a.animate.set_value(35), run_time=1.2)
        self.wipe()

        # supplementary
        O2 = P(-2.4, -1.4)
        b = ValueTracker(128)
        line = Line(O2 + LEFT * 3, O2 + RIGHT * 3, color=WHITE, stroke_width=4)
        rr = always_redraw(lambda: Line(O2, O2 + 2.6 * unit(b.get_value()), color=WHITE, stroke_width=4))
        w1 = always_redraw(lambda: wedge(O2, 0, b.get_value(), 1.2, COL_ANG, 0.45))
        w2 = always_redraw(lambda: wedge(O2, b.get_value(), 180 - b.get_value(), 1.2, COL_ANG2, 0.45))
        n1 = always_redraw(lambda: deg_number(b.get_value(), O2 + 1.65 * unit(b.get_value() / 2), COL_ANG, 32))
        n2 = always_redraw(lambda: deg_number(180 - b.get_value(), O2 + 1.65 * unit(90 + b.get_value() / 2), COL_ANG2, 32))
        t2 = VGroup(T("supplementari", 34), M(r"\alpha + \beta = 180^\circ", 42, COL_RES)).arrange(DOWN, buff=0.3).move_to(P(3.6, 1.2))
        with self.say("Sono supplementari se insieme formano un angolo piatto: la somma è centottanta gradi."):
            self.play(Create(line), Create(rr), FadeIn(w1), FadeIn(w2), FadeIn(n1), FadeIn(n2))
            self.play(FadeIn(t2))
            self.play(b.animate.set_value(60), run_time=1.8)
            self.play(b.animate.set_value(128), run_time=1.4)
        self.wipe()

        O3 = P(-2.4, -0.3)
        w3 = wedge(O3, 0, 110, 1.3, COL_ANG, 0.45)
        w4 = wedge(O3, 110, 250, 1.3, COL_ANG2, 0.45)
        ex = VGroup(w3, w4, Line(O3, O3 + 2.3 * RIGHT, color=WHITE, stroke_width=4),
                    Line(O3, O3 + 2.3 * unit(110), color=WHITE, stroke_width=4),
                    M(r"110^\circ", 32, COL_ANG).move_to(O3 + 1.75 * unit(55)),
                    M(r"250^\circ", 32, COL_ANG2).move_to(O3 + 1.75 * unit(235)))
        t3 = VGroup(T("esplementari", 34), M(r"\alpha + \beta = 360^\circ", 42, COL_RES)).arrange(DOWN, buff=0.3).move_to(P(3.6, 1.2))
        with self.say("E sono esplementari se insieme fanno un giro completo: la somma è trecentosessanta gradi."):
            self.play(FadeIn(ex), FadeIn(t3), run_time=1.4)
        self.wipe()

        e1 = M(r"90^\circ - 35^\circ = 55^\circ", 48).move_to(P(0, 2.2))
        with self.say("Esempio: qual è il complementare di trentacinque gradi? Novanta meno trentacinque: cinquantacinque gradi."):
            self.play(Write(e1), run_time=1.5)
        p1 = T("Due angoli complementari: uno è il doppio dell'altro.", 30).move_to(P(0, 1.1))
        eqA = MathTex(r"x", r"+", r"2x", r"=", r"90^\circ", font_size=52).move_to(P(0, -0.1))
        eqB = MathTex(r"3x", r"=", r"90^\circ", font_size=52).move_to(P(0, -0.1))
        eqC = MathTex(r"x", r"=", r"30^\circ", font_size=52).move_to(P(0, -0.1))
        res = M(r"30^\circ \ \text{e}\ 60^\circ", 50, COL_RES).move_to(P(0, -1.4))
        with self.say("Un indovinello: due angoli complementari, e uno è il doppio dell'altro. Chiamo x il più piccolo."):
            self.play(FadeIn(p1))
        with self.say("Allora x più due x fa novanta, cioè tre x uguale novanta, e x vale trenta. Gli angoli sono trenta e sessanta gradi."):
            self.play(Write(eqA))
            self.wait(0.6)
            self.play(TransformMatchingTex(eqA, eqB))
            self.wait(0.6)
            self.play(TransformMatchingTex(eqB, eqC))
            self.play(Write(res))
        self.wipe()
        p2 = T("Due angoli supplementari differiscono di 40°.", 30).move_to(P(0, 2.0))
        eqD = MathTex(r"x", r"+", r"(x + 40^\circ)", r"=", r"180^\circ", font_size=50).move_to(P(0, 0.7))
        eqE = MathTex(r"2x", r"=", r"140^\circ", font_size=50).move_to(P(0, 0.7))
        eqF = MathTex(r"x", r"=", r"70^\circ", font_size=50).move_to(P(0, 0.7))
        res2 = M(r"70^\circ \ \text{e}\ 110^\circ", 50, COL_RES).move_to(P(0, -0.6))
        with self.say("Un altro indovinello: due angoli supplementari differiscono di 40°. Chiamo x il più piccolo: l'altro è x più 40."):
            self.play(FadeIn(p2))
            self.play(Write(eqD))
        with self.say("La somma è 180, quindi 2x fa 140, e x vale 70. Gli angoli sono 70 e 110 gradi."):
            self.play(TransformMatchingTex(eqD, eqE))
            self.wait(0.5)
            self.play(TransformMatchingTex(eqE, eqF))
            self.play(Write(res2))
        self.wipe()

        # vertical angles
        O4 = P(-2.8, -0.6)
        ph = ValueTracker(40)
        l1 = Line(O4 + LEFT * 3, O4 + RIGHT * 3, color=WHITE, stroke_width=4)
        l2 = always_redraw(lambda: Line(O4 - 3 * unit(ph.get_value()), O4 + 3 * unit(ph.get_value()), color=WHITE, stroke_width=4))
        g1 = always_redraw(lambda: wedge(O4, 0, ph.get_value(), 0.9, COL_ANG, 0.5))
        g3 = always_redraw(lambda: wedge(O4, 180, ph.get_value(), 0.9, COL_ANG, 0.5))
        g2 = always_redraw(lambda: wedge(O4, ph.get_value(), 180 - ph.get_value(), 0.6, COL_GIV, 0.35))
        labs = always_redraw(lambda: VGroup(
            M(r"1", 34, COL_ANG).move_to(O4 + 1.25 * unit(ph.get_value() / 2)),
            M(r"2", 34, COL_GIV).move_to(O4 + 1.0 * unit(90 + ph.get_value() / 2)),
            M(r"3", 34, COL_ANG).move_to(O4 + 1.25 * unit(180 + ph.get_value() / 2)),
            M(r"4", 34, COL_GIV).move_to(O4 + 1.0 * unit(270 + ph.get_value() / 2))))
        nums = always_redraw(lambda: VGroup(
            M(r"\widehat{1} =", 40, COL_ANG), DecimalNumber(ph.get_value(), num_decimal_places=0, unit=r"^\circ", font_size=40, color=COL_ANG),
            M(r"\quad \widehat{3} =", 40, COL_ANG), DecimalNumber(ph.get_value(), num_decimal_places=0, unit=r"^\circ", font_size=40, color=COL_ANG)
        ).arrange(RIGHT, buff=0.15).move_to(P(3.2, 2.3)))
        with self.say("Ora due rette che si incrociano, come le lame di un paio di forbici. Si formano quattro angoli."):
            self.play(Create(l1), Create(l2), FadeIn(g1), FadeIn(g2), FadeIn(g3), FadeIn(labs), run_time=1.6)
        with self.say("L'angolo uno e l'angolo tre si chiamano opposti al vertice. Se apro le forbici cambiano tutti, ma l'uno e il tre restano sempre uguali. Perché?"):
            self.play(FadeIn(nums))
            self.play(ph.animate.set_value(70), run_time=2.0)
            self.play(ph.animate.set_value(40), run_time=1.8)
        pr = VGroup(M(r"\widehat{1} + \widehat{2} = 180^\circ", 40), M(r"\widehat{2} + \widehat{3} = 180^\circ", 40),
                    M(r"\widehat{1} = 180^\circ - \widehat{2} = \widehat{3}", 44, COL_RES)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(P(3.3, 0.0))
        with self.say("Ragioniamo. L'uno più il due fa centottanta, perché stanno su una retta."):
            self.play(FadeOut(nums), Write(pr[0]))
        with self.say("Anche il due più il tre fa centottanta, per lo stesso motivo."):
            self.play(Write(pr[1]))
        with self.say("Quindi l'uno e il tre sono entrambi centottanta meno il due: sono uguali! Questa è la tua prima dimostrazione, e vale per ogni X che sia mai stata disegnata."):
            self.play(Write(pr[2]), run_time=1.5)
            self.play(Circumscribe(pr[2], color=COL_RES))
        self.end()


# ══════════════════════════════════════════════════════════════════════
# PARTE 6: parallele e trasversale
# ══════════════════════════════════════════════════════════════════════
BIS = [32.5, 122.5, 212.5, 302.5]   # label directions for the 4 angles at a crossing (t at 65 deg)
SECT = [(0, 65), (65, 115), (180, 65), (245, 115)]   # (start, sweep) of angles 1..4


class P06_Parallele(LessonScene):
    PART, TITLE = 6, "Rette parallele e trasversale"

    def lines(self):
        r = Line(P(-6, 1.3), P(6, 1.3), color=WHITE, stroke_width=4)
        s = Line(P(-6, -1.2), P(6, -1.2), color=WHITE, stroke_width=4)
        t = Line(Q6 - 1.6 * unit(65), P6 + 1.6 * unit(65), color=COL_AUX, stroke_width=4)
        lr = M("r", 36).next_to(r, RIGHT, buff=0.1).shift(LEFT * 0.4 + UP * 0.25)
        ls = M("s", 36).next_to(s, RIGHT, buff=0.1).shift(LEFT * 0.4 + UP * 0.25)
        lt = M("t", 36, COL_AUX).move_to(P6 + 1.75 * unit(65) + RIGHT * 0.25)
        return VGroup(r, s, t, lr, ls, lt)

    def numbers(self, C, first):
        return VGroup(*[M(str(first + k), 32, COL_ANG if k % 2 == 0 else COL_GIV).move_to(C + 0.55 * unit(BIS[k])) for k in range(4)])

    def construct(self):
        self.title_card()
        g = self.lines()
        with self.say("Pensa a due binari del treno, perfettamente paralleli, e a una strada dritta che li attraversa."):
            self.play(Create(g[0]), Create(g[1]), run_time=1.4)
            self.play(Create(g[2]), run_time=1.0)
        with self.say("In geometria i binari sono due rette parallele, erre ed esse, e la strada è una retta trasversale, ti."):
            self.play(FadeIn(g[3:]))
        n1, n2 = self.numbers(P6, 1), self.numbers(Q6, 5)
        with self.say("Si formano due incroci, ciascuno con quattro angoli: otto angoli in tutto."):
            self.play(LaggedStart(*[FadeIn(x, scale=0.7) for x in n1], lag_ratio=0.2), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(x, scale=0.7) for x in n2], lag_ratio=0.2), run_time=1.2)
        # slide
        cross = VGroup(Line(Q6 + LEFT * 1.2, Q6 + RIGHT * 1.2, color=COL_ANG, stroke_width=6),
                       Line(Q6 - 1.0 * unit(65), Q6 + 1.0 * unit(65), color=COL_ANG, stroke_width=6),
                       wedge(Q6, 0, 65, 0.8, COL_ANG, 0.5))
        with self.say("Ecco l'idea chiave: le rette sono parallele, quindi il secondo incrocio è una copia esatta del primo."):
            self.play(FadeIn(cross))
        with self.say("Guarda: faccio scivolare l'incrocio di sotto lungo la strada, e combacia perfettamente con quello di sopra."):
            self.play(cross.animate.shift(P6 - Q6), run_time=2.5)
            self.play(Flash(P6, color=COL_ANG))
        self.play(FadeOut(cross))
        w1 = wedge(P6, 0, 65, 0.85, COL_ANG, 0.5)
        w5 = wedge(Q6, 0, 65, 0.85, COL_ANG, 0.5)
        Fpath = VMobject(color=COL_ANG, stroke_width=7).set_points_as_corners([P(2.6, 1.3), P6, Q6, P(2.6, -1.2)])
        Fstem = Line(Q6, Q6 - 1.0 * unit(65), color=COL_ANG, stroke_width=7)
        lF = T("F: corrispondenti, uguali", 30, COL_ANG).move_to(P(4.7, 2.5))
        with self.say("Per questo gli angoli nella stessa posizione sono uguali: si chiamano corrispondenti, e formano una effe."):
            self.play(FadeIn(w1), FadeIn(w5), Create(Fpath), Create(Fstem), run_time=1.5)
            self.play(FadeIn(lF))
        self.play(FadeOut(Fpath), FadeOut(Fstem), FadeOut(lF), FadeOut(w5))
        w3 = wedge(P6, 180, 65, 0.85, COL_ANG, 0.5)
        with self.say("Ora prendi l'angolo tre: è opposto al vertice dell'angolo uno, quindi è uguale."):
            self.play(FadeIn(w3))
            self.play(Indicate(n1[2], scale_factor=1.5), Indicate(n1[0], scale_factor=1.5))
        Zpath = VMobject(color=COL_RES, stroke_width=7).set_points_as_corners([P(-4.2, 1.3), P6, Q6, P(3.2, -1.2)])
        w5b = wedge(Q6, 0, 65, 0.85, COL_RES, 0.5)
        lZ = T("Z: alterni interni, uguali", 30, COL_RES).move_to(P(4.7, 2.5))
        with self.say("Ma l'angolo uno è uguale al cinque. Quindi il tre e il cinque sono uguali: sono gli alterni interni, e formano una zeta."):
            self.play(FadeOut(w1), w3.animate.set_color(COL_RES), FadeIn(w5b), Create(Zpath), run_time=1.6)
            self.play(FadeIn(lZ))
        self.play(FadeOut(Zpath), FadeOut(lZ), FadeOut(w3))
        w4 = wedge(P6, 245, 115, 0.85, COL_GIV, 0.45)
        Cpath = VMobject(color=COL_GIV, stroke_width=7).set_points_as_corners([P(3.2, 1.3), P6, Q6, P(3.2, -1.2)])
        lC = VGroup(T("C: coniugati", 30, COL_GIV), M(r"\widehat{4} + \widehat{5} = 180^\circ", 38, COL_GIV)).arrange(DOWN, buff=0.2).move_to(P(4.7, 2.55))
        with self.say("E l'angolo quattro con il cinque? Stanno dalla stessa parte: sono coniugati, formano una ci, e la loro somma è centottanta gradi."):
            self.play(FadeIn(w4), w5b.animate.set_color(COL_ANG), Create(Cpath), run_time=1.5)
            self.play(FadeIn(lC))
        self.play(FadeOut(w4), FadeOut(w5b), FadeOut(Cpath), FadeOut(lC))

        # trap: tilt r
        de = ValueTracker(0)
        g[0].add_updater(lambda m: m.put_start_and_end_on(P6 + 6.6 * unit(180 + de.get_value()), P6 + 5.4 * unit(de.get_value())))
        wz3 = always_redraw(lambda: wedge(P6, 180 + de.get_value(), 65 - de.get_value(), 0.85, COL_ERR, 0.45))
        wz5 = wedge(Q6, 0, 65, 0.85, COL_ERR, 0.45)
        vals = always_redraw(lambda: VGroup(
            M(r"\widehat{3} =", 36, COL_ERR), DecimalNumber(65 - de.get_value(), num_decimal_places=0, unit=r"^\circ", font_size=36, color=COL_ERR),
            M(r"\quad \widehat{5} = 65^\circ", 36, COL_ERR)).arrange(RIGHT, buff=0.12).move_to(P(4.6, 2.55)))
        with self.say("Attenzione, trappola: queste regole valgono solo se le rette sono parallele. Se inclino la retta erre, gli angoli della zeta diventano diversi."):
            self.play(FadeOut(n1), FadeIn(wz3), FadeIn(wz5), FadeIn(vals))
            self.play(de.animate.set_value(12), run_time=2.5)
            self.wait(0.8)
            self.play(de.animate.set_value(0), run_time=1.5)
        g[0].clear_updaters()
        self.play(FadeOut(wz3), FadeOut(wz5), FadeOut(vals), FadeIn(n1))
        nb = VGroup(T("Dal quaderno:", 26, GRAY_B), T("alterni esterni: 180 gradi", 30, COL_ERR),
                    T("alterni esterni: UGUALI", 30, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(P(4.7, 2.45))
        w1x = wedge(P6, 0, 65, 0.85, COL_RES, 0.45)
        w7x = wedge(Q6, 180, 65, 0.85, COL_RES, 0.45)
        with self.say("E un'altra trappola, dal tuo quaderno: gli alterni esterni, come l'uno e il sette, non sommano centottanta. Sono uguali, proprio come gli alterni interni."):
            self.play(FadeIn(nb[0]), FadeIn(nb[1]))
            self.play(Create(Cross(nb[1], stroke_color=COL_ERR, stroke_width=4)))
            self.play(FadeIn(nb[2]), FadeIn(w1x), FadeIn(w7x))
        self.wipe()

        # example
        g2 = self.lines()
        self.play(FadeIn(g2), run_time=0.6)
        ex = M(r"r \parallel s,\ \widehat{1} = 65^\circ", 36, COL_ANG).move_to(P(-3.6, 2.6))
        vals1 = [65, 115, 65, 115]
        v1 = VGroup(*[M(rf"{vals1[k]}^\circ", 30, COL_ANG if k % 2 == 0 else COL_GIV).move_to(P6 + 0.72 * unit(BIS[k])) for k in range(4)])
        v2 = VGroup(*[M(rf"{vals1[k]}^\circ", 30, COL_ANG if k % 2 == 0 else COL_GIV).move_to(Q6 + 0.72 * unit(BIS[k])) for k in range(4)])
        with self.say("Esempio: le rette sono parallele e l'angolo uno misura sessantacinque gradi. Troviamo gli altri sette."):
            self.play(FadeIn(ex), FadeIn(v1[0]))
        with self.say("Il due è il suo supplementare: centoquindici. Il tre è opposto al vertice: sessantacinque. Il quattro: centoquindici."):
            for k in (1, 2, 3):
                self.play(FadeIn(v1[k], scale=0.7), run_time=0.8)
        with self.say("Nell'incrocio di sotto tutto si ripete. Con le parallele, un solo angolo decide tutti e otto."):
            self.play(LaggedStart(*[FadeIn(x, scale=0.7) for x in v2], lag_ratio=0.25), run_time=2.0)
        self.play(FadeOut(v1), FadeOut(v2), FadeOut(ex))
        z3 = wedge(P6, 180, 65, 0.85, COL_RES, 0.45)
        z5 = wedge(Q6, 0, 65, 0.85, COL_RES, 0.45)
        e3 = M(r"3x + 10^\circ", 34, COL_RES).move_to(P6 + 1.55 * unit(205))
        e5 = M(r"2x + 40^\circ", 34, COL_RES).move_to(Q6 + 1.6 * unit(22))
        with self.say("Ultimo esempio: due angoli alterni interni misurano 3x più 10 gradi e 2x più 40 gradi. Sono alterni interni, quindi sono uguali."):
            self.play(FadeIn(z3), FadeIn(z5), Write(e3), Write(e5))
        s1 = MathTex(r"3x + 10", r"=", r"2x + 40", font_size=44).move_to(P(3.9, 2.55))
        s2 = MathTex(r"x", r"=", r"30", font_size=44).move_to(P(3.9, 2.55))
        s3 = M(r"3\cdot 30 + 10 = 100^\circ", 42, COL_RES).move_to(P(3.8, -2.2))
        with self.say("Allora 3x più 10 è uguale a 2x più 40: tolgo 2x e 10 da entrambe le parti, e x vale 30."):
            self.play(Write(s1))
            self.wait(0.6)
            self.play(TransformMatchingTex(s1, s2))
        with self.say("Ogni angolo misura 3 per 30 più 10, cioè 100 gradi. E infatti anche 2 per 30 più 40 fa 100."):
            self.play(Write(s3))
            self.play(Circumscribe(s3, color=COL_RES))
        self.end()


# ══════════════════════════════════════════════════════════════════════
# PARTE 7: somma degli angoli = 180
# ══════════════════════════════════════════════════════════════════════
class P07_Somma180(LessonScene):
    PART, TITLE = 7, "La somma degli angoli è 180°"

    def construct(self):
        self.title_card()
        A, B, C = A7, B7, C7
        G = (A + B + C) / 3
        t = tri(A, B, C, WHITE, fill=GRAY_E, op=0.25)
        la, lb, lc = vlabel("A", A, G), vlabel("B", B, G), vlabel("C", C, G)
        wa = wedge(A, 0, 50, 0.85, COL_ANG, 0.8)
        wb = wedge(B, 120, 60, 0.85, COL_ANG2, 0.8)
        wc = wedge(C, 230, 70, 0.85, COL_ANG3, 0.8)
        ga = M(r"\alpha", 36).move_to(A + 1.15 * unit(25))
        gb = M(r"\beta", 36).move_to(B + 1.15 * unit(150))
        gc = M(r"\gamma", 36).move_to(C + 1.15 * unit(265))
        with self.say("Adesso i triangoli. Un triangolo ha tre vertici, tre lati e tre angoli: alfa, beta e gamma."):
            self.play(Create(t), FadeIn(la), FadeIn(lb), FadeIn(lc), run_time=1.4)
            self.play(FadeIn(wa), FadeIn(wb), FadeIn(wc), FadeIn(ga), FadeIn(gb), FadeIn(gc))
        with self.say("Facciamo un esperimento: ritagliamo i tre angoli e li mettiamo uno accanto all'altro."):
            X = P(4.2, -0.6)
            base = Line(X + LEFT * 2.2, X + RIGHT * 2.2, color=WHITE, stroke_width=3)
            self.play(Create(base))
            ca, cb, cc = wa.copy(), wb.copy(), wc.copy()
            self.play(ca.animate.shift(X - A), run_time=1.3)
            self.play(cb.animate.shift(X - B), run_time=1.3)
            self.play(Rotate(cc, angle=PI, about_point=C), run_time=1.0)
            self.play(cc.animate.shift(X - C), run_time=1.3)
        res = M(r"\alpha+\beta+\gamma = 180^\circ", 46, COL_RES).move_to(P(4.0, 1.0))
        with self.say("Formano esattamente un angolo piatto: centottanta gradi!"):
            self.play(Write(res))
            self.play(Flash(X, color=COL_RES))
        with self.say("Ma un esperimento non è una dimostrazione. Vediamo perché succede sempre, con qualunque triangolo."):
            self.play(FadeOut(VGroup(base, ca, cb, cc)), res.animate.set_opacity(0.35))
        par = Line(C + LEFT * 4.2, C + RIGHT * 4.2, color=COL_AUX, stroke_width=4)
        lpar = M(r"r \parallel AB", 34, COL_AUX).next_to(par, RIGHT, buff=0.1).shift(LEFT * 1.2 + UP * 0.3)
        with self.say("Traccio per il vertice ci la retta parallela al lato a bi."):
            self.play(Create(par), FadeIn(lpar), run_time=1.4)
        with self.say("Il lato a ci è una trasversale di queste due parallele: l'angolo alfa in a e questo angolo in ci formano una zeta, quindi sono uguali."):
            ma = wa.copy()
            self.play(Indicate(seg(A, C, COL_AUX, 6)), run_time=1.0)
            self.play(Rotate(ma, angle=PI, about_point=(A + C) / 2), run_time=2.0)
        with self.say("Lo stesso con il lato bi ci: anche beta si ritrova in ci."):
            mb = wb.copy()
            self.play(Rotate(mb, angle=PI, about_point=(B + C) / 2), run_time=2.0)
        with self.say("Ora in ci, lungo la retta, ci sono alfa, gamma e beta uno accanto all'altro: riempiono un angolo piatto."):
            self.play(Indicate(VGroup(ma, wc, mb), scale_factor=1.15), run_time=1.6)
        with self.say("Quindi in ogni triangolo, alfa più beta più gamma fa centottanta gradi."):
            self.play(res.animate.set_opacity(1).scale(1.1))
            self.play(Circumscribe(res, color=COL_RES))
        self.wipe()
        t2 = tri(A, B, C, WHITE, fill=GRAY_E, op=0.25)
        n50 = M(r"50^\circ", 32, COL_ANG).move_to(A + 1.25 * unit(25))
        n70 = M(r"70^\circ", 32, COL_ANG3).move_to(C + 1.25 * unit(265))
        n60 = M(r"60^\circ", 32, COL_ANG2).move_to(B + 1.2 * unit(150))
        base_w = VGroup(wedge(A, 0, 50, 0.85, COL_ANG, 0.6), wedge(B, 120, 60, 0.85, COL_ANG2, 0.6), wedge(C, 230, 70, 0.85, COL_ANG3, 0.6))
        Dx = B + RIGHT * 2.6
        with self.say("Una conseguenza utile: l'angolo esterno. Prendo il triangolo con angoli di 50, 60 e 70 gradi, e prolungo il lato AB oltre B."):
            self.play(Create(t2), FadeIn(VGroup(la, lb, lc)), FadeIn(base_w), FadeIn(VGroup(n50, n60, n70)))
            self.play(Create(DashedLine(B, Dx, color=WHITE)), FadeIn(M("D", 32).next_to(Dx, DOWN, buff=0.15)))
        wext = wedge(B, 0, 120, 0.7, COL_RES, 0.5)
        next_ = M(r"120^\circ", 34, COL_RES).move_to(B + 1.05 * unit(55))
        eqx = M(r"180^\circ - 60^\circ = 120^\circ = 50^\circ + 70^\circ", 38, COL_RES).move_to(P(3.3, 2.5))
        with self.say("L'angolo esterno in B è il supplementare di 60: cioè 120 gradi. E guarda: 120 è proprio 50 più 70!"):
            self.play(FadeIn(wext), Write(next_))
            self.play(Write(eqx), run_time=1.8)
        with self.say("Un angolo esterno è sempre uguale alla somma dei due angoli interni lontani da lui."):
            self.play(Circumscribe(eqx, color=COL_RES))
        self.wipe()

        e1 = VGroup(T("Due angoli: 50° e 60°. Il terzo?", 32),
                    M(r"180^\circ - 50^\circ - 60^\circ = 70^\circ", 44, COL_RES)).arrange(DOWN, buff=0.3).move_to(P(0, 1.9))
        with self.say("Esempio: due angoli misurano cinquanta e sessanta gradi. Il terzo? Centottanta meno cinquanta meno sessanta: settanta gradi."):
            self.play(FadeIn(e1[0]))
            self.play(Write(e1[1]))
        e2 = VGroup(T("Isoscele, angolo al vertice 40°", 32),
                    M(r"\frac{180^\circ - 40^\circ}{2} = 70^\circ", 44, COL_RES)).arrange(DOWN, buff=0.3).move_to(P(0, -0.5))
        with self.say("In un triangolo isoscele gli angoli alla base sono uguali. Se l'angolo al vertice è quaranta gradi, ciascun angolo alla base è centottanta meno quaranta, diviso due: settanta gradi."):
            self.play(FadeIn(e2[0]))
            self.play(Write(e2[1]))
        e3 = T("Due angoli ottusi? Impossibile: supererebbero già 180°.", 30, COL_ERR).move_to(P(0, -2.3))
        with self.say("E una conseguenza: un triangolo non può avere due angoli ottusi, perché supererebbero già centottanta gradi."):
            self.play(FadeIn(e3))
        self.end()


# ══════════════════════════════════════════════════════════════════════
# PARTE 8: le altezze
# ══════════════════════════════════════════════════════════════════════
class P08_Altezze(LessonScene):
    PART, TITLE = 8, "Le altezze"

    def construct(self):
        self.title_card()
        # the measuring analogy
        floor = Line(P(-5.5, -2.2), P(-1.0, -2.2), color=GRAY_B, stroke_width=4)
        wall = Line(P(-4.8, -2.2), P(-4.8, 2.4), color=GRAY_B, stroke_width=4)
        head = Circle(radius=0.32, color=WHITE, stroke_width=3).move_to(P(-3.3, 1.3))
        body = VGroup(Line(P(-3.3, 0.98), P(-3.3, -0.8)), Line(P(-3.3, -0.8), P(-3.65, -2.2)), Line(P(-3.3, -0.8), P(-2.95, -2.2)),
                      Line(P(-3.3, 0.5), P(-3.8, -0.3)), Line(P(-3.3, 0.5), P(-2.8, -0.3))).set_stroke(WHITE, 3)
        bar = Line(P(-4.8, 1.62), P(-2.9, 1.62), color=COL_ANG, stroke_width=5)
        down = Arrow(P(-2.3, 1.62), P(-2.3, -2.2), buff=0, color=COL_RES, stroke_width=5)
        slant = Arrow(P(-2.3, 1.62), P(-1.2, -2.2), buff=0, color=COL_ERR, stroke_width=4)
        with self.say("Parliamo di altezze. Quando il medico misura quanto sei alta, l'asticella scende dritta, ad angolo retto, fino al pavimento."):
            self.play(Create(floor), Create(wall), Create(head), Create(body), run_time=1.5)
            self.play(Create(bar), GrowArrow(down))
        with self.say("Un metro tenuto storto darebbe un numero più grande, e sarebbe sbagliato."):
            self.play(GrowArrow(slant))
            self.play(Create(Cross(slant, stroke_color=COL_ERR, stroke_width=4, scale_factor=0.4)))
        self.wipe()

        A, B, C = P(-4.6, -2.0), P(1.4, -2.0), P(-2.4, 1.6)
        t = tri(A, B, C, WHITE, fill=GRAY_E, op=0.25)
        G = (A + B + C) / 3
        labs = VGroup(vlabel("A", A, G), vlabel("B", B, G), vlabel("C", C, G))
        xs = ValueTracker(-0.6)
        sl = always_redraw(lambda: Line(C, P(xs.get_value(), -2.0), color=COL_AUX, stroke_width=5))
        ang = always_redraw(lambda: deg_number(convex(P(xs.get_value(), -2.0), C, B)[1], P(xs.get_value() + 0.75, -1.55), COL_AUX, 30))
        with self.say("L'altezza di un triangolo è la stessa idea: il segmento che parte da un vertice e cade perpendicolare sul lato opposto."):
            self.play(Create(t), FadeIn(labs), run_time=1.3)
            self.play(Create(sl), FadeIn(ang))
        with self.say("Se il segmento è storto, non è un'altezza. Lo sposto finché forma un angolo retto."):
            self.play(xs.animate.set_value(0.4), run_time=1.4)
            self.play(xs.animate.set_value(-2.4), run_time=2.4)
        H = P(-2.4, -2.0)
        rm = rmark(H, B, C, 0.25, COL_AUX)
        lh = M("H", 34, COL_AUX).next_to(H, DOWN, buff=0.15)
        with self.say("Ecco: novanta gradi. Il punto acca si chiama piede dell'altezza."):
            self.play(Create(rm), FadeIn(lh))
        note = VGroup(T("un triangolo ha 3 lati", 30), T("quindi 3 altezze", 30, COL_AUX)).arrange(DOWN, aligned_edge=LEFT).move_to(P(4.3, 1.3))
        with self.say("Un triangolo ha tre lati, quindi ha tre altezze: una per ogni lato."):
            self.play(FadeIn(note))
        self.wipe()

        # three cases
        def case(A, B, C, shift, s=0.62, ext=None):
            A, B, C = A * s + shift, B * s + shift, C * s + shift
            Ha, Hb, Hc = foot(A, B, C), foot(B, A, C), foot(C, A, B)
            H = intersect(A, Ha, B, Hb)
            grp = VGroup(tri(A, B, C, WHITE, fill=GRAY_E, op=0.3))
            alts = VGroup(seg(A, Ha, COL_AUX, 3.5), seg(B, Hb, COL_AUX, 3.5), seg(C, Hc, COL_AUX, 3.5))
            return A, B, C, H, grp, alts
        # acute, right, obtuse (coordinates checked in verify.py of the booklet)
        a = case(P(0, 0), P(4, 0), P(1.6, 3.0), P(-6.3, -1.0))
        r = case(P(0, 0), P(4, 0), P(0, 3.0), P(-1.4, -1.0))
        o = case(P(0, 0), P(3.4, 0), P(-0.7, 2.4), P(3.9, -0.3))
        cap_a = T("acutangolo: dentro", 24).move_to(P(-5.05, -1.6))
        cap_r = T("rettangolo: sul vertice", 24).move_to(P(-0.15, -1.6))
        cap_o = T("ottusangolo: fuori", 24).move_to(P(4.95, -1.75))
        with self.say("Nel triangolo acutangolo le tre altezze stanno dentro e si incontrano in un punto: l'ortocentro."):
            self.play(Create(a[4]))
            self.play(LaggedStart(*[Create(x) for x in a[5]], lag_ratio=0.4), run_time=1.8)
            self.play(FadeIn(Dot(a[3], color=COL_ERR, radius=0.09)), FadeIn(cap_a))
        with self.say("Nel triangolo rettangolo due altezze sono i cateti stessi, e l'ortocentro è proprio il vertice dell'angolo retto."):
            self.play(Create(r[4]))
            self.play(Create(r[5][0]), Indicate(seg(r[0], r[1], COL_AUX, 6)), Indicate(seg(r[0], r[2], COL_AUX, 6)), run_time=1.8)
            self.play(FadeIn(Dot(r[3], color=COL_ERR, radius=0.09)), FadeIn(cap_r))
        oA, oB, oC, oH = o[0], o[1], o[2], o[3]
        exts = VGroup(DashedLine(foot(oC, oA, oB), oA, color=GRAY_B), DashedLine(oA, foot(oB, oA, oC), color=GRAY_B),
                      DashedLine(foot(oC, oA, oB), oH, color=COL_AUX), DashedLine(foot(oB, oA, oC), oH, color=COL_AUX),
                      DashedLine(oA, oH, color=COL_AUX))
        with self.say("Nel triangolo ottusangolo due altezze cadono fuori: bisogna prolungare i lati. E l'ortocentro finisce fuori dal triangolo."):
            self.play(Create(o[4]))
            self.play(Create(exts[0]), Create(exts[1]))
            self.play(LaggedStart(*[Create(x) for x in o[5]], lag_ratio=0.4), run_time=1.6)
            self.play(Create(exts[2:]), run_time=1.2)
            self.play(FadeIn(Dot(oH, color=COL_ERR, radius=0.09)), FadeIn(cap_o))
        with self.say("Attenzione: nel caso ottusangolo non sono i segmenti a toccarsi, ma le rette su cui stanno."):
            self.play(Indicate(exts[2:], color=COL_AUX), run_time=1.5)
        self.wipe()

        # 3-4-5 turned three ways
        k = 0.9
        loc = [P(0, 0), P(4, 0), P(0, 3)]    # right angle at vertex 0, legs 4 and 3
        poly = Polygon(*[p * k for p in loc], color=WHITE, stroke_width=4).set_fill(GRAY_E, 0.3)
        poly.move_to(P(-2.6, -0.3))

        def verts():
            v = poly.get_vertices()
            return v[0], v[1], v[2]

        info = VGroup()

        def show(base_pair, alt, text_formula, base_len, alt_len, alt_side=RIGHT):
            nonlocal info
            p, q = base_pair
            v = verts()
            cen = (v[0] + v[1] + v[2]) / 3
            mid = (p + q) / 2
            away = (mid - cen) / norm(mid - cen)
            a0, a1 = alt.get_start(), alt.get_end()
            items = VGroup(Line(p, q, color=COL_ANG2, stroke_width=8), alt,
                           M(text_formula, 44, COL_RES).move_to(P(3.3, 0.3)),
                           M(base_len, 34, COL_ANG2).move_to(mid + 0.38 * away),
                           M(alt_len, 34, COL_AUX).next_to((a0 + a1) / 2, alt_side, buff=0.15))
            info = items
            return items

        with self.say("L'altezza non è la linea verticale: dipende da quale lato scegli come base. Guarda questo triangolo rettangolo con i lati tre, quattro e cinque."):
            self.play(Create(poly))
        v0, v1, v2 = verts()
        it = show((v0, v1), Line(v0, v2, color=COL_AUX, stroke_width=6), r"\frac{4\cdot 3}{2} = 6", "4", "3", LEFT)
        with self.say("Base quattro, altezza tre: l'area è quattro per tre diviso due, cioè sei."):
            self.play(Create(it[0]), Create(it[1]), FadeIn(it[3]), FadeIn(it[4]))
            self.play(Write(it[2]))
        self.play(FadeOut(info))
        self.play(Rotate(poly, angle=PI / 2, about_point=poly.get_center()), run_time=1.5)
        v0, v1, v2 = verts()
        it = show((v2, v0), Line(v0, v1, color=COL_AUX, stroke_width=6), r"\frac{3\cdot 4}{2} = 6", "3", "4", RIGHT)
        with self.say("Lo giro: base tre, altezza quattro. L'area è ancora sei."):
            self.play(Create(it[0]), Create(it[1]), FadeIn(it[3]), FadeIn(it[4]))
            self.play(Write(it[2]))
        self.play(FadeOut(info))
        # rotate so that the hypotenuse is horizontal with the right angle on top
        v0, v1, v2 = verts()
        hyp = dirdeg(v2 - v1)
        rot = -hyp if (v0 - v1)[1] * np.cos(np.radians(hyp)) - (v0 - v1)[0] * np.sin(np.radians(hyp)) >= 0 else 180 - hyp
        self.play(Rotate(poly, angle=np.radians(rot), about_point=poly.get_center()), run_time=1.5)
        v0, v1, v2 = verts()
        F = foot(v0, v1, v2)
        it = show((v1, v2), Line(v0, F, color=COL_AUX, stroke_width=6), r"\frac{5\cdot h}{2} = 6 \ \Rightarrow\ h = 2{,}4", "5", "h", RIGHT)
        with self.say("Lo giro ancora: base cinque. L'area è sempre sei, quindi cinque per acca diviso due fa sei, e l'altezza è due virgola quattro."):
            self.play(Create(it[0]), Create(it[1]), Create(rmark(F, v2, v0, 0.2, COL_AUX)), FadeIn(it[3]), FadeIn(it[4]))
            self.play(Write(it[2]))
        rule = T("L'altezza viaggia sempre con la sua base.", 32, COL_RES).move_to(P(0, 2.7))
        with self.say("La regola da ricordare: l'altezza viaggia sempre insieme alla sua base."):
            self.play(Write(rule))
        self.wipe()
        # base 10 with altitude 6; another side of 12 (scale 0.5 unit per cm)
        A, B = A8, B8
        C = C8
        Hc = foot(C, A, B)
        Fb = foot(B, A, C)
        tr = tri(A, B, C, WHITE, fill=GRAY_E, op=0.3)
        G = (A + B + C) / 3
        labs = VGroup(vlabel("A", A, G), vlabel("B", B, G), vlabel("C", C, G))
        with self.say("Un ultimo esempio. Un triangolo ha un lato di 10 centimetri, e l'altezza relativa a quel lato è 6 centimetri."):
            self.play(Create(tr), FadeIn(labs))
            self.play(Create(seg(A, B, COL_ANG2, 7)), Create(DashedLine(B, Hc, color=GRAY_B)), Create(seg(C, Hc, COL_AUX, 5)), Create(rmark(Hc, A, C, 0.2, COL_AUX)))
            self.play(FadeIn(M("10", 32, COL_ANG2).next_to((A + B) / 2, DOWN, buff=0.15)), FadeIn(M("6", 32, COL_AUX).next_to((C + Hc) / 2, RIGHT, buff=0.12)))
        a1 = M(r"\text{Area} = \frac{10\cdot 6}{2} = 30", 40).move_to(P(3.6, 2.4))
        with self.say("L'area è 10 per 6 diviso 2: 30 centimetri quadrati."):
            self.play(Write(a1))
        with self.say("Un altro lato, AC, misura 12 centimetri. Quanto è lunga l'altezza relativa a quel lato?"):
            self.play(Create(seg(A, C, COL_ANG2, 7)), FadeIn(M("12", 32, COL_ANG2).move_to((A + C) / 2 + P(-0.35, 0.3))))
            self.play(Create(seg(B, Fb, COL_RES, 5)), Create(rmark(Fb, C, B, 0.2, COL_RES)))
        a2 = M(r"\frac{12\cdot h}{2} = 30 \ \Rightarrow\ h = 5", 40, COL_RES).move_to(P(3.6, 1.1))
        with self.say("L'area non cambia: 12 per acca diviso 2 fa 30, quindi acca è 5 centimetri."):
            self.play(Write(a2))
            self.play(Circumscribe(a2, color=COL_RES))
        self.end()


# ══════════════════════════════════════════════════════════════════════
# PARTE 9: la congruenza
# ══════════════════════════════════════════════════════════════════════
class P09_Congruenza(LessonScene):
    PART, TITLE = 9, "Che cos'è la congruenza"

    def construct(self):
        self.title_card()
        A, B, C = P(-5.0, -1.4), P(-2.0, -1.4), P(-4.1, 0.9)
        t1 = VGroup(tri(A, B, C, WHITE, fill=COL_GIV, op=0.25), ticks(A, B, 1), ticks(B, C, 2), ticks(C, A, 3))
        cen = (A + B + C) / 3
        t2 = t1.copy().flip(UP, about_point=cen).rotate(140 * DEGREES, about_point=cen).shift(RIGHT * 7.8 + UP * 0.6)
        t2[0].set_fill(COL_RES, 0.25)
        d1 = T("Due figure sono congruenti se una si sovrappone perfettamente all'altra.", 28).move_to(P(0, 2.7))
        with self.say("Ora la parola più importante di oggi: congruente. Due figure sono congruenti se puoi sovrapporle perfettamente, muovendone una senza deformarla."):
            self.play(FadeIn(d1))
            self.play(Create(t1), Create(t2), run_time=1.6)
        with self.say("Puoi farla scivolare, ruotarla, e anche ribaltarla. Ma mai allungarla o piegarla."):
            self.play(t2.animate.shift(LEFT * 7.8 + DOWN * 0.6), run_time=2.0)
        with self.say("Guarda: la ruoto, la ribalto, e combacia perfettamente. Sono congruenti."):
            self.play(Rotate(t2, angle=-140 * DEGREES, about_point=cen), run_time=1.6)
            self.play(t2.animate.flip(UP, about_point=cen), run_time=1.4)
            self.play(Flash(cen, color=COL_RES, flash_radius=1.8))
        self.wipe()

        # corresponding parts
        A, B, C = P(-5.2, -1.5), P(-2.0, -1.5), P(-4.2, 1.0)
        D, E, F = P(1.8, 1.2), P(4.6, -0.4), P(2.1, -1.6)   # rotated copy (same lengths not needed exactly for the naming idea)
        # build DEF as an exact rotated copy of ABC
        rotm = lambda p, c, a: c + np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]]) @ (p - c)
        cen = (A + B + C) / 3
        D, E, F = [rotm(p, cen, -2.2) + P(6.9, 0.3) for p in (A, B, C)]
        g1 = VGroup(tri(A, B, C, WHITE, fill=COL_GIV, op=0.2), ticks(A, B, 1), ticks(B, C, 2), ticks(C, A, 3))
        g2 = VGroup(tri(D, E, F, WHITE, fill=COL_GIV, op=0.2), ticks(D, E, 1), ticks(E, F, 2), ticks(F, D, 3))
        c1, c2 = (A + B + C) / 3, (D + E + F) / 3
        L1 = VGroup(vlabel("A", A, c1), vlabel("B", B, c1), vlabel("C", C, c1))
        L2 = VGroup(vlabel("D", D, c2), vlabel("E", E, c2), vlabel("F", F, c2))
        eq = M(r"\triangle ABC \cong \triangle DEF", 46).move_to(P(0, 2.6))
        with self.say("Quando due triangoli sono congruenti, ogni lato e ogni angolo ha un compagno: si chiamano elementi omologhi."):
            self.play(Create(g1), Create(g2), FadeIn(L1), FadeIn(L2), run_time=1.6)
        with self.say("L'ordine delle lettere conta: a bi ci congruente a di e effe vuol dire che a va con di, bi con e, ci con effe."):
            self.play(Write(eq))
            for p, q in zip(L1, L2):
                self.play(Indicate(p, color=COL_ANG, scale_factor=1.6), Indicate(q, color=COL_ANG, scale_factor=1.6), run_time=0.8)
        with self.say("Una regola utile: i lati omologhi stanno di fronte agli angoli omologhi, e hanno lo stesso numero di trattini."):
            self.play(Indicate(g1[2], color=COL_ANG), Indicate(g2[2], color=COL_ANG), run_time=1.4)
        self.wipe()

        # traps
        k = 0.62
        ta = VGroup(tri(P(-6, -1.8), P(-6 + 4 * k, -1.8), P(-6, -1.8 + 3 * k), WHITE, fill=COL_GIV, op=0.25),
                    M(r"A = 6", 30).move_to(P(-5.3, -1.2))).shift(UP * 0.5)
        tb = VGroup(tri(P(-3.0, -1.8), P(-3.0 + 6 * k, -1.8), P(-3.0, -1.8 + 2 * k), WHITE, fill=COL_ERR, op=0.25),
                    M(r"A = 6", 30).move_to(P(-2.2, -1.45))).shift(UP * 0.5)
        neq = M(r"\ncong", 50, COL_ERR).move_to(P(-3.4, 0.9))
        tt = T("Trappola 1: stessa area", 30, COL_ERR).move_to(P(-3.6, 2.6))
        with self.say("Trappola numero uno: stessa area non vuol dire congruenti. Questi due triangoli hanno entrambi area sei, ma forme diverse."):
            self.play(FadeIn(tt), Create(ta), Create(tb), run_time=1.5)
            self.play(Write(neq))
        eqa = VGroup(tri(P(1.2, -1.8), P(4.4, -1.8), P(2.8, -1.8 + 2.771), WHITE, fill=COL_GIV, op=0.25),
                     tri(P(5.0, -1.8), P(6.4, -1.8), P(5.7, -1.8 + 1.212), WHITE, fill=COL_ERR, op=0.25)).shift(UP * 0.5)
        a60 = T("tutti gli angoli: 60°", 26).move_to(P(3.9, -1.95))
        tt2 = T("Trappola 2: stessi angoli", 30, COL_ERR).move_to(P(3.8, 2.6))
        with self.say("Trappola numero due: stessi angoli non basta. Due triangoli equilateri hanno tutti gli angoli di sessanta gradi, ma uno può essere molto più grande."):
            self.play(FadeIn(tt2), Create(eqa), FadeIn(a60), run_time=1.5)
        fin = T("Congruenti = stessa forma E stessa grandezza", 32, COL_RES).move_to(P(0, 1.95))
        with self.say("Congruenti vuol dire stessa forma e stessa grandezza."):
            self.play(Write(fin))
        self.end()


# ══════════════════════════════════════════════════════════════════════
# PARTE 10: i tre criteri
# ══════════════════════════════════════════════════════════════════════
class P10_Criteri(LessonScene):
    PART, TITLE = 10, "I tre criteri di congruenza"

    def construct(self):
        self.title_card()
        q = T("Come sapere se due triangoli sono congruenti, senza ritagliarli?", 30).move_to(P(0, 2.6))
        six = VGroup(T("3 lati", 34, COL_GIV), T("+", 34), T("3 angoli", 34, COL_ANG), T("= 6 misure", 34)).arrange(RIGHT, buff=0.3).move_to(P(0, 0.9))
        three = T("ne bastano 3, se sono quelle giuste", 34, COL_RES).move_to(P(0, -0.3))
        with self.say("Come facciamo a sapere se due triangoli sono congruenti, senza ritagliarli?"):
            self.play(FadeIn(q))
        with self.say("Un triangolo ha sei misure: tre lati e tre angoli. Ma ne bastano tre, se sono quelle giuste. Sono i criteri di congruenza."):
            self.play(FadeIn(six))
            self.play(Write(three))
        self.wipe()

        A, B, C = A10, B10, C10
        info_x = 3.9
        # SAS
        h = VGroup(T("Primo criterio: LAL", 36, COL_RES), T("due lati e l'angolo compreso", 28)).arrange(DOWN, buff=0.2).move_to(P(info_x, 2.3))
        with self.say("Primo criterio, LAL: due lati e l'angolo compreso tra loro."):
            self.play(FadeIn(h))
        ang = VGroup(Line(A, A + 4.6 * RIGHT, color=GRAY_B, stroke_width=2), Line(A, A + 3.6 * unit(55), color=GRAY_B, stroke_width=2),
                     wedge(A, 0, 55, 0.8, COL_ANG, 0.5), M(r"55^\circ", 30, COL_ANG).move_to(A + 1.15 * unit(27)))
        sAB, sAC = seg(A, B, COL_GIV, 6), seg(A, C, COL_GIV, 6)
        with self.say("Disegno l'angolo, e sui suoi lati riporto le due lunghezze."):
            self.play(Create(ang), run_time=1.2)
            self.play(Create(sAB), Create(sAC), run_time=1.4)
        third = DashedLine(B, C, color=COL_RES, dash_length=0.15)
        with self.say("Gli estremi sono fissati, e il terzo lato non ha scelta: è obbligato."):
            self.play(Create(third), run_time=1.2)
            self.play(ReplacementTransform(third, seg(B, C, COL_RES, 6)))
            self.play(Flash(C, color=COL_RES))
        self.wipe()

        # ASA
        h = VGroup(T("Secondo criterio: ALA", 36, COL_RES), T("un lato e i due angoli adiacenti", 28)).arrange(DOWN, buff=0.2).move_to(P(info_x, 2.3))
        with self.say("Secondo criterio, ALA: un lato e i due angoli adiacenti."):
            self.play(FadeIn(h), Create(seg(A, B, COL_GIV, 6)))
            self.play(FadeIn(wedge(A, 0, 55, 0.8, COL_ANG, 0.5)), FadeIn(wedge(B, 180 - ANG_B10, ANG_B10, 0.8, COL_ANG2, 0.5)))
        rA = Line(A, A + 1.25 * (C - A), color=COL_ANG, stroke_width=3)
        rB = Line(B, B + 1.3 * (C - B), color=COL_ANG2, stroke_width=3)
        with self.say("Dagli estremi partono due semirette con gli angoli dati. Due semirette non parallele si incontrano in un solo punto: il terzo vertice."):
            self.play(Create(rA), Create(rB), run_time=2.0)
            dC = Dot(C, color=COL_RES, radius=0.12)
            self.play(FadeIn(dC, scale=2))
            self.play(Flash(C, color=COL_RES))
        self.wipe()

        # SSS
        h = VGroup(T("Terzo criterio: LLL", 36, COL_RES), T("tre lati", 28)).arrange(DOWN, buff=0.2).move_to(P(info_x, 2.3))
        with self.say("Terzo criterio, LLL: tre lati."):
            self.play(FadeIn(h), Create(seg(A, B, COL_GIV, 6)))
        cA = Arc(radius=norm(C - A), start_angle=np.radians(35), angle=np.radians(45), arc_center=A, color=COL_GIV, stroke_width=3)
        cB = Arc(radius=BC10, start_angle=np.radians(180 - ANG_B10 - 25), angle=np.radians(45), arc_center=B, color=COL_GIV, stroke_width=3)
        with self.say("Il terzo vertice deve stare a una certa distanza da a, e a un'altra distanza da bi: due archi di circonferenza, che sopra la base si incontrano in un solo punto."):
            self.play(Create(cA), run_time=1.3)
            self.play(Create(cB), run_time=1.3)
            self.play(FadeIn(Dot(C, color=COL_RES, radius=0.12), scale=2))
            self.play(Create(DashedLine(A, C, color=COL_RES)), Create(DashedLine(B, C, color=COL_RES)))
        self.wipe()

        # rigidity
        s = 1.7
        O = P(-5.2, -1.6)
        ang_t = ValueTracker(90)
        sq = always_redraw(lambda: VMobject(color=COL_DOOR, stroke_width=7).set_points_as_corners(
            [O, O + RIGHT * s, O + RIGHT * s + s * unit(ang_t.get_value()), O + s * unit(ang_t.get_value()), O]))
        pins = always_redraw(lambda: VGroup(*[Dot(p, radius=0.08, color=WHITE) for p in
                                              [O, O + RIGHT * s, O + RIGHT * s + s * unit(ang_t.get_value()), O + s * unit(ang_t.get_value())]]))
        T0 = P(-1.0, -1.6)
        trg = VGroup(VMobject(color=COL_DOOR, stroke_width=7).set_points_as_corners([T0, T0 + RIGHT * s, T0 + s * unit(60), T0]),
                     *[Dot(p, radius=0.08) for p in [T0, T0 + RIGHT * s, T0 + s * unit(60)]])
        with self.say("È per questo che il triangolo è rigido. Un quadrato fatto di bastoncini si piega..."):
            self.add(sq, pins)
            self.play(ang_t.animate.set_value(58), run_time=2.0)
        with self.say("un triangolo no: tre lati fissano tutto, anche gli angoli."):
            self.play(Create(trg))
            self.play(Wiggle(trg, scale_value=1.02, rotation_angle=0.01 * TAU), run_time=1.2)
        Tr = P(3.0, -1.6)
        truss = VGroup(Line(Tr, Tr + P(4.0, 0)), Line(Tr + P(4.0, 0), Tr + P(2.0, 1.5)), Line(Tr + P(2.0, 1.5), Tr),
                       Line(Tr + P(2.0, 0), Tr + P(2.0, 1.5)), Line(Tr + P(1.0, 0.75), Tr + P(2.0, 0)), Line(Tr + P(2.0, 0), Tr + P(3.0, 0.75))).set_stroke(COL_DOOR, 6)
        with self.say("Per questo tetti, gru e ponti sono pieni di triangoli."):
            self.play(Create(truss), run_time=1.6)
            self.play(FadeIn(T("capriata", 26, COL_DOOR).next_to(truss, DOWN, buff=0.2)))
        self.wipe()

        # SSA fails
        u = U_SSA
        A2, B2 = P(-5.8, -2.1), P(-5.8 + 6 * u, -2.1)
        C1 = A2 + T1_SSA * u * unit(30)
        C2 = A2 + T2_SSA * u * unit(30)
        hh = T("LLA non funziona", 34, COL_ERR).move_to(P(3.6, 2.4))
        with self.say("Ma attenzione: non tutte le terne funzionano. Due lati e un angolo non compreso: LLA."):
            self.play(FadeIn(hh))
        rayA = Line(A2, A2 + 9.3 * u * unit(30), color=WHITE, stroke_width=3)
        with self.say("Angolo in a di trenta gradi, a bi lungo sei, bi ci lungo quattro."):
            self.play(Create(seg(A2, B2, COL_GIV, 5)), Create(rayA), FadeIn(wedge(A2, 0, 30, 0.9, COL_ANG, 0.5)))
            self.play(FadeIn(M(r"30^\circ", 28, COL_ANG).move_to(A2 + 1.3 * unit(15))))
        circ = Arc(radius=4 * u, start_angle=np.radians(40), angle=np.radians(150), arc_center=B2, color=COL_GRID, stroke_width=2)
        with self.say("La circonferenza di raggio quattro intorno a bi taglia la semiretta due volte: due triangoli diversi, con gli stessi dati. Non è un criterio."):
            self.play(Create(circ), run_time=1.4)
            self.play(FadeIn(tri(A2, B2, C1, COL_GIV, fill=COL_GIV, op=0.25)), FadeIn(tri(A2, B2, C2, COL_ERR, fill=COL_ERR, op=0.35)))
            self.play(FadeIn(M("C_1", 32, COL_GIV).next_to(C1, UP, buff=0.12)), FadeIn(M("C_2", 32, COL_ERR).next_to(C2, UP + LEFT, buff=0.1)))
        aaa = T("e AAA fissa solo la forma, non la grandezza", 28, COL_ERR).move_to(P(3.3, 1.5))
        with self.say("E tre angoli, AAA, fissano solo la forma, non la grandezza."):
            self.play(FadeIn(aaa))
        self.end()


# ══════════════════════════════════════════════════════════════════════
# PARTE 11: come si dimostra
# ══════════════════════════════════════════════════════════════════════
class P11_Dimostrazioni(LessonScene):
    PART, TITLE = 11, "Come si scrive una dimostrazione"

    def construct(self):
        self.title_card()
        cards = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=1.1, corner_radius=0.15, color=c, stroke_width=3),
                                T(s, 30, c)) for s, c in [("1. Disegno", WHITE), ("2. Ipotesi", COL_GIV),
                                                            ("3. Tesi", COL_RES), ("4. Dimostrazione", COL_ANG)]])
        for cd in cards:
            cd[1].move_to(cd[0])
        cards.arrange(RIGHT, buff=0.3).move_to(P(0, 0.4))
        with self.say("Adesso impariamo a dimostrare, con il metodo del tuo quaderno: disegno, ipotesi, tesi, e poi la dimostrazione."):
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.4), run_time=2.4)
        self.wipe()

        A, B, C = P(-3.6, 2.0), P(-5.8, -2.0), P(-1.4, -2.0)
        D = P(-3.6, -2.0)
        G = (A + B + C) / 3
        base = VGroup(tri(A, B, C, WHITE), ticks(A, B, 1, COL_GIV), ticks(A, C, 1, COL_GIV))
        labs = VGroup(vlabel("A", A, G), vlabel("B", B, G, dist=0.35), vlabel("C", C, G, dist=0.35))
        hyp = VGroup(M(r"\text{Ipotesi: } \overline{AB} \cong \overline{AC}", 36, COL_GIV),
                     M(r"\text{Tesi: } \widehat{B} \cong \widehat{C}", 36, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(P(2.9, 2.4))
        with self.say("Primo esempio: in un triangolo isoscele gli angoli alla base sono congruenti."):
            self.play(Create(base), FadeIn(labs), run_time=1.5)
        with self.say("Ipotesi: a bi è congruente ad a ci. Tesi: l'angolo bi è congruente all'angolo ci."):
            self.play(Write(hyp), run_time=1.6)
        bis = seg(A, D, COL_AUX, 5)
        ld = M("D", 34, COL_AUX).next_to(D, DOWN, buff=0.15)
        am = VGroup(angle_mark(A, B, D, 0.7, COL_AUX, 0.35), angle_mark(A, D, C, 0.8, COL_AUX, 0.2))
        with self.say("Traccio la bisettrice dell'angolo in a: divide l'angolo in due parti uguali, e arriva in di."):
            self.play(Create(bis), FadeIn(ld), FadeIn(am))
        f1 = tri(A, B, D, COL_GIV, fill=COL_GIV, op=0.25, w=0)
        f2 = tri(A, D, C, COL_RES, fill=COL_RES, op=0.2, w=0)
        with self.say("Considero i triangoli a bi di e a ci di."):
            self.play(FadeIn(f1), FadeIn(f2))
        st = steps_column([(r"\overline{AB} \cong \overline{AC}", "per ipotesi", COL_GIV),
                           (r"B\widehat{A}D \cong C\widehat{A}D", "AD è bisettrice", COL_AUX),
                           (r"\overline{AD}\ \text{in comune}", "lato in comune", WHITE)], x=0.3, y_top=1.0, fs=34)
        with self.say("A bi è congruente ad a ci, per ipotesi."):
            self.play(Write(st[0]))
        with self.say("Gli angoli in a sono congruenti, perché a di è la bisettrice."):
            self.play(Write(st[1]))
        with self.say("E a di è un lato in comune."):
            self.play(Write(st[2]))
        concl = M(r"\text{LAL} \Rightarrow \triangle ABD \cong \triangle ACD", 38, COL_RES).next_to(st, DOWN, buff=0.4, aligned_edge=LEFT)
        with self.say("Due lati e l'angolo compreso: per il primo criterio i triangoli sono congruenti. Guarda: ribaltando uno sulla bisettrice, combacia con l'altro."):
            self.play(Write(concl))
            ghost = f1.copy().set_fill(COL_GIV, 0.5)
            self.play(ghost.animate.flip(UP, about_point=A), run_time=1.6)
            self.play(Flash(D + UP * 1.3, color=COL_RES), FadeOut(ghost))
        angs = VGroup(angle_mark(B, C, A, 0.6, COL_RES, 0.5), angle_mark(C, A, B, 0.6, COL_RES, 0.5))
        fin = M(r"\widehat{B} \cong \widehat{C}\quad \text{c.v.d.}", 40, COL_RES).next_to(concl, DOWN, buff=0.3, aligned_edge=LEFT)
        with self.say("E allora anche gli angoli bi e ci, che sono omologhi, sono congruenti. Come volevasi dimostrare."):
            self.play(FadeIn(angs), Write(fin))
        self.wipe()

        # the altitude problem
        base = VGroup(tri(A, B, C, WHITE), ticks(A, B, 1, COL_GIV), ticks(A, C, 1, COL_GIV))
        H = D
        alt = seg(A, H, COL_AUX, 5)
        lh = M("H", 34, COL_AUX).next_to(H, DOWN, buff=0.15)
        rm = rmark(H, C, A, 0.25, COL_AUX)
        hyp = VGroup(M(r"\text{Ipotesi: } \overline{AB} \cong \overline{AC},\ AH \perp BC", 34, COL_GIV),
                     M(r"\text{Tesi: } \overline{BH} \cong \overline{HC}", 34, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(P(2.9, 2.5))
        with self.say("Ora un problema classico: nel triangolo isoscele a bi ci traccio l'altezza a acca relativa alla base."):
            self.play(Create(base), FadeIn(labs))
            self.play(Create(alt), FadeIn(lh), Create(rm))
        with self.say("Tesi: l'altezza divide la base in due parti uguali, e i triangoli a bi acca e a ci acca sono congruenti."):
            self.play(Write(hyp), run_time=1.6)
        st = steps_column([(r"\widehat{B} \cong \widehat{C}", "angoli alla base", COL_GIV),
                           (r"A\widehat{H}B = A\widehat{H}C = 90^\circ", "AH altezza", COL_AUX),
                           (r"B\widehat{A}H = 180^\circ - 90^\circ - \widehat{B}", "somma angoli", WHITE),
                           (r"B\widehat{A}H \cong C\widehat{A}H", "", COL_ANG)], x=0.3, y_top=1.1, fs=32, buff=0.22)
        with self.say("Gli angoli bi e ci sono congruenti: l'abbiamo appena dimostrato."):
            self.play(Write(st[0]), FadeIn(VGroup(angle_mark(B, C, A, 0.6, COL_GIV, 0.4), angle_mark(C, A, B, 0.6, COL_GIV, 0.4))))
        with self.say("Gli angoli in acca sono retti. Quindi, per la somma degli angoli, anche gli angoli in a sono uguali: centottanta meno novanta meno lo stesso angolo."):
            self.play(Write(st[1]))
            self.play(Write(st[2]))
            self.play(Write(st[3]), FadeIn(VGroup(angle_mark(A, B, H, 0.75, COL_ANG, 0.35), angle_mark(A, H, C, 0.85, COL_ANG, 0.25))))
        concl = M(r"\text{LAL} \Rightarrow \triangle ABH \cong \triangle ACH", 34, COL_RES).next_to(st, DOWN, buff=0.35, aligned_edge=LEFT)
        with self.say("Ora a bi acca e a ci acca hanno a bi congruente ad a ci, a acca in comune, e gli angoli compresi congruenti: primo criterio!"):
            self.play(Write(concl), run_time=1.8)
        res = VGroup(ticks(B, H, 2, COL_RES), ticks(H, C, 2, COL_RES))
        fin = VGroup(T("H è il punto medio:", 26, COL_RES), T("altezza = mediana = bisettrice", 26, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(concl, DOWN, buff=0.3, aligned_edge=LEFT)
        with self.say("Quindi bi acca è congruente ad acca ci: acca è il punto medio. In un triangolo isoscele l'altezza sulla base è anche mediana e bisettrice."):
            self.play(Create(res))
            self.play(FadeIn(fin))
            self.play(Flash(H, color=COL_RES))
        self.end()


# ══════════════════════════════════════════════════════════════════════
# PARTE 12: i problemi del quaderno
# ══════════════════════════════════════════════════════════════════════
class P12_Quaderno(LessonScene):
    PART, TITLE = 12, "I due problemi del quaderno"

    def construct(self):
        self.title_card()
        s, sh = 1.2, P(-3.6, -2.35)
        A, B, C = P(0, 3.0) * s + sh, P(-1.5, 0) * s + sh, P(1.5, 0) * s + sh
        D, E = P(0.675, 4.35) * s + sh, P(-0.675, 4.35) * s + sh
        G = (A + B + C) / 3
        tri0 = VGroup(tri(A, B, C, WHITE), ticks(A, B, 1, COL_GIV), ticks(A, C, 1, COL_GIV))
        labs = VGroup(M("A", 32).next_to(A, RIGHT, buff=0.15), vlabel("B", B, G), vlabel("C", C, G))
        txt = VGroup(T("ABC isoscele di base BC.", 26), T("Prolungo BA e CA oltre A", 26), T("di due segmenti congruenti AD e AE.", 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(P(3.0, 2.65))
        with self.say("Ora risolviamo insieme i due problemi del tuo quaderno. Primo problema: triangolo isoscele a bi ci, di base bi ci."):
            self.play(Create(tri0), FadeIn(labs), FadeIn(txt[0]))
        ext = VGroup(seg(A, D, COL_AUX, 4), seg(A, E, COL_AUX, 4), ticks(A, D, 2, COL_AUX), ticks(A, E, 2, COL_AUX),
                     M("D", 32, COL_AUX).next_to(D, UP, buff=0.12), M("E", 32, COL_AUX).next_to(E, UP, buff=0.12))
        with self.say("Prolunghiamo i lati bi a e ci a oltre a, di due segmenti congruenti: a di e a e."):
            self.play(FadeIn(txt[1:]), Create(ext), run_time=1.6)
        th1 = M(r"\text{Tesi: } \overline{BD} \cong \overline{CE}", 36, COL_RES).move_to(P(3.0, 1.5))
        sm = M(r"\overline{BD} = \overline{BA} + \overline{AD} \cong \overline{CA} + \overline{AE} = \overline{CE}", 32, COL_RES).move_to(P(2.9, 0.7))
        with self.say("La tesi, come è scritta nel quaderno: bi di è congruente a ci e."):
            self.play(Write(th1))
        with self.say("Bi di è a bi più a di, e ci e è a ci più a e. Sono somme di segmenti congruenti, quindi sono congruenti. Fatto!"):
            self.play(Indicate(seg(B, D, COL_RES, 7)), run_time=1.2)
            self.play(Indicate(seg(C, E, COL_RES, 7)), run_time=1.2)
            self.play(Write(sm), run_time=1.6)
        th2 = M(r"\text{Versione dei libri: } \overline{BE} \cong \overline{CD}\,?", 34, COL_ANG).move_to(P(3.0, -0.25))
        with self.say("Molti libri chiedono invece: bi e è congruente a ci di? Qui servono i triangoli."):
            self.play(Write(th2))
            self.play(Create(seg(B, E, COL_GIV, 3)), Create(seg(C, D, COL_RES, 3)))
        fA = tri(A, B, E, COL_GIV, fill=COL_GIV, op=0.25, w=0)
        fB = tri(A, C, D, COL_RES, fill=COL_RES, op=0.25, w=0)
        va = VGroup(angle_mark(A, B, E, 0.45, COL_ANG, 0.5), angle_mark(A, C, D, 0.45, COL_ANG, 0.5))
        st = M(r"\overline{AB}\cong\overline{AC},\ \overline{AE}\cong\overline{AD},\ B\widehat{A}E \cong C\widehat{A}D", 30).move_to(P(2.9, -1.15))
        with self.say("Considero a bi e, e a ci di: a bi è congruente ad a ci, a e ad a di, e gli angoli in a sono opposti al vertice."):
            self.play(FadeOut(sm), FadeIn(fA), FadeIn(fB), FadeIn(va))
            self.play(Write(st), run_time=1.6)
        fin = M(r"\text{LAL} \Rightarrow \overline{BE} \cong \overline{CD}", 36, COL_RES).move_to(P(2.9, -1.95))
        with self.say("Primo criterio: i triangoli sono congruenti, quindi bi e è congruente a ci di."):
            self.play(Write(fin))
            self.play(Circumscribe(fin, color=COL_RES))
        self.wipe()

        # problem 2
        s, sh = 1.15, P(-5.7, -2.35)
        A, B, C = P(0, 0) * s + sh, P(4, 0) * s + sh, P(2, 4.5) * s + sh
        Mm, N, Gg = P(3, 2.25) * s + sh, P(1, 2.25) * s + sh, P(2, 1.5) * s + sh
        G0 = (A + B + C) / 3
        base = VGroup(tri(A, B, C, WHITE), ticks(A, N, 1, COL_GIV), ticks(N, C, 1, COL_GIV), ticks(C, Mm, 1, COL_GIV), ticks(Mm, B, 1, COL_GIV))
        labs = VGroup(vlabel("A", A, G0), vlabel("B", B, G0), vlabel("C", C, G0),
                      M("N", 32).next_to(N, LEFT, buff=0.15), M("M", 32).next_to(Mm, RIGHT, buff=0.15))
        meds = VGroup(seg(A, Mm, COL_AUX, 4), seg(B, N, COL_AUX, 4))
        lg = M("G", 32, COL_AUX).next_to(Gg, DOWN, buff=0.2)
        with self.say("Secondo problema: triangolo isoscele di base a bi. Le mediane a emme e bi enne arrivano nei punti medi dei lati congruenti, e si incontrano in gi."):
            self.play(Create(base), FadeIn(labs), run_time=1.5)
            self.play(Create(meds), FadeIn(lg))
        th = M(r"\text{Tesi: } \triangle AGN \cong \triangle BGM", 36, COL_RES).move_to(P(3.0, 2.6))
        fAGN = tri(A, Gg, N, COL_GIV, fill=COL_GIV, op=0.3, w=0)
        fBGM = tri(B, Gg, Mm, COL_RES, fill=COL_RES, op=0.3, w=0)
        with self.say("Tesi: i triangoli a gi enne e bi gi emme sono congruenti."):
            self.play(Write(th), FadeIn(fAGN), FadeIn(fBGM))
        st = steps_column([(r"\overline{AN} \cong \overline{BM}", "metà di lati congruenti", COL_GIV),
                           (r"\triangle ABN \cong \triangle BAM", "LAL", COL_ANG),
                           (r"A\widehat{N}B \cong B\widehat{M}A", "omologhi", WHITE),
                           (r"N\widehat{A}G \cong M\widehat{B}G", "differenze di angoli", WHITE)], x=0.2, y_top=1.9, fs=32, buff=0.25)
        with self.say("Primo passo: a enne e bi emme sono metà di lati congruenti, quindi sono congruenti."):
            self.play(Write(st[0]))
        big1 = tri(A, B, N, COL_ANG, w=5)
        with self.say("Secondo passo: i triangoli a bi enne e bi a emme hanno a bi in comune, a enne congruente a bi emme, e gli angoli alla base congruenti. Primo criterio: sono congruenti."):
            self.play(FadeOut(fAGN), FadeOut(fBGM), Create(big1))
            big2 = tri(B, A, Mm, COL_ANG, w=5)
            self.play(ReplacementTransform(big1, big2), run_time=1.5)
            self.play(Write(st[1]))
        with self.say("Da qui ricavo due coppie di angoli omologhi: gli angoli in enne e in emme, e gli angoli in bi e in a dei triangoli grandi."):
            self.play(Write(st[2]))
        with self.say("Terzo passo: togliendo angoli uguali da angoli uguali, anche gli angoli in a e in bi dei triangoli piccoli sono congruenti."):
            self.play(Write(st[3]))
        fin = M(r"\text{ALA} \Rightarrow \triangle AGN \cong \triangle BGM\quad \text{c.v.d.}", 34, COL_RES).next_to(st, DOWN, buff=0.4, aligned_edge=LEFT)
        with self.say("Ora a gi enne e bi gi emme hanno un lato congruente e i due angoli adiacenti congruenti: secondo criterio. Come volevasi dimostrare."):
            self.play(FadeOut(big2))
            self.play(FadeIn(tri(A, Gg, N, COL_GIV, fill=COL_GIV, op=0.35, w=0)), FadeIn(tri(B, Gg, Mm, COL_RES, fill=COL_RES, op=0.35, w=0)))
            self.play(Write(fin), run_time=1.6)
            self.play(Circumscribe(fin, color=COL_RES))
        self.end()


# ══════════════════════════════════════════════════════════════════════
# PARTE 13: riepilogo
# ══════════════════════════════════════════════════════════════════════
class P13_Riepilogo(LessonScene):
    PART, TITLE = 13, "Riepilogo"

    def construct(self):
        self.title_card()
        items = [
            ("Un angolo è una rotazione; un giro vale 360°.", COL_ANG),
            ("Opposti al vertice: uguali.", WHITE),
            ("Parallele: Z e F uguali, C somma 180°.", COL_AUX),
            ("Triangolo: la somma degli angoli è 180°.", COL_RES),
            ("Altezza: perpendicolare alla sua base.", COL_AUX),
            ("Congruenza: LAL, ALA, LLL (non AAA, non LLA).", COL_GIV),
        ]
        rows = VGroup(*[T("•  " + s, 30, c) for s, c in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(P(0, 0.3))
        texts = [
            "Ricapitoliamo il nostro viaggio. Un angolo è una rotazione, e un giro completo vale trecentosessanta gradi: un numero scelto perché si divide bene.",
            "Gli angoli opposti al vertice sono uguali.",
            "Con le rette parallele, gli angoli a zeta e a effe sono uguali, e quelli a ci sommano centottanta.",
            "Per questo la somma degli angoli di un triangolo è sempre centottanta gradi.",
            "L'altezza cade sempre ad angolo retto sulla sua base, anche quando bisogna prolungare il lato.",
            "E due triangoli sono congruenti con tre dati giusti: LAL, ALA oppure LLL. Non bastano tre angoli, e non basta LLA.",
        ]
        for row, txt in zip(rows, texts):
            with self.say(txt):
                self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.9)
        self.wipe()
        O, L = P(-2.4, -1.7), 4.2
        th = ValueTracker(0)
        d = door(self, O, L, th)
        with self.say("Torniamo alla porta dell'inizio. Adesso sai che cosa misura davvero un angolo: la rotazione, non la lunghezza dei lati."):
            self.play(FadeIn(d))
            self.play(th.animate.set_value(100), run_time=2.5)
        self.wipe()
        q1 = T("«Non esiste una via regia per la geometria.»", 36, WHITE).move_to(P(0, 1.2))
        q2 = T("Euclide, secondo Proclo", 26, GRAY_B).next_to(q1, DOWN, buff=0.3)
        bye = T("Buono studio!", 54, COL_ANG, weight=BOLD).move_to(P(0, -1.2))
        with self.say("Euclide diceva: non esiste una via regia per la geometria. Ma un disegno alla volta, la strada diventa facile."):
            self.play(Write(q1), run_time=2.0)
            self.play(FadeIn(q2))
        with self.say("Buono studio!"):
            self.play(Write(bye))
        self.wait(1.0)
        self.end()


# ── sanity checks (python lezione_geometria.py) ─────────────────────────
if __name__ == "__main__":
    ok = True

    def check(name, got, want, tol=1e-6):
        global ok
        good = abs(got - want) <= tol
        ok &= good
        print(("OK  " if good else "BAD ") + f"{name}: {got:.4f} (expected {want})")

    divisors = [d for d in range(1, 361) if 360 % d == 0]
    check("divisors of 360", len(divisors), 24)
    smallest = min(n for n in range(1, 361) if sum(1 for d in range(1, n + 1) if n % d == 0) >= 24)
    check("smallest number with 24 divisors", smallest, 360)
    check("pie 12/30*360", 12 * 360 / 30, 144)
    check("pie 9/30*360", 9 * 360 / 30, 108)
    check("clock 2:30 hour hand", 2 * 30 + 30 * 0.5, 75)
    check("clock 2:30 angle", 180 - 75, 105)
    check("act 6 P x", P6[0], -0.6 + 2.5 / np.tan(np.radians(65)))
    check("act 6 angle 5", convex(Q6, Q6 + RIGHT, P6)[1], 65)
    check("act 6 tilt 12: angle 3", 65 - 12, 53)
    check("act 7 angle A", convex(A7, B7, C7)[1], 50)
    check("act 7 angle B", convex(B7, A7, C7)[1], 60)
    check("act 7 angle C", convex(C7, A7, B7)[1], 70)
    check("act 10 BC / unit", BC10 / U10, 2.8389, 1e-3)
    check("act 10 angle B", ANG_B10, 46.168, 1e-3)
    check("SSA AC1", T1_SSA, 7.842, 1e-3)
    check("SSA AC2", T2_SSA, 2.550, 1e-3)
    for t in (T1_SSA, T2_SSA):
        Cc = t * unit(30)
        check("SSA |BC| = 4", norm(Cc - P(6, 0)), 4)
    check("3-4-5 altitude", 2 * 6 / 5, 2.4)
    check("act 8 example AC (cm)", norm(C8 - A8) / 0.5, 12)
    check("act 8 example altitude from C (cm)", (C8[1] - A8[1]) / 0.5, 6)
    check("act 8 example altitude to AC (cm)", norm(foot(B8, A8, C8) - B8) / 0.5, 5)
    check("supplementary puzzle", (180 - 40) / 2, 70)
    check("alternate x", (40 - 10) / (3 - 2), 30)
    check("exterior angle", 180 - 60, 50 + 70)
    print("ALL OK" if ok else "SOME CHECKS FAILED")
