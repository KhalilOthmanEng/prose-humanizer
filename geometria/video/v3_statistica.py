"""
Video 3 · Statistica e probabilità
==================================
Scenes (render each with  manim -qh v3_statistica.py <Scene>):
  V3_P1_Media        Luca's marks as bars: the mean levels the bars (the total stays 55), median, mode, range
  V3_P2_Areogramma   from a table to a pie chart and back (library books, pupils' grades)
  V3_P3_Probabilita  favourable over possible cases: one die, the 0 to 1 scale, the urn, the complement
  V3_P4_DueDadi      the 6 x 6 table of two dice: sum 7, doubles, sum greater than 10
  V3_P5_Esercizi     summary and the matching exercises
"""
from comune import *

MARKS = [6, 7, 5, 8, 7, 9, 7, 6]
BOOKS = [("gialli", 96), ("fantasy", 60), ("storici", 48), ("biografie", 36)]
PIPS = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)],
        4: [(-1, 1), (1, 1), (-1, -1), (1, -1)], 5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
        6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)]}


def die(n, c, s=0.8, col=WHITE):
    face = RoundedRectangle(width=s, height=s, corner_radius=0.12, color=col, stroke_width=3).set_fill(GRAY_E, 0.6).move_to(c)
    dots = VGroup(*[Dot(c + P(dx * s * 0.27, dy * s * 0.27), radius=s * 0.07, color=WHITE) for dx, dy in PIPS[n]])
    return VGroup(face, dots)


class V3_P1_Media(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 3, "Statistica e probabilità", 1, "Media, mediana, moda"

    def construct(self):
        self.video_card("media · mediana · moda · areogrammi · probabilità",
                        "Ciao! In questo video impariamo a leggere i dati: media, mediana e moda, gli areogrammi, e poi la probabilità, con i dadi e le palline.")
        self.header()
        k = 0.4
        base_y = -1.9
        xs = [-5.2 + 0.85 * i for i in range(8)]
        axis = Line(P(-5.8, base_y), P(1.2, base_y), color=GRAY_B, stroke_width=2)

        def bar(i, v, col=COL_GIV):
            return Rectangle(width=0.6, height=v * k, color=col, stroke_width=2).set_fill(col, 0.55).move_to(P(xs[i], base_y + v * k / 2))
        bars = VGroup(*[bar(i, v) for i, v in enumerate(MARKS)])
        vals = VGroup(*[M(str(v), 30).next_to(bars[i], UP, buff=0.1) for i, v in enumerate(MARKS)])
        with self.say("Questi sono i voti di Luca in matematica: sei, sette, cinque, otto, sette, nove, sette, sei. Li disegno come colonne."):
            self.play(Create(axis))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), FadeIn(vals, lag_ratio=0.15), run_time=2.2)
        tot = M(r"\text{somma} = 55", 40, COL_ANG).move_to(P(4.2, 2.0))
        with self.say("Qual è il voto medio? La media è il valore che ognuno avrebbe se dividessimo tutto in parti uguali. Prima sommo tutti i voti: cinquantacinque."):
            self.play(Write(tot))
        mean = 55 / 8
        lev = VGroup(*[bar(i, mean, COL_RES) for i in range(8)])
        mline = DashedLine(P(-5.8, base_y + mean * k), P(1.2, base_y + mean * k), color=COL_RES, stroke_width=3)
        with self.say("Adesso livello le colonne: tolgo dalle più alte e riempio le più basse. Il totale resta cinquantacinque, ma le colonne diventano tutte uguali."):
            self.play(FadeOut(vals), Transform(bars, lev), run_time=2.4)
            self.play(Create(mline))
        form = VGroup(M(r"\text{media} = \frac{\text{somma}}{\text{numero dei dati}}", 40),
                      M(r"= \frac{55}{8} = 6{,}875", 44, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P(4.1, 0.4))
        with self.say("Ogni colonna è alta cinquantacinque diviso otto: sei virgola otto sette cinque. Questa è la media: la somma dei dati diviso il numero dei dati."):
            self.play(Write(form[0]))
            self.play(Write(form[1]))
        self.wipe()

        bars = VGroup(*[bar(i, v) for i, v in enumerate(MARKS)])
        vals = VGroup(*[M(str(v), 30).next_to(bars[i], UP, buff=0.1) for i, v in enumerate(MARKS)])
        cols = VGroup(*[VGroup(b, t) for b, t in zip(bars, vals)])
        self.play(Create(axis), FadeIn(cols), run_time=0.8)
        order = sorted(range(8), key=lambda i: (MARKS[i], i))
        with self.say("La mediana è il valore che sta in mezzo. Ma prima bisogna mettere i dati in ordine, dal più piccolo al più grande."):
            self.play(*[cols[i].animate.shift(RIGHT * (xs[order.index(i)] - xs[i])) for i in range(8)], run_time=2.0)
        mid = VGroup(cols[order[3]], cols[order[4]])
        med = VGroup(M(r"5,\,6,\,6,\,\mathbf{7},\,\mathbf{7},\,7,\,8,\,9", 40),
                     M(r"\text{mediana} = \frac{7+7}{2} = 7", 42, COL_RES)).arrange(DOWN, buff=0.35).move_to(P(4.2, 1.3))
        with self.say("I dati sono otto, un numero pari: in mezzo ce ne sono due, sette e sette. La mediana è la loro media: sette."):
            self.play(Write(med[0]))
            self.play(Indicate(mid, color=COL_RES, scale_factor=1.08), run_time=1.4)
            self.play(Write(med[1]))
        sevens = VGroup(*[cols[i] for i in range(8) if MARKS[i] == 7])
        mo = VGroup(M(r"\text{moda} = 7", 42, COL_ANG), T("(compare 3 volte)", 24, COL_ANG)).arrange(RIGHT, buff=0.25).move_to(P(4.2, -0.2))
        cv = M(r"\text{campo di variazione} = 9 - 5 = 4", 38, COL_AUX).move_to(P(4.0, -1.1))
        with self.say("La moda è il valore che compare più spesso: il sette, che compare tre volte."):
            self.play(Indicate(sevens, color=COL_ANG, scale_factor=1.08), run_time=1.4)
            self.play(Write(mo))
        with self.say("E il campo di variazione è la differenza tra il valore più grande e il più piccolo: nove meno cinque, quattro."):
            self.play(Write(cv))
        self.end()


class V3_P2_Areogramma(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 3, "Statistica e probabilità", 2, "L'areogramma"

    def construct(self):
        self.title_card()
        rows = VGroup(*[VGroup(T(n, 28, PIE[i]), M(str(v), 34)).arrange(RIGHT, buff=0.5) for i, (n, v) in enumerate(BOOKS)])
        for r in rows:
            r[1].shift(RIGHT * (1.8 - r[1].get_center()[0] + r[0].get_center()[0]))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(P(-4.4, 1.2))
        totr = VGroup(T("totale", 28), M("240", 34, COL_ANG)).arrange(RIGHT, buff=0.5).next_to(rows, DOWN, buff=0.35, aligned_edge=LEFT)
        with self.say("In una biblioteca ci sono novantasei gialli, sessanta fantasy, quarantotto romanzi storici e trentasei biografie. In tutto, duecentoquaranta libri."):
            self.play(FadeIn(rows, lag_ratio=0.3), run_time=1.6)
            self.play(FadeIn(totr))
        f = VGroup(M(r"\% = \frac{\text{parte}}{\text{totale}}\cdot 100", 38),
                   M(r"\text{gradi} = \frac{\text{parte}}{\text{totale}}\cdot 360^\circ", 38)).arrange(DOWN, buff=0.35).move_to(P(3.4, 2.1))
        with self.say("Per ogni genere calcolo la percentuale, parte su totale per cento, e i gradi del settore, parte su totale per trecentosessanta."):
            self.play(Write(f))
        ex = M(r"\text{gialli: } \frac{96}{240}\cdot 360^\circ = 144^\circ", 40, PIE[0]).move_to(P(3.2, 0.5))
        with self.say("Per i gialli: novantasei su duecentoquaranta sono i due quinti, cioè il quaranta per cento. In gradi: centoquarantaquattro."):
            self.play(Write(ex))
        self.play(FadeOut(f), FadeOut(ex))
        C = P(3.0, 0.2)
        secs, info = pie(C, 1.9, [v for _, v in BOOKS], PIE[:4])
        labels = [r"144^\circ", r"90^\circ", r"72^\circ", r"54^\circ"]
        pct = ["40\\%", "25\\%", "20\\%", "15\\%"]
        with self.say("Ecco l'areogramma, settore per settore: centoquarantaquattro, novanta, settantadue e cinquantaquattro gradi. In tutto trecentosessanta."):
            for k in range(4):
                mid, _ = info[k]
                lab = M(labels[k] + r"\ \ " + pct[k], 26, BG).move_to(C + 1.15 * unit(mid))
                self.play(FadeIn(secs[k], scale=0.95), FadeIn(lab), run_time=0.9)
        self.wipe()

        # back from the chart to the data
        C2 = P(-3.2, 0.1)
        secs2, info2 = pie(C2, 1.9, [150, 120, 90], [PIE[1], PIE[2], PIE[3]])
        names = ["sufficiente", "buono", "ottimo"]
        degs = [r"150^\circ", r"120^\circ", r"?"]
        labs = VGroup(*[VGroup(T(names[k], 22, BG), M(degs[k], 28, BG)).arrange(DOWN, buff=0.05).move_to(C2 + 1.1 * unit(info2[k][0])) for k in range(3)])
        with self.say("Ora al contrario. Questo areogramma mostra i giudizi di settantadue alunni. Il settore «ottimo» non è scritto: quanto misura?"):
            self.play(FadeIn(secs2), FadeIn(labs))
        s1 = M(r"360^\circ - (150^\circ + 120^\circ) = 90^\circ", 40, COL_ANG).move_to(P(2.8, 2.65))
        with self.say("Tutto il cerchio è trecentosessanta gradi: tolgo centocinquanta e centoventi, e restano novanta gradi."):
            self.play(Write(s1))
            self.play(Transform(labs[2][1], M(r"90^\circ", 28, BG).move_to(labs[2][1])))
        s2 = VGroup(M(r"\frac{150}{360}\cdot 72 = 30", 40), M(r"\frac{120}{360}\cdot 72 = 24", 40), M(r"\frac{90}{360}\cdot 72 = 18", 40),
                    M(r"30+24+18 = 72\ \checkmark", 40, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(P(2.8, 0.2))
        with self.say("E quanti alunni per ogni giudizio? La stessa frazione del cerchio, ma di settantadue: trenta, ventiquattro e diciotto. Il controllo: la somma fa settantadue."):
            self.play(LaggedStart(*[Write(x) for x in s2], lag_ratio=0.5), run_time=3.2)
        self.end()


class V3_P3_Probabilita(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 3, "Statistica e probabilità", 3, "La probabilità"

    def construct(self):
        self.title_card()
        dice = VGroup(*[die(n, P(-5.0 + 1.1 * (n - 1), 1.6)) for n in range(1, 7)])
        with self.say("Lancio un dado. Può uscire uno, due, tre, quattro, cinque o sei: sei casi possibili, tutti con la stessa possibilità."):
            self.play(LaggedStart(*[FadeIn(d, scale=0.7) for d in dice], lag_ratio=0.15), run_time=1.6)
        form = M(r"P = \frac{\text{casi favorevoli}}{\text{casi possibili}}", 46, COL_ANG).move_to(P(3.2, 1.6))
        with self.say("La probabilità di un evento è il numero dei casi favorevoli diviso il numero dei casi possibili."):
            self.play(Write(form))
        ev = VGroup(M(r"P(\text{pari}) = \frac36 = \frac12 = 50\%", 42), M(r"P(>4) = \frac26 = \frac13 \approx 33\%", 42)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P(-1.6, -0.3))
        with self.say("Esce un numero pari? I casi favorevoli sono due, quattro e sei: tre su sei, cioè un mezzo, il cinquanta per cento."):
            self.play(*[dice[n - 1][0].animate.set_fill(COL_GIV, 0.7) for n in (2, 4, 6)])
            self.play(Write(ev[0]))
        with self.say("Esce un numero maggiore di quattro? Solo cinque e sei: due su sei, un terzo."):
            self.play(*[dice[n - 1][0].animate.set_fill(GRAY_E, 0.6) for n in (2, 4, 6)])
            self.play(*[dice[n - 1][0].animate.set_fill(COL_ANG2, 0.7) for n in (5, 6)])
            self.play(Write(ev[1]))
        self.wipe()

        nl = NumberLine(x_range=[0, 1, 0.25], length=10, color=GRAY_B, include_numbers=False).move_to(P(0, 0.8))
        ticks = VGroup(M("0", 34).next_to(nl.n2p(0), DOWN), M(r"\tfrac12", 34).next_to(nl.n2p(0.5), DOWN), M("1", 34).next_to(nl.n2p(1), DOWN))
        words = VGroup(T("impossibile", 26, COL_ERR).next_to(nl.n2p(0), UP, buff=0.3), T("50%", 26, COL_ANG).next_to(nl.n2p(0.5), UP, buff=0.3),
                       T("certo", 26, COL_RES).next_to(nl.n2p(1), UP, buff=0.3))
        with self.say("La probabilità è sempre un numero tra zero e uno. Zero è l'evento impossibile, come far uscire il sette con un dado. Uno è l'evento certo, come far uscire un numero da uno a sei."):
            self.play(Create(nl), FadeIn(ticks))
            self.play(FadeIn(words, lag_ratio=0.4), run_time=1.6)
        self.wipe()

        # the urn
        jar = VMobject(color=GRAY_B, stroke_width=4).set_points_as_corners([P(-5.6, 1.6), P(-5.6, -1.8), P(-2.4, -1.8), P(-2.4, 1.6)])
        cols = [COL_ERR] * 5 + [COL_GIV] * 3 + [COL_RES] * 2
        balls = VGroup(*[Circle(0.26, color=WHITE, stroke_width=1.5).set_fill(c, 0.9) for c in cols])
        balls.arrange_in_grid(3, 4, buff=0.12).move_to(P(-4.0, -0.9))
        with self.say("Un'urna contiene cinque palline rosse, tre blu e due verdi. Ne estraggo una a caso: dieci casi possibili."):
            self.play(Create(jar))
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.5) for b in balls], lag_ratio=0.08), run_time=1.6)
        u = VGroup(M(r"P(\text{rossa}) = \frac{5}{10} = \frac12", 42, COL_ERR),
                   M(r"P(\text{non blu}) = 1 - \frac{3}{10} = \frac{7}{10}", 42, COL_GIV),
                   M(r"P(\text{rossa o verde}) = \frac{5+2}{10} = \frac{7}{10}", 42, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(P(2.5, 0.2))
        with self.say("La probabilità di una pallina rossa è cinque su dieci, un mezzo."):
            self.play(Indicate(balls[:5], color=COL_ERR, scale_factor=1.15))
            self.play(Write(u[0]))
        with self.say("Non blu? È l'evento contrario di blu. Uno meno tre decimi: sette decimi. Si può controllare contando: sette palline non sono blu."):
            self.play(Write(u[1]))
        with self.say("Rossa oppure verde: cinque più due casi favorevoli, sette su dieci."):
            self.play(Write(u[2]))
        self.end()


class V3_P4_DueDadi(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 3, "Statistica e probabilità", 4, "Due dadi"

    def construct(self):
        self.title_card()
        s = 0.62
        o = P(-5.6, 1.9)
        cells = {}
        grid = VGroup()
        for i in range(1, 7):
            for j in range(1, 7):
                c = o + P(i * s, -j * s)
                sq = Square(s, color=GRAY_B, stroke_width=1.2).move_to(c)
                num = M(str(i + j), 28).move_to(c)
                cells[(i, j)] = VGroup(sq, num)
                grid.add(cells[(i, j)])
        hdr = VGroup(*[M(str(i), 30, COL_GIV).move_to(o + P(i * s, 0)) for i in range(1, 7)],
                     *[M(str(j), 30, COL_ANG).move_to(o + P(0, -j * s)) for j in range(1, 7)])
        with self.say("Adesso lancio due dadi e sommo i numeri. Quanti sono i casi possibili? Faccio una tabella: il primo dado in orizzontale, il secondo in verticale."):
            self.play(FadeIn(hdr, lag_ratio=0.1), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.02), run_time=2.4)
        tot = M(r"6\cdot 6 = 36\ \text{casi}", 42).move_to(P(3.2, 2.2))
        with self.say("Sei per sei: trentasei casi possibili, tutti con la stessa probabilità."):
            self.play(Write(tot))
        seven = VGroup(*[cells[(i, 7 - i)][0] for i in range(1, 7)])
        r7 = M(r"P(\text{somma } 7) = \frac{6}{36} = \frac16", 42, COL_RES).move_to(P(3.2, 1.1))
        with self.say("Somma sette: guarda, i casi stanno tutti su una diagonale. Sono sei. Sei su trentasei, un sesto. È la somma più probabile!"):
            self.play(*[c.animate.set_fill(COL_RES, 0.55) for c in seven], run_time=1.2)
            self.play(Write(r7))
        trap = VGroup(T("1 + 6 e 6 + 1 sono due casi diversi!", 26, COL_ERR)).move_to(P(3.2, 0.2))
        with self.say("Attenzione: uno più sei e sei più uno sono due casi diversi. Il primo dado dà uno e il secondo sei, oppure il contrario. Occupano due caselle."):
            self.play(Indicate(cells[(1, 6)], color=COL_ERR, scale_factor=1.3), Indicate(cells[(6, 1)], color=COL_ERR, scale_factor=1.3), run_time=1.4)
            self.play(FadeIn(trap))
        dbl = VGroup(*[cells[(i, i)][0] for i in range(1, 7)])
        rd = M(r"P(\text{numeri uguali}) = \frac{6}{36} = \frac16", 40, COL_ANG).move_to(P(3.2, -0.7))
        with self.say("Numeri uguali: anche loro sono su una diagonale, l'altra. Sei casi: un sesto."):
            self.play(*[c.animate.set_fill(COL_ANG, 0.55) for c in dbl], run_time=1.2)
            self.play(Write(rd))
        big = VGroup(*[cells[(i, j)][0] for i in range(1, 7) for j in range(1, 7) if i + j > 10])
        rb = M(r"P(\text{somma} > 10) = \frac{3}{36} = \frac{1}{12}", 40, COL_ERR).move_to(P(3.2, -1.6))
        with self.say("Somma maggiore di dieci: undici o dodici. Solo tre caselle nell'angolo: tre su trentasei, un dodicesimo."):
            self.play(*[c.animate.set_stroke(COL_ERR, 4) for c in big], run_time=1.0)
            self.play(Write(rb))
        self.end()


class V3_P5_Esercizi(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 3, "Statistica e probabilità", 5, "Riepilogo ed esercizi"

    def construct(self):
        self.header()
        items = [(r"\text{media} = \frac{\text{somma}}{\text{numero dei dati}}", COL_RES),
                 (r"\text{mediana: in mezzo ai dati in ordine}\qquad \text{moda: il pi\`u frequente}", COL_GIV),
                 (r"\text{gradi} = \frac{\text{parte}}{\text{totale}}\cdot 360^\circ", COL_ANG),
                 (r"P = \frac{\text{favorevoli}}{\text{possibili}}\qquad P(\text{contrario}) = 1 - P", COL_ERR)]
        col = lines_column(items, 38, 0.45).move_to(P(0, 0.4))
        with self.say("Ricapitoliamo. La media livella i dati. La mediana sta in mezzo, dopo averli ordinati. La moda è il più frequente. I gradi di un settore sono la parte del totale per trecentosessanta. E la probabilità è casi favorevoli su casi possibili."):
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in col], lag_ratio=0.5), run_time=4)
        self.wait(0.6)
        self.wipe(keep_header=False)
        self.exercises([("S1", COL_GIV), ("S2", COL_ANG), ("S3", COL_ANG), ("S4", COL_GIV), ("S5", COL_ERR), ("X4", COL_ERR)],
                       "Adesso tocca a te. Nel file degli esercizi fai la sezione cinque, da S uno a S cinque. Poi prova il quesito X quattro della simulazione d'esame.",
                       ["• Per la mediana, prima metti i dati in ordine", "• Controlla che i gradi sommino 360", "• Controlla con il file delle soluzioni"])


if __name__ == "__main__":
    from fractions import Fraction as Fr
    ok = True

    def check(name, got, want):
        global ok
        good = Fr(got) == Fr(want) if not isinstance(want, float) else abs(got - want) < 1e-9
        ok &= good
        print(("OK  " if good else "BAD ") + f"{name}: {got} (expected {want})")
    check("sum marks", sum(MARKS), 55)
    check("mean", 55 / 8, 6.875)
    s = sorted(MARKS)
    check("median", Fr(s[3] + s[4], 2), 7)
    check("mode count", MARKS.count(7), 3)
    check("range", max(MARKS) - min(MARKS), 4)
    tot = sum(v for _, v in BOOKS)
    check("books total", tot, 240)
    for (n, v), deg, pc in zip(BOOKS, (144, 90, 72, 54), (40, 25, 20, 15)):
        check(f"{n} deg", Fr(v * 360, tot), deg)
        check(f"{n} pct", Fr(v * 100, tot), pc)
    check("ottimo", 360 - 150 - 120, 90)
    check("pupils", Fr(150 * 72, 360) + Fr(120 * 72, 360) + Fr(90 * 72, 360), 72)
    check("sum 7", sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 7), 6)
    check("sum > 10", sum(1 for a in range(1, 7) for b in range(1, 7) if a + b > 10), 3)
    check("not blue", 1 - Fr(3, 10), Fr(7, 10))
    print("ALL OK" if ok else "SOME CHECKS FAILED")
