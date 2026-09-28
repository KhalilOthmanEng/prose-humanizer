"""
Video 4 · Il piano cartesiano
=============================
Scenes (render each with  manim -qh v4_cartesiano.py <Scene>):
  V4_P1_Coordinate    a point needs two numbers: walk along x, then climb along y; quadrants; the rectangle of C1
  V4_P2_Distanza      the distance between two points is a hypotenuse: the triangle of C2
  V4_P3_Retta         the line y = 2x - 1 from a table; slope m as a staircase, q where it cuts the y axis
  V4_P4_Intersezione  two lines meet where they have the same y; a point on a line; the triangle of C4
  V4_P5_Taxi          two taxi fares: where the graphs cross, which is cheaper, direct proportion (X3)
  V4_P6_Esercizi      summary and the matching exercises
"""
from comune import *


def plane(xr, yr, u, center):
    pl = NumberPlane(x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 1],
                     x_length=u * (xr[1] - xr[0]), y_length=u * (yr[1] - yr[0]),
                     background_line_style={"stroke_color": GRAY_D, "stroke_width": 1, "stroke_opacity": 0.6},
                     axis_config={"stroke_color": GRAY_B, "stroke_width": 2})
    pl.move_to(center)
    nums = VGroup(*[M(str(k), 20, GRAY_B).next_to(pl.c2p(k, 0), DOWN, buff=0.08) for k in range(xr[0], xr[1] + 1) if k != 0],
                  *[M(str(k), 20, GRAY_B).next_to(pl.c2p(0, k), LEFT, buff=0.08) for k in range(yr[0], yr[1] + 1) if k != 0])
    xl = M("x", 30).next_to(pl.c2p(xr[1], 0), RIGHT, buff=0.1)
    yl = M("y", 30).next_to(pl.c2p(0, yr[1]), UP, buff=0.1)
    return pl, VGroup(nums, xl, yl)


class V4_P1_Coordinate(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 4, "Il piano cartesiano", 1, "Le coordinate"

    def construct(self):
        self.video_card("coordinate · distanza · retta · intersezione",
                        "Ciao! In questo video impariamo a muoverci nel piano cartesiano: le coordinate di un punto, la distanza tra due punti, le rette e dove si incontrano.")
        self.header()
        pl, lab = plane((-4, 8), (-3, 6), 0.52, P(-2.6, 0.1))
        with self.say("Il piano cartesiano è come la battaglia navale: per trovare un punto servono due numeri. Due rette perpendicolari, gli assi, si incontrano nell'origine."):
            self.play(Create(pl), run_time=1.6)
            self.play(FadeIn(lab))
        O = pl.c2p(0, 0)
        walk = Arrow(O, pl.c2p(3, 0), buff=0, color=COL_GIV, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        climb = Arrow(pl.c2p(3, 0), pl.c2p(3, 2), buff=0, color=COL_ANG, stroke_width=6, max_tip_length_to_length_ratio=0.2)
        A = Dot(pl.c2p(3, 2), radius=0.1, color=WHITE)
        la = M(r"A(3;\,2)", 36).next_to(A, UR, buff=0.08)
        rule = VGroup(T("prima x: cammina in orizzontale", 26, COL_GIV), T("poi y: sali o scendi", 26, COL_ANG)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(P(4.3, 1.8))
        with self.say("Il punto A ha coordinate tre e due. Il primo numero è la x: parto dall'origine e cammino di tre verso destra. Il secondo è la y: salgo di due."):
            self.play(GrowArrow(walk), FadeIn(rule[0]))
            self.play(GrowArrow(climb), FadeIn(rule[1]))
            self.play(FadeIn(A, scale=2), Write(la))
        w2 = Arrow(O, pl.c2p(-2, 0), buff=0, color=COL_GIV, stroke_width=6, max_tip_length_to_length_ratio=0.2)
        c2 = Arrow(pl.c2p(-2, 0), pl.c2p(-2, -1), buff=0, color=COL_ANG, stroke_width=6, max_tip_length_to_length_ratio=0.35)
        B = Dot(pl.c2p(-2, -1), radius=0.1, color=WHITE)
        lb = M(r"B(-2;\,-1)", 36).next_to(B, DL, buff=0.08)
        with self.say("I numeri negativi dicono di andare nell'altro verso. B, meno due e meno uno: due passi a sinistra e uno in giù."):
            self.play(GrowArrow(w2))
            self.play(GrowArrow(c2))
            self.play(FadeIn(B, scale=2), Write(lb))
        trap = VGroup(T("Trappola:", 26, COL_ERR), M(r"(3;\,2)\neq(2;\,3)", 36, COL_ERR)).arrange(RIGHT, buff=0.2).move_to(P(4.3, 0.3))
        wrong = Dot(pl.c2p(2, 3), radius=0.1, color=COL_ERR)
        with self.say("Attenzione: l'ordine conta. Tre e due non è lo stesso punto di due e tre."):
            self.play(FadeIn(trap), FadeIn(wrong, scale=2))
        self.wipe()

        pl, lab = plane((-1, 8), (-1, 6), 0.55, P(-2.6, 0.2))
        self.play(FadeIn(pl), FadeIn(lab), run_time=0.6)
        pts = {"A": (1, 1), "B": (7, 1), "C": (7, 5), "D": (1, 5)}
        dots = VGroup(*[Dot(pl.c2p(*v), radius=0.09) for v in pts.values()])
        names = VGroup(*[M(f"{k}({v[0]};{v[1]})", 28).next_to(pl.c2p(*v), d, buff=0.1)
                         for (k, v), d in zip(pts.items(), [DL, DR, UR, UL])])
        rect = Polygon(*[pl.c2p(*v) for v in pts.values()], color=COL_GIV, stroke_width=4).set_fill(COL_GIV, 0.2)
        with self.say("Esercizio C uno. Disegno A uno uno, B sette uno, C sette cinque, D uno cinque, e li unisco: è un rettangolo."):
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.3), FadeIn(names), run_time=1.6)
            self.play(Create(rect))
        calc = VGroup(M(r"\overline{AB} = 7 - 1 = 6", 38), M(r"\overline{BC} = 5 - 1 = 4", 38),
                      M(r"2p = 2(6+4) = 20", 38, COL_RES), M(r"A = 6\cdot 4 = 24", 38, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(P(4.3, 1.0))
        with self.say("A e B hanno la stessa y: il lato è orizzontale e la sua lunghezza è la differenza delle x, sei. B e C hanno la stessa x: il lato è verticale, lungo quattro."):
            self.play(Write(calc[0]))
            self.play(Write(calc[1]))
        with self.say("Perimetro venti, area ventiquattro. E la diagonale? Per quella serve Pitagora: lo vediamo subito."):
            self.play(Write(calc[2]), Write(calc[3]))
        self.end()


class V4_P2_Distanza(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 4, "Il piano cartesiano", 2, "La distanza tra due punti"

    def construct(self):
        self.title_card()
        pl, lab = plane((-3, 5), (-2, 4), 0.62, P(-2.6, 0.2))
        self.play(FadeIn(pl), FadeIn(lab), run_time=0.6)
        A, B, C = (-2, -1), (4, -1), (1, 3)
        dA, dB, dC = [Dot(pl.c2p(*v), radius=0.09) for v in (A, B, C)]
        nA = M(r"A(-2;\,-1)", 28).next_to(dA, DL, buff=0.08)
        nB = M(r"B(4;\,-1)", 28).next_to(dB, DR, buff=0.08)
        nC = M(r"C(1;\,3)", 28).next_to(dC, UP, buff=0.12)
        ac = Line(pl.c2p(*A), pl.c2p(*C), color=COL_ANG, stroke_width=5)
        with self.say("Quanto è lungo il segmento da A a C? È obliquo, non posso contare i quadretti."):
            self.play(FadeIn(dA), FadeIn(dC), Write(nA), Write(nC))
            self.play(Create(ac))
        H = (1, -1)
        hor = Line(pl.c2p(*A), pl.c2p(*H), color=COL_GIV, stroke_width=5)
        ver = Line(pl.c2p(*H), pl.c2p(*C), color=COL_AUX, stroke_width=5)
        l3 = M("3", 34, COL_GIV).next_to(hor, DOWN, buff=0.12)
        l4 = M("4", 34, COL_AUX).next_to(ver, RIGHT, buff=0.12)
        ra = rmark(pl.c2p(*H), pl.c2p(*A), pl.c2p(*C), 0.2)
        with self.say("Ma posso costruire un triangolo rettangolo: cammino in orizzontale da A fino sotto C, tre quadretti, e poi salgo, quattro quadretti. Il segmento A C è l'ipotenusa."):
            self.play(Create(hor), Write(l3))
            self.play(Create(ver), Write(l4), Create(ra))
        f = VGroup(M(r"\overline{AC} = \sqrt{3^2 + 4^2}", 42), M(r"= \sqrt{9 + 16} = \sqrt{25} = 5", 42, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P(3.6, 1.8))
        with self.say("Per il teorema di Pitagora: radice di tre al quadrato più quattro al quadrato, radice di venticinque, cinque."):
            self.play(Write(f[0]))
            self.play(Write(f[1]))
        gen = M(r"d = \sqrt{(x_B - x_A)^2 + (y_B - y_A)^2}", 36, COL_ANG).move_to(P(3.6, 0.3))
        with self.say("In generale, la distanza è la radice della differenza delle x al quadrato più la differenza delle y al quadrato."):
            self.play(Write(gen))
        tri = Polygon(pl.c2p(*A), pl.c2p(*B), pl.c2p(*C), color=WHITE, stroke_width=3).set_fill(COL_GIV, 0.15)
        res = VGroup(M(r"\overline{AB} = 6,\quad \overline{AC} = \overline{BC} = 5", 34), T("isoscele", 28, COL_RES),
                     M(r"2p = 16 \qquad A = \frac{6\cdot 4}{2} = 12", 34, COL_RES)).arrange(DOWN, buff=0.25).move_to(P(3.6, -1.2))
        with self.say("Con B, quattro meno uno, si forma il triangolo dell'esercizio C due. Anche B C è lungo cinque, per lo stesso motivo: il triangolo è isoscele. Perimetro sedici, area dodici."):
            self.play(FadeIn(dB), Write(nB), FadeIn(tri))
            self.play(FadeIn(res, lag_ratio=0.3), run_time=1.6)
        self.end()


class V4_P3_Retta(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 4, "Il piano cartesiano", 3, "La retta y = mx + q"

    def construct(self):
        self.title_card()
        pl, lab = plane((-2, 5), (-2, 7), 0.55, P(-3.0, 0.3))
        self.play(FadeIn(pl), FadeIn(lab), run_time=0.6)
        tab = VGroup(*[M(s, 34) for s in (r"x", r"0", r"1", r"2", r"3")]).arrange(RIGHT, buff=0.5)
        tab2 = VGroup(*[M(s, 34, COL_ANG) for s in (r"y", r"-1", r"1", r"3", r"5")])
        for a, b in zip(tab, tab2):
            b.next_to(a, DOWN, buff=0.35)
        tabg = VGroup(tab, tab2).move_to(P(3.4, 2.2))
        eq = M(r"y = 2x - 1", 48, COL_GIV).next_to(tabg, DOWN, buff=0.4)
        with self.say("Una funzione collega ogni x a una y. Prendiamo y uguale due x meno uno, e facciamo una tabella: per x uguale zero, y vale meno uno; per uno, uno; per due, tre; per tre, cinque."):
            self.play(Write(eq))
            self.play(FadeIn(tab))
            self.play(LaggedStart(*[FadeIn(t) for t in tab2], lag_ratio=0.3), run_time=1.6)
        dots = VGroup(*[Dot(pl.c2p(x, 2 * x - 1), radius=0.09, color=COL_ANG) for x in range(4)])
        with self.say("Disegno i punti. Guarda: sono tutti allineati."):
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.3), run_time=1.4)
        line = Line(pl.c2p(-0.5, -2), pl.c2p(4, 7), color=COL_GIV, stroke_width=4)
        with self.say("Li unisco: è una retta. Ogni funzione come y uguale m x più q ha per grafico una retta."):
            self.play(Create(line), run_time=1.4)
        steps = VGroup()
        for x in range(3):
            steps.add(Line(pl.c2p(x, 2 * x - 1), pl.c2p(x + 1, 2 * x - 1), color=COL_RES, stroke_width=5),
                      Line(pl.c2p(x + 1, 2 * x - 1), pl.c2p(x + 1, 2 * x + 1), color=COL_RES, stroke_width=5))
        mtxt = VGroup(M(r"m = 2", 44, COL_RES), T("1 a destra, 2 in su", 26, COL_RES)).arrange(DOWN, buff=0.15).move_to(P(3.4, -0.4))
        with self.say("Il numero m davanti alla x si chiama coefficiente angolare: dice quanto è ripida la retta. Qui m è due: ogni passo a destra, la retta sale di due. È una scala."):
            self.play(Create(steps, lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(mtxt))
        qdot = Dot(pl.c2p(0, -1), radius=0.13, color=COL_AUX)
        qtxt = VGroup(M(r"q = -1", 44, COL_AUX), T("dove taglia l'asse y", 26, COL_AUX)).arrange(DOWN, buff=0.15).move_to(P(3.4, -1.9))
        with self.say("Il numero q è dove la retta taglia l'asse y: qui meno uno. Se q è zero, la retta passa per l'origine: è la proporzionalità diretta."):
            self.play(FadeIn(qdot, scale=2), FadeIn(qtxt))
        self.end()


class V4_P4_Intersezione(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 4, "Il piano cartesiano", 4, "Dove si incontrano due rette"

    def construct(self):
        self.title_card()
        pl, lab = plane((-1, 6), (-2, 8), 0.5, P(-3.2, 0.3))
        self.play(FadeIn(pl), FadeIn(lab), run_time=0.6)
        r = Line(pl.c2p(-0.5, -2), pl.c2p(4.5, 8), color=COL_GIV, stroke_width=4)
        s = Line(pl.c2p(-1, 6), pl.c2p(6, -1), color=COL_ERR, stroke_width=4)
        er = M(r"r:\ y = 2x - 1", 38, COL_GIV).move_to(P(3.3, 2.5))
        es = M(r"s:\ y = -x + 5", 38, COL_ERR).move_to(P(3.3, 1.8))
        with self.say("Esercizio C quattro: due rette, erre, y uguale due x meno uno, ed esse, y uguale meno x più cinque."):
            self.play(Create(r), Write(er))
            self.play(Create(s), Write(es))
        sol = VGroup(M(r"2x - 1 = -x + 5", 38), M(r"3x = 6 \ \Rightarrow\ x = 2", 38), M(r"y = 2\cdot 2 - 1 = 3", 38),
                     M(r"(2;\,3)", 42, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(P(3.3, 0.0))
        I = Dot(pl.c2p(2, 3), radius=0.12, color=COL_RES)
        with self.say("Dove si incontrano? Nel punto in cui hanno la stessa y. Allora metto uguali le due espressioni: due x meno uno uguale meno x più cinque."):
            self.play(Write(sol[0]))
        with self.say("Tre x uguale sei, x uguale due. E y vale due per due meno uno, tre. Il punto d'incontro è due tre."):
            self.play(Write(sol[1]))
            self.play(Write(sol[2]))
            self.play(Write(sol[3]), FadeIn(I, scale=2))
            self.play(Flash(I, color=COL_RES))
        self.wipe()
        self.play(FadeIn(pl), FadeIn(lab), Create(r), Create(s), FadeIn(I), run_time=0.8)
        Pd = Dot(pl.c2p(4, 7), radius=0.1, color=COL_ANG)
        pt = VGroup(M(r"P(4;\,7)", 38, COL_ANG), M(r"r:\ 2\cdot 4 - 1 = 7\ \checkmark", 36, COL_GIV),
                    M(r"s:\ -4 + 5 = 1 \neq 7", 36, COL_ERR)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(P(3.3, 1.8))
        with self.say("Il punto P, quattro sette, sta sulla retta erre? Metto quattro al posto di x: due per quattro meno uno fa sette. Sì! Su esse invece viene uno, non sette: P non sta su esse."):
            self.play(FadeIn(Pd, scale=2), Write(pt[0]))
            self.play(Write(pt[1]))
            self.play(Write(pt[2]))
        tri = Polygon(pl.c2p(0.5, 0), pl.c2p(5, 0), pl.c2p(2, 3), color=COL_ANG, stroke_width=3).set_fill(COL_ANG, 0.3)
        ar = VGroup(M(r"\text{base} = 5 - \tfrac12 = \tfrac92", 34), M(r"\text{altezza} = 3", 34),
                    M(r"A = \frac{\frac92\cdot 3}{2} = \frac{27}{4} = 6{,}75", 36, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(P(3.3, -1.1))
        with self.say("Infine il triangolo tra le due rette e l'asse x. Erre taglia l'asse x in un mezzo, esse in cinque: la base è quattro virgola cinque. L'altezza è la y del punto d'incontro, tre. Area: sei virgola settantacinque."):
            self.play(FadeIn(tri))
            self.play(LaggedStart(*[Write(a) for a in ar], lag_ratio=0.5), run_time=2.4)
        self.end()


class V4_P5_Taxi(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 4, "Il piano cartesiano", 5, "Quale taxi conviene?"

    def construct(self):
        self.title_card()
        q = VGroup(T("Taxi A: 3 € fissi + 1,50 € al km", 28, COL_GIV), T("Taxi B: 2,50 € al km", 28, COL_ERR)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(P(3.4, 2.5))
        with self.say("Un problema dalla simulazione d'esame. Il taxi A costa tre euro fissi più un euro e cinquanta al chilometro. Il taxi B costa due euro e cinquanta al chilometro, senza quota fissa."):
            self.play(FadeIn(q, lag_ratio=0.3))
        f = VGroup(M(r"A:\ y = 1{,}5x + 3", 38, COL_GIV), M(r"B:\ y = 2{,}5x", 38, COL_ERR)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(P(3.4, 1.2))
        with self.say("Scrivo le formule: x sono i chilometri, y il costo. A: y uguale uno virgola cinque x più tre. B: y uguale due virgola cinque x."):
            self.play(Write(f))
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 25, 5], x_length=6.2, y_length=4.6, tips=False,
                  axis_config={"color": GRAY_B, "stroke_width": 2, "include_numbers": True, "font_size": 22}).move_to(P(-3.0, 0.0))
        xl = T("km", 22, GRAY_B).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = T("euro", 22, GRAY_B).next_to(ax.y_axis, UP, buff=0.1)
        gA = ax.plot(lambda x: 1.5 * x + 3, x_range=[0, 10], color=COL_GIV, stroke_width=4)
        gB = ax.plot(lambda x: 2.5 * x, x_range=[0, 10], color=COL_ERR, stroke_width=4)
        with self.say("Disegno i grafici. B parte dall'origine: zero chilometri, zero euro. È una proporzionalità diretta. A parte da tre euro, anche se non ti muovi."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(gB), run_time=1.4)
            self.play(Create(gA), run_time=1.4)
        X = Dot(ax.c2p(3, 7.5), radius=0.11, color=COL_RES)
        c = VGroup(M(r"1{,}5x + 3 = 2{,}5x", 38), M(r"x = 3\ \text{km},\quad y = 7{,}50", 38, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(P(3.4, -0.2))
        with self.say("Le rette si incrociano: lì i due taxi costano uguale. Uno virgola cinque x più tre uguale due virgola cinque x: x uguale tre chilometri, sette euro e cinquanta."):
            self.play(FadeIn(X, scale=2), Flash(X, color=COL_RES))
            self.play(Write(c))
        region = ax.get_area(gB, x_range=[3, 10], bounded_graph=gA, color=COL_GIV, opacity=0.25)
        tip = T("oltre 3 km conviene A", 28, COL_GIV).move_to(P(3.4, -1.5))
        with self.say("Prima dei tre chilometri il grafico di B sta sotto: conviene B. Dopo, sta sotto quello di A: per i viaggi lunghi conviene A."):
            self.play(FadeIn(region))
            self.play(FadeIn(tip))
        d18 = VGroup(DashedLine(ax.c2p(0, 18), ax.c2p(10, 18), color=COL_ANG), DashedLine(ax.c2p(10, 0), ax.c2p(10, 18), color=COL_ANG))
        t18 = M(r"1{,}5x + 3 = 18 \Rightarrow x = 10\ \text{km}", 34, COL_ANG).move_to(P(3.4, -2.2))
        with self.say("E con diciotto euro, quanti chilometri fai con A? Uno virgola cinque x più tre uguale diciotto: x uguale dieci chilometri."):
            self.play(Create(d18))
            self.play(Write(t18))
        self.end()


class V4_P6_Esercizi(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 4, "Il piano cartesiano", 6, "Riepilogo ed esercizi"

    def construct(self):
        self.header()
        items = [(r"P(x;\,y):\ \text{prima orizzontale, poi verticale}", COL_GIV),
                 (r"d = \sqrt{(x_B - x_A)^2 + (y_B - y_A)^2}", COL_ANG),
                 (r"y = mx + q:\ m\ \text{pendenza},\ q\ \text{sull'asse}\ y", COL_RES),
                 (r"\text{incontro: stessa}\ y\ \Rightarrow\ \text{equazione}", COL_ERR)]
        col = lines_column(items, 38, 0.45).move_to(P(0, 0.4))
        with self.say("Ricapitoliamo. Un punto ha due coordinate, prima la x e poi la y. La distanza si trova con Pitagora. La retta y uguale m x più q ha pendenza m e taglia l'asse y in q. E due rette si incontrano dove hanno la stessa y."):
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in col], lag_ratio=0.5), run_time=4)
        self.wait(0.6)
        self.wipe(keep_header=False)
        self.exercises([("C1", COL_GIV), ("C2", COL_ANG), ("C3", COL_ANG), ("C4", COL_ERR), ("X3", COL_ERR)],
                       "Adesso tocca a te. Nel file degli esercizi fai la sezione sei, da C uno a C quattro, e poi il quesito X tre della simulazione.",
                       ["• Usa la carta a quadretti", "• Per le rette fai sempre una tabella", "• Controlla con il file delle soluzioni"])


if __name__ == "__main__":
    from math import hypot
    ok = True

    def check(name, got, want):
        global ok
        good = abs(got - want) < 1e-9
        ok &= good
        print(("OK  " if good else "BAD ") + f"{name}: {got} (expected {want})")
    check("C1 perimetro", 2 * (6 + 4), 20)
    check("C1 area", 6 * 4, 24)
    check("AC", hypot(1 - (-2), 3 - (-1)), 5)
    check("BC", hypot(4 - 1, -1 - 3), 5)
    check("C2 area", 6 * 4 / 2, 12)
    for x in range(4):
        check(f"table x={x}", 2 * x - 1, [-1, 1, 3, 5][x])
    check("intersection x", 6 / 3, 2)
    check("intersection y r", 2 * 2 - 1, 3)
    check("intersection y s", -2 + 5, 3)
    check("P on r", 2 * 4 - 1, 7)
    check("r x-intercept", 0.5, 1 / 2)
    check("triangle area", (5 - 0.5) * 3 / 2, 6.75)
    check("taxi cross x", 3 / (2.5 - 1.5), 3)
    check("taxi cross y", 2.5 * 3, 7.5)
    check("taxi 18", (18 - 3) / 1.5, 10)
    print("ALL OK" if ok else "SOME CHECKS FAILED")
