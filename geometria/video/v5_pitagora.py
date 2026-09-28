"""
Video 5 · Pitagora, poligoni e cerchio
======================================
Scenes (render each with  manim -qh v5_pitagora.py <Scene>):
  V5_P1_Pitagora    squares on the sides of the 3-4-5 triangle; proof by moving four triangles; the formulas
  V5_P2_Aree        areas by cutting and moving: parallelogram, triangle, trapezium, rhombus
  V5_P3_Problemi    Pythagoras inside polygons: rectangle (G2), rhombus (G4), isosceles trapezium (G5)
  V5_P4_Cerchio     pi by rolling a wheel; the area by slicing the disc into a rectangle; arcs and sectors
  V5_P5_Esercizi    summary and the matching exercises
"""
from comune import *

# ── precomputed geometry (checked in __main__) ─────────────────────────
PA, PB = 3, 4                      # legs of the proof square
NW = 16                            # wedges of the disc
RW = 1.5
TH = 360 / NW
WW = RW * np.sin(np.radians(TH / 2))   # half chord
HW = RW * np.cos(np.radians(TH / 2))   # apothem of a wedge


class V5_P1_Pitagora(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 5, "Pitagora, poligoni e cerchio", 1, "Il teorema di Pitagora"

    def construct(self):
        self.video_card("Pitagora · aree dei poligoni · circonferenza e cerchio",
                        "Ciao! In questo video scopriamo perché il teorema di Pitagora è vero, da dove vengono le formule delle aree, e che cosa è il pi greco.")
        self.header()
        u = 0.48
        O = P(-4.4, -0.25)
        X = O + P(4 * u, 0)
        Y = O + P(0, 3 * u)
        n = P(3 * u, 4 * u)
        tri = poly(O, X, Y, col=WHITE, fill=GRAY_D, op=0.6, w=3)
        sqa = poly(O, Y, Y + P(-3 * u, 0), O + P(-3 * u, 0), col=COL_GIV, fill=COL_GIV, op=0.4)
        sqb = poly(O, X, X + P(0, -4 * u), O + P(0, -4 * u), col=COL_ANG, fill=COL_ANG, op=0.4)
        sqc = poly(X, Y, Y + n, X + n, col=COL_RES, fill=COL_RES, op=0.4)
        la = M("3", 30).next_to(seg(O, Y), RIGHT, buff=0.08)
        lb = M("4", 30).next_to(seg(O, X), UP, buff=0.08)
        lc = M("5", 30).move_to((X + Y) / 2 + P(-0.18, -0.24))
        with self.say("Ecco un triangolo rettangolo con i cateti di tre e quattro e l'ipotenusa di cinque."):
            self.play(DrawBorderThenFill(tri), FadeIn(la), FadeIn(lb), FadeIn(lc), run_time=1.4)
        ta, tb, tc = M("9", 40).move_to(sqa), M("16", 40).move_to(sqb), M("25", 40).move_to(sqc)
        with self.say("Su ogni lato costruisco un quadrato. Quello sul cateto tre ha area nove, quello sul cateto quattro sedici, quello sull'ipotenusa venticinque."):
            self.play(DrawBorderThenFill(sqa), FadeIn(ta))
            self.play(DrawBorderThenFill(sqb), FadeIn(tb))
            self.play(DrawBorderThenFill(sqc), FadeIn(tc))
        eq = VGroup(M(r"9 + 16 = 25", 56), M(r"3^2 + 4^2 = 5^2", 56, COL_RES)).arrange(DOWN, buff=0.4).move_to(P(3.3, 0.6))
        with self.say("Nove più sedici fa venticinque! La somma dei quadrati dei cateti è uguale al quadrato dell'ipotenusa. Questo è il teorema di Pitagora. Ma perché è vero sempre?"):
            self.play(Write(eq[0]))
            self.play(Write(eq[1]))
        self.wipe()

        # proof by rearrangement: big square of side c + C (a = c, b = C in the code)
        a, b = PA, PB
        s = 0.5
        Q = P(-5.6, -2.1)

        def q(x, y):
            return Q + P(x * s, y * s)
        big = Square((a + b) * s, color=WHITE, stroke_width=3).move_to(q((a + b) / 2, (a + b) / 2))
        T1 = poly(q(0, 0), q(a, 0), q(0, b), col=WHITE, fill=COL_GIV, op=0.75, w=2)
        T2 = poly(q(a, 0), q(a + b, 0), q(a + b, a), col=WHITE, fill=COL_GIV, op=0.75, w=2)
        T3 = poly(q(a + b, a + b), q(b, a + b), q(a + b, a), col=WHITE, fill=COL_GIV, op=0.75, w=2)
        T4 = poly(q(b, a + b), q(0, a + b), q(0, b), col=WHITE, fill=COL_GIV, op=0.75, w=2)
        hole = poly(q(a, 0), q(a + b, a), q(b, a + b), q(0, b), col=COL_RES, fill=COL_RES, op=0.35, w=0)
        hc = M("i^2", 44, COL_RES).move_to(hole)
        with self.say("Ecco una dimostrazione che si fa con le mani. Prendo un quadrato grande e dentro metto quattro copie del triangolo, una per angolo."):
            self.play(Create(big))
            self.play(LaggedStart(*[DrawBorderThenFill(t) for t in (T1, T2, T3, T4)], lag_ratio=0.3), run_time=2.0)
        with self.say("Lo spazio che resta libero in mezzo è un quadrato costruito sull'ipotenusa i: la sua area è i al quadrato."):
            self.play(FadeIn(hole), Write(hc))
        with self.say("Adesso sposto i triangoli, senza girarli, solo facendoli scivolare."):
            self.play(FadeOut(hole), FadeOut(hc))
            self.play(T1.animate.shift(P(0, a * s)), T3.animate.shift(P(-b * s, 0)), run_time=1.8)
            self.play(T4.animate.shift(P(a * s, -b * s)), run_time=1.4)
        ha = poly(q(0, 0), q(a, 0), q(a, a), q(0, a), col=COL_GIV, fill=COL_GIV, op=0.35, w=0)
        hb = poly(q(a, a), q(a + b, a), q(a + b, a + b), q(a, a + b), col=COL_ANG, fill=COL_ANG, op=0.35, w=0)
        with self.say("Adesso lo spazio libero sono due quadrati, uno per ogni cateto: c piccolo e C grande. Le loro aree sono c al quadrato e C al quadrato."):
            self.play(FadeIn(ha), FadeIn(hb))
            self.play(Write(M("c^2", 40, COL_GIV).move_to(ha)), Write(M("C^2", 40, COL_ANG).move_to(hb)))
        concl = VGroup(T("Stesso quadrato grande, stessi 4 triangoli:", 26), T("lo spazio libero è lo stesso.", 26),
                       M(r"i^2 = c^2 + C^2", 60, COL_RES)).arrange(DOWN, buff=0.3).move_to(P(3.2, 0.3))
        with self.say("Il quadrato grande è lo stesso e i quattro triangoli sono gli stessi: quindi anche lo spazio libero è uguale. I al quadrato è uguale a c al quadrato più C al quadrato. E vale per ogni triangolo rettangolo."):
            self.play(FadeIn(concl[:2]))
            self.play(Write(concl[2]))
            self.play(Circumscribe(concl[2], color=COL_RES))
        self.wipe()
        fs = VGroup(M(r"i = \sqrt{c^2 + C^2}", 50, COL_RES), M(r"c = \sqrt{i^2 - C^2}", 50, COL_ANG)).arrange(DOWN, buff=0.4).move_to(P(-3.0, 1.0))
        ex = VGroup(M(r"i = \sqrt{9^2 + 12^2} = \sqrt{225} = 15", 40), M(r"c = \sqrt{26^2 - 10^2} = \sqrt{576} = 24", 40)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(P(2.6, 1.0))
        with self.say("Da qui le due formule. Per l'ipotenusa si sommano i quadrati e si fa la radice. Per un cateto si sottrae."):
            self.play(Write(fs[0]))
            self.play(Write(fs[1]))
        with self.say("Esempi: con i cateti nove e dodici l'ipotenusa è quindici. Con ipotenusa ventisei e un cateto dieci, l'altro cateto è ventiquattro."):
            self.play(Write(ex[0]))
            self.play(Write(ex[1]))
        trap = T("Trappola: per un cateto si SOTTRAE, non si somma!", 28, COL_ERR).move_to(P(0, -1.3))
        with self.say("L'errore più comune è sommare anche quando si cerca un cateto. L'ipotenusa è il lato più lungo: se sommi, il cateto verrebbe più lungo dell'ipotenusa, ed è impossibile."):
            self.play(FadeIn(trap))
        self.end()


class V5_P2_Aree(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 5, "Pitagora, poligoni e cerchio", 2, "Le aree tagliando e spostando"

    def construct(self):
        self.title_card()
        s = 0.72
        o = P(-5.6, -1.2)

        def g(x, y):
            return o + P(x * s, y * s)
        rect = unit_squares(3, 5, s, o, COL_GIV, 0.3)
        with self.say("L'area è quanti quadretti servono per coprire una figura. Un rettangolo di base cinque e altezza tre contiene cinque per tre, quindici quadretti: base per altezza."):
            self.play(FadeIn(rect, lag_ratio=0.05), run_time=1.2)
            self.play(Write(M(r"A = b\cdot h = 15", 44, COL_GIV).move_to(P(2.8, 1.8))))
        self.wipe()
        # parallelogram -> rectangle
        rest = poly(g(1.2, 0), g(4, 0), g(5.2, 2.5), g(1.2, 2.5), col=WHITE, fill=COL_ANG, op=0.3)
        cut = poly(g(0, 0), g(1.2, 0), g(1.2, 2.5), col=WHITE, fill=COL_ANG, op=0.3)
        hl = DashedLine(g(1.2, 0), g(1.2, 2.5), color=WHITE)
        lb = M("b", 36).next_to(seg(g(0, 0), g(4, 0)), DOWN, buff=0.12)
        lh = M("h", 36).next_to(hl, RIGHT, buff=0.1)
        with self.say("Un parallelogramma. Taglio il triangolo a sinistra lungo l'altezza..."):
            self.play(DrawBorderThenFill(VGroup(rest, cut)), FadeIn(lb))
            self.play(Create(hl), FadeIn(lh), cut.animate.set_fill(COL_ERR, 0.55))
        with self.say("e lo sposto a destra. Diventa un rettangolo con la stessa base e la stessa altezza: area base per altezza."):
            self.play(cut.animate.shift(P(4 * s, 0)), lb.animate.shift(P(1.2 * s, 0)), run_time=1.6)
            self.play(Write(M(r"A = b\cdot h", 48, COL_ANG).move_to(P(3.2, 1.2))))
        self.wipe()
        # triangle = half a parallelogram
        tA, tB, tC = g(0, 0), g(4, 0), g(1.2, 2.5)
        t1 = poly(tA, tB, tC, col=WHITE, fill=COL_GIV, op=0.45)
        t2 = t1.copy().set_fill(COL_RES, 0.45)
        with self.say("Un triangolo. Ne faccio una copia e la giro di mezzo giro."):
            self.play(DrawBorderThenFill(t1))
            self.play(Rotate(t2, angle=PI, about_point=(tB + tC) / 2), run_time=1.6)
        with self.say("Insieme formano un parallelogramma, di area base per altezza. Il triangolo è la metà: base per altezza diviso due."):
            self.play(Indicate(VGroup(t1, t2), scale_factor=1.03))
            self.play(Write(M(r"A = \frac{b\cdot h}{2}", 52, COL_GIV).move_to(P(3.2, 1.2))))
        self.wipe()
        # trapezium: two copies make a parallelogram of base B + b
        z = [g(0, 0), g(5, 0), g(3.5, 2), g(1.5, 2)]
        tz = poly(*z, col=WHITE, fill=COL_AUX, op=0.45)
        tz2 = tz.copy().set_fill(COL_ANG2, 0.45)
        piv = (z[1] + z[2]) / 2
        lB = M("B", 34).next_to(seg(z[0], z[1]), DOWN, buff=0.1)
        lsb = M("b", 34).next_to(seg(z[3], z[2]), UP, buff=0.1)
        with self.say("Un trapezio, con base maggiore B e base minore b. Faccio una copia e la giro di mezzo giro attorno a un lato obliquo."):
            self.play(DrawBorderThenFill(tz), FadeIn(lB), FadeIn(lsb))
            self.play(Rotate(tz2, angle=PI, about_point=piv), run_time=1.6)
        br = Brace(Line(z[0], g(7, 0)), DOWN, buff=0.45)
        brl = M("B + b", 34).next_to(br, DOWN, buff=0.1)
        with self.say("Ottengo un parallelogramma con base B più b. Il trapezio è la metà: B più b, per h, diviso due."):
            self.play(GrowFromCenter(br), FadeIn(brl))
            self.play(Write(M(r"A = \frac{(B+b)\cdot h}{2}", 50, COL_AUX).move_to(P(3.4, 1.6))))
        self.wipe()
        # rhombus: half of the rectangle of its diagonals
        c = g(2.5, 1.2)
        L, R_, Tt, Bt = c + P(-2.0, 0), c + P(2.0, 0), c + P(0, 1.2), c + P(0, -1.2)
        box = Rectangle(width=4.0, height=2.4, color=GRAY_B, stroke_width=2).move_to(c)
        rh = poly(L, Tt, R_, Bt, col=WHITE, fill=COL_RES, op=0.5)
        diags = VGroup(DashedLine(L, R_, color=WHITE), DashedLine(Tt, Bt, color=WHITE))
        with self.say("Infine il rombo. Lo metto dentro un rettangolo che ha per lati le sue due diagonali, D e d."):
            self.play(DrawBorderThenFill(rh), Create(diags))
            self.play(Create(box))
            self.play(FadeIn(M("D", 34).next_to(box, DOWN, buff=0.1)), FadeIn(M("d", 34).next_to(box, LEFT, buff=0.1)))
        with self.say("I quattro triangoli fuori dal rombo sono uguali ai quattro triangoli dentro. Il rombo è metà del rettangolo: D per d diviso due."):
            corners = VGroup(poly(L, Tt, c + P(-2.0, 1.2), col=WHITE, fill=GRAY_B, op=0.3, w=1), poly(Tt, R_, c + P(2.0, 1.2), col=WHITE, fill=GRAY_B, op=0.3, w=1),
                             poly(R_, Bt, c + P(2.0, -1.2), col=WHITE, fill=GRAY_B, op=0.3, w=1), poly(Bt, L, c + P(-2.0, -1.2), col=WHITE, fill=GRAY_B, op=0.3, w=1))
            self.play(FadeIn(corners))
            self.play(Write(M(r"A = \frac{D\cdot d}{2}", 52, COL_RES).move_to(P(3.4, 1.2))))
        self.end()


class V5_P3_Problemi(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 5, "Pitagora, poligoni e cerchio", 3, "Pitagora nei poligoni"

    def construct(self):
        self.title_card()
        s = 0.16
        o = P(-6.0, -1.0)
        r = Rectangle(width=24 * s, height=7 * s, color=WHITE, stroke_width=3).set_fill(COL_GIV, 0.2).move_to(o, aligned_edge=DL)
        dg = Line(o, o + P(24 * s, 7 * s), color=COL_ANG, stroke_width=4)
        with self.say("Il segreto: in molti poligoni si nasconde un triangolo rettangolo. Un rettangolo ha la base di ventiquattro e la diagonale di venticinque. La diagonale lo divide in due triangoli rettangoli."):
            self.play(Create(r), FadeIn(M("24", 30).next_to(r, DOWN, buff=0.1)))
            self.play(Create(dg), FadeIn(M("25", 30, COL_ANG).move_to(dg.get_center() + P(-0.2, 0.3))))
        s1 = VGroup(M(r"h = \sqrt{25^2 - 24^2} = \sqrt{49} = 7", 38), M(r"A = 24\cdot 7 = 168", 38, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(P(3.0, 1.9))
        with self.say("L'altezza è un cateto: radice di venticinque al quadrato meno ventiquattro al quadrato, sette. Area centosessantotto."):
            self.play(Write(s1[0]))
            self.play(Write(s1[1]), FadeIn(M("7", 30, COL_RES).next_to(r, LEFT, buff=0.1)))
        self.wipe()
        c = P(-3.6, 0.4)
        k = 0.1
        L, R_, Tt, Bt = c + P(-15 * k, 0), c + P(15 * k, 0), c + P(0, 8 * k), c + P(0, -8 * k)
        rh = poly(L, Tt, R_, Bt, col=WHITE, fill=COL_RES, op=0.25)
        tq = poly(c, R_, Tt, col=COL_ANG, fill=COL_ANG, op=0.5, w=3)
        with self.say("Un rombo con le diagonali di sedici e trenta. Le diagonali si tagliano a metà ad angolo retto: il lato è l'ipotenusa di un triangolo con cateti otto e quindici."):
            self.play(DrawBorderThenFill(rh), Create(VGroup(DashedLine(L, R_), DashedLine(Tt, Bt))))
            self.play(FadeIn(tq), FadeIn(M("15", 26).next_to(seg(c, R_), DOWN, buff=0.08)), FadeIn(M("8", 26).next_to(seg(c, Tt), LEFT, buff=0.08)))
        s2 = VGroup(M(r"\ell = \sqrt{8^2 + 15^2} = \sqrt{289} = 17", 38), M(r"A = \frac{16\cdot 30}{2} = 240", 38, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(P(2.8, 1.2))
        with self.say("Il lato è radice di sessantaquattro più duecentoventicinque, radice di duecentottantanove, diciassette. L'area è sedici per trenta diviso due, duecentoquaranta."):
            self.play(Write(s2[0]))
            self.play(Write(s2[1]))
        self.wipe()
        k = 0.24
        o = P(-6.0, -1.2)
        A_, B_, C_, D_ = o, o + P(22 * k, 0), o + P(16 * k, 8 * k), o + P(6 * k, 8 * k)
        H_ = o + P(6 * k, 0)
        tz = poly(A_, B_, C_, D_, col=WHITE, fill=COL_AUX, op=0.25)
        tri = poly(A_, H_, D_, col=COL_ANG, fill=COL_ANG, op=0.5, w=3)
        with self.say("Un trapezio isoscele con le basi di ventidue e dieci e il lato obliquo di dieci. Traccio l'altezza: stacca un triangolo rettangolo."):
            self.play(DrawBorderThenFill(tz), FadeIn(M("22", 28).next_to(seg(A_, B_), DOWN, buff=0.1)), FadeIn(M("10", 28).next_to(seg(D_, C_), UP, buff=0.1)))
            self.play(Create(DashedLine(D_, H_)), FadeIn(tri), FadeIn(M("10", 26, COL_ANG).move_to((A_ + D_) / 2 + P(-0.3, 0.1))))
        s3 = VGroup(M(r"\overline{AH} = \frac{22 - 10}{2} = 6", 38), M(r"h = \sqrt{10^2 - 6^2} = 8", 38),
                    M(r"A = \frac{(22 + 10)\cdot 8}{2} = 128", 38, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(P(3.0, 1.2))
        with self.say("La base piccola del triangolo è metà della differenza delle basi: ventidue meno dieci, diviso due, sei. L'altezza è radice di cento meno trentasei, otto. Area centoventotto."):
            self.play(Write(s3[0]))
            self.play(Write(s3[1]))
            self.play(Write(s3[2]))
        self.end()


class V5_P4_Cerchio(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 5, "Pitagora, poligoni e cerchio", 4, "Circonferenza e cerchio"

    def construct(self):
        self.title_card()
        d = 2.3
        r = d / 2
        x0 = -5.9
        yb = -1.5
        ground = Line(P(x0 - 0.4, yb), P(x0 + 3.5 * d, yb), color=GRAY_B, stroke_width=2)
        ticks = VGroup(*[VGroup(Line(P(x0 + k * d, yb - 0.1), P(x0 + k * d, yb + 0.1), color=GRAY_B),
                                M(str(k), 26, GRAY_B).next_to(P(x0 + k * d, yb), DOWN, buff=0.15)) for k in range(4)])
        t = ValueTracker(0)

        def wheel():
            cx = x0 + t.get_value() * PI * d
            ang = -2 * PI * t.get_value()
            c = P(cx, yb + r)
            circ = Circle(radius=r, color=COL_GIV, stroke_width=4).move_to(c)
            mark = Dot(c + r * np.array([np.sin(ang), -np.cos(ang), 0]), radius=0.1, color=COL_ERR)
            spoke = Line(c, c + r * np.array([np.sin(ang), -np.cos(ang), 0]), color=COL_GIV, stroke_width=2)
            return VGroup(circ, spoke, mark)
        w = always_redraw(wheel)
        trace = always_redraw(lambda: Line(P(x0, yb), P(x0 + t.get_value() * PI * d + 1e-4, yb), color=COL_ERR, stroke_width=6))
        with self.say("Che cos'è il pi greco? Prendo una ruota con il diametro lungo uno, e segno un punto rosso dove tocca terra."):
            self.play(Create(ground), FadeIn(ticks), FadeIn(w))
        with self.say("Adesso la faccio rotolare per un giro completo. Il pezzo di strada percorso è lungo esattamente come la circonferenza."):
            self.add(trace)
            self.play(t.animate.set_value(1), run_time=4, rate_func=linear)
        pi_l = M(r"\pi \approx 3{,}14", 54, COL_ERR).move_to(P(x0 + PI * d / 2 - 0.6, 1.1))
        with self.say("Il giro misura poco più di tre diametri: tre virgola uno quattro. Questo numero si chiama pi greco. La circonferenza è sempre pi greco volte il diametro."):
            self.play(Write(pi_l))
        f = VGroup(M(r"C = \pi\cdot d = 2\pi r", 50, COL_GIV), M(r"\text{ruota: } d = 70\ \text{cm}", 38),
                   M(r"C = 3{,}14\cdot 70 = 219{,}8\ \text{cm}", 38)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P(4.2, 2.3))
        with self.say("Per una ruota di bicicletta di settanta centimetri: tre virgola uno quattro per settanta, duecentodiciannove virgola otto centimetri a ogni giro."):
            self.play(Write(f[0]))
            self.play(Write(f[1]), Write(f[2]))
        self.remove(w, trace)
        self.wipe()

        # area: slice and rearrange
        C0 = P(-3.6, 0.5)
        cols = [COL_GIV, COL_ANG]
        wedges = VGroup(*[wedge(C0, i * TH, TH, RW, cols[i % 2], 0.8) for i in range(NW)])
        rr = Line(C0, C0 + RW * RIGHT, color=WHITE, stroke_width=3)
        with self.say("E l'area del cerchio? Taglio il cerchio di raggio r in sedici fette, come una pizza."):
            self.play(FadeIn(wedges, lag_ratio=0.05), Create(rr), FadeIn(M("r", 32).next_to(rr, UP, buff=0.05)), run_time=1.6)
        self.play(FadeOut(rr), *[FadeOut(m) for m in self.mobjects if isinstance(m, MathTex)])
        xs, yb2 = 0.4, -1.1
        rots, shifts = [], []
        for i in range(NW):
            beta = i * TH + TH / 2
            tip0 = C0 + 0.35 * unit(beta)
            if i % 2 == 0:
                tgt, tau = P(xs + i * WW, yb2), 90
            else:
                tgt, tau = P(xs + i * WW, yb2 + HW), 270
            rots.append((tau - beta, tip0))
            shifts.append(tgt - tip0)
        with self.say("Separo le fette e le metto in fila, una con la punta in giù e una con la punta in su."):
            self.play(*[wedges[i].animate.shift(0.35 * unit(i * TH + TH / 2)) for i in range(NW)], run_time=0.8)
            self.play(*[Rotate(wedges[i], angle=np.radians(rots[i][0]), about_point=rots[i][1]) for i in range(NW)], run_time=1.4)
            self.play(*[wedges[i].animate.shift(shifts[i]) for i in range(NW)], run_time=1.8)
        top = Brace(Line(P(xs, yb2 + HW), P(xs + NW * WW, yb2 + HW)), UP, buff=0.1)
        side = Brace(Line(P(xs, yb2), P(xs, yb2 + HW)), LEFT, buff=0.1)
        with self.say("Viene quasi un rettangolo. La base è metà circonferenza, cioè pi greco per r. L'altezza è il raggio r. Più fette faccio, più diventa un rettangolo perfetto."):
            self.play(GrowFromCenter(top), FadeIn(M(r"\pi r", 36).next_to(top, UP, buff=0.1)))
            self.play(GrowFromCenter(side), FadeIn(M("r", 36).next_to(side, LEFT, buff=0.1)))
        area = M(r"A = \pi r\cdot r = \pi r^2", 56, COL_RES).move_to(P(2.6, 2.1))
        with self.say("Area del rettangolo: pi greco r per r. L'area del cerchio è pi greco r al quadrato."):
            self.play(Write(area))
            self.play(Circumscribe(area, color=COL_RES))
        self.wipe()

        # arcs and sectors: the same fraction as a pie chart
        Cc = P(-3.6, 0.3)
        disc = Circle(radius=1.7, color=WHITE, stroke_width=3).move_to(Cc)
        sec = wedge(Cc, 90, 72, 1.7, COL_ANG, 0.7)
        arc = Arc(radius=1.7, start_angle=np.radians(90), angle=np.radians(72), arc_center=Cc, color=COL_ERR, stroke_width=8)
        with self.say("Un arco e un settore sono una parte di circonferenza e di cerchio. Un angolo di settantadue gradi è un quinto di trecentosessanta: arco e settore sono un quinto del totale."):
            self.play(Create(disc))
            self.play(FadeIn(sec), Create(arc))
        rows = VGroup(M(r"r = 5:\quad C = 31{,}4 \qquad A = 78{,}5", 38),
                      M(r"\frac{72^\circ}{360^\circ} = \frac15", 40, COL_ANG),
                      M(r"\text{arco} = \frac{31{,}4}{5} = 6{,}28", 38, COL_ERR),
                      M(r"\text{settore} = \frac{78{,}5}{5} = 15{,}7", 38, COL_ANG)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P(2.6, 0.4))
        with self.say("Con raggio cinque la circonferenza è trentuno virgola quattro e il cerchio settantotto virgola cinque. L'arco è un quinto, sei virgola ventotto; il settore quindici virgola sette. È la stessa idea dell'areogramma!"):
            self.play(LaggedStart(*[Write(x) for x in rows], lag_ratio=0.5), run_time=3.4)
        self.end()


class V5_P5_Esercizi(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 5, "Pitagora, poligoni e cerchio", 5, "Riepilogo ed esercizi"

    def construct(self):
        self.header()
        items = [(r"i^2 = c^2 + C^2", COL_RES),
                 (r"\text{parallelogramma } b\cdot h \quad \text{triangolo } \tfrac{b\cdot h}{2} \quad \text{trapezio } \tfrac{(B+b)\cdot h}{2} \quad \text{rombo } \tfrac{D\cdot d}{2}", COL_ANG),
                 (r"C = 2\pi r \qquad A = \pi r^2", COL_GIV),
                 (r"\text{arco e settore: frazione } \tfrac{\alpha}{360^\circ}", COL_ERR)]
        col = lines_column(items, 36, 0.5).move_to(P(0, 0.4))
        with self.say("Ricapitoliamo. Il teorema di Pitagora. Le aree dei poligoni, che vengono tutte dal rettangolo tagliando e spostando. La circonferenza, due pi greco r, e il cerchio, pi greco r al quadrato."):
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in col], lag_ratio=0.5), run_time=4)
        self.wait(0.6)
        self.wipe(keep_header=False)
        self.exercises([("G1", COL_GIV), ("G2", COL_GIV), ("G3", COL_GIV), ("G4", COL_ANG), ("G5", COL_ANG), ("G6", COL_ERR)],
                       "Adesso tocca a te. Nel file degli esercizi fai la sezione nove, da G uno a G sei.",
                       ["• Cerca sempre il triangolo rettangolo nascosto", "• Usa π = 3,14", "• Controlla con il file delle soluzioni"])


if __name__ == "__main__":
    from math import sqrt, pi
    ok = True

    def check(name, got, want, tol=1e-9):
        global ok
        good = abs(got - want) < tol
        ok &= good
        print(("OK  " if good else "BAD ") + f"{name}: {got} (expected {want})")
    check("3-4-5", 3**2 + 4**2, 5**2)
    a, b = PA, PB
    check("big square = 4 triangles + c^2", (a + b) ** 2, 4 * a * b / 2 + 25)
    check("big square = 4 triangles + a^2 + b^2", (a + b) ** 2, 4 * a * b / 2 + a * a + b * b)
    check("9-12", sqrt(81 + 144), 15)
    check("26-10", sqrt(26**2 - 10**2), 24)
    check("rect h", sqrt(25**2 - 24**2), 7)
    check("rhombus side", sqrt(64 + 225), 17)
    check("rhombus area", 16 * 30 / 2, 240)
    check("trap h", sqrt(100 - 36), 8)
    check("trap area", 32 * 8 / 2, 128)
    check("pi ~", round(pi, 2), 3.14)
    check("wheel", 3.14 * 70, 219.8)
    check("wedges width vs pi r", NW * WW, pi * RW, tol=0.04)
    check("wedge height vs r", HW, RW, tol=0.03)
    check("C r=5", 2 * 3.14 * 5, 31.4)
    check("A r=5", 3.14 * 25, 78.5)
    check("arc 72", 31.4 / 5, 6.28)
    check("sector 72", 78.5 / 5, 15.7)
    print("ALL OK" if ok else "SOME CHECKS FAILED")
