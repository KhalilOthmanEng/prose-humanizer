"""
Video 1 · Numeri e frazioni
===========================
Scenes (render each with  manim -qh v1_numeri.py <Scene>):
  V1_P1_Proprieta   distributive property as an area, commutative as a turned rectangle, division by zero
  V1_P2_McmMcd      the two buses (LCM) and the pencil cases (GCD) with prime factors
  V1_P3_Frazioni    fractions on a pizza, equivalent fractions, common denominator, exercise F1
  V1_P4_Potenze     powers as repeated products, the rules by counting factors, a^0, negative bases
  V1_P5_Radici      square roots as the side of a square, sqrt(50), repeating decimals
  V1_P6_Esercizi    summary and the matching exercises of the worksheet
"""
from comune import *

# ── precomputed values (checked in __main__) ───────────────────────────
DIST = (7, 10, 3)                  # 7·(10+3)
BUS_A, BUS_B = 12, 18
PENS, PENCILS = 48, 72
GCD = 24


class V1_P1_Proprieta(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 1, "Numeri e frazioni", 1, "Le proprietà delle operazioni"

    def construct(self):
        self.video_card("proprietà · mcm e MCD · frazioni · potenze · radici",
                        "Ciao! In questo video parliamo di numeri: le proprietà delle operazioni, "
                        "il minimo comune multiplo e il massimo comune divisore, le frazioni, le potenze e le radici.")
        self.header()
        # distributive property as the area of a rectangle
        s = 0.3
        o = P(-6.2, -1.9)
        grid = unit_squares(7, 13, s, o, COL_GIV, 0.35)
        l13 = M("13", 34).next_to(grid, UP, buff=0.15)
        l7 = M("7", 34).next_to(grid, LEFT, buff=0.15)
        with self.say("Partiamo da una moltiplicazione: sette per tredici. La disegno come un rettangolo: sette file da tredici quadretti."):
            self.play(LaggedStart(*[FadeIn(q) for q in grid], lag_ratio=0.004), run_time=2.0)
            self.play(FadeIn(l13), FadeIn(l7))
        left = VGroup(*[grid[r * 13 + c] for r in range(7) for c in range(10)])
        right = VGroup(*[grid[r * 13 + c] for r in range(7) for c in range(10, 13)])
        with self.say("Adesso taglio il rettangolo in due pezzi: dieci colonne da una parte e tre dall'altra."):
            self.play(right.animate.shift(RIGHT * 0.45).set_fill(COL_ANG, 0.45).set_stroke(COL_ANG), run_time=1.4)
            l10 = M("10", 32, COL_GIV).next_to(left, UP, buff=0.15)
            l3 = M("3", 32, COL_ANG).next_to(right, UP, buff=0.15)
            self.play(ReplacementTransform(l13, VGroup(l10, l3)))
        eq = VGroup(M(r"7\cdot(10+3)", 42),
                    M(r"= 7\cdot 10 + 7\cdot 3", 42),
                    M(r"= 70 + 21", 42),
                    M(r"= 91", 46, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P(3.6, 0.4))
        with self.say("Sette per dieci fa settanta, sette per tre fa ventuno. Insieme fanno novantuno, proprio come sette per tredici."):
            self.play(Write(eq[0]))
            self.play(Write(eq[1]))
            self.play(Write(eq[2]))
            self.play(Write(eq[3]))
        name = T("proprietà distributiva", 32, COL_RES).next_to(eq, UP, buff=0.4)
        with self.say("Questa è la proprietà distributiva: moltiplicare una somma è come moltiplicare ogni pezzo e poi sommare. Ti aiuta anche a fare i conti a mente."):
            self.play(Write(name))
            self.play(Circumscribe(eq, color=COL_RES))
        self.wipe()

        # commutative property: a turned rectangle
        o2 = P(-4.8, -1.4)
        r35 = unit_squares(3, 5, 0.5, o2, COL_ANG2, 0.4)
        lab = M(r"3\cdot 5 = 15", 42).move_to(P(2.8, 1.2))
        with self.say("Guarda questo rettangolo: tre file da cinque, quindici quadretti."):
            self.play(FadeIn(r35, lag_ratio=0.05), run_time=1.2)
            self.play(Write(lab))
        lab2 = M(r"5\cdot 3 = 15", 42).move_to(P(2.8, 0.2))
        with self.say("Se lo giro, diventa cinque file da tre. I quadretti sono sempre quindici: tre per cinque è uguale a cinque per tre. È la proprietà commutativa."):
            self.play(Rotate(r35, angle=-PI / 2), run_time=1.6)
            self.play(Write(lab2))
            self.play(FadeIn(T("proprietà commutativa", 30, COL_RES).next_to(lab2, DOWN, buff=0.4)))
        self.wipe()

        # division and zero
        d1 = M(r"12 : 3 = 4 \quad\text{perch\'e}\quad 4\cdot 3 = 12", 42).move_to(P(0, 2.2))
        with self.say("E lo zero? Dividere vuol dire chiedersi: quale numero, moltiplicato per il divisore, mi dà il dividendo? Dodici diviso tre fa quattro, perché quattro per tre fa dodici."):
            self.play(Write(d1), run_time=1.6)
        rows = VGroup(
            VGroup(M(r"0 : 9 = 0", 42, COL_RES), T("perché 0 · 9 = 0", 28, COL_RES)),
            VGroup(M(r"9 : 0 = \;?", 42, COL_ERR), T("nessun numero · 0 fa 9: impossibile", 28, COL_ERR)),
            VGroup(M(r"0 : 0 = \;?", 42, COL_ANG), T("ogni numero · 0 fa 0: indeterminata", 28, COL_ANG)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.6)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(P(0, 0.0))
        with self.say("Zero diviso nove fa zero, perché zero per nove fa zero."):
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
        with self.say("Ma nove diviso zero? Nessun numero moltiplicato per zero può dare nove. La divisione è impossibile."):
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2))
        with self.say("E zero diviso zero? Qui succede il contrario: tutti i numeri moltiplicati per zero danno zero. Si dice indeterminata."):
            self.play(FadeIn(rows[2], shift=RIGHT * 0.2))
        self.end()


class V1_P2_McmMcd(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 1, "Numeri e frazioni", 2, "mcm e MCD"

    def construct(self):
        self.title_card()
        prob = VGroup(T("Due autobus partono insieme alle 7:00.", 28),
                      T("Il primo ripassa ogni 12 minuti, il secondo ogni 18.", 28)).arrange(DOWN, buff=0.12).move_to(P(0, 2.7))
        with self.say("Due autobus partono insieme dal capolinea alle sette. Il primo ripassa ogni dodici minuti, il secondo ogni diciotto. Quando ripartono di nuovo insieme?"):
            self.play(FadeIn(prob))
        nlA = NumberLine(x_range=[0, 40, 2], length=11, color=GRAY_B, include_ticks=True, tick_size=0.05).move_to(P(0, 1.0))
        nlB = nlA.copy().move_to(P(0, -0.9))
        la = T("autobus A", 24, COL_GIV).next_to(nlA, LEFT, buff=0.2).shift(UP * 0.35 + RIGHT * 1.4)
        lb = T("autobus B", 24, COL_ANG2).next_to(nlB, LEFT, buff=0.2).shift(UP * 0.35 + RIGHT * 1.4)
        nums = VGroup(*[M(str(k), 22, GRAY_B).next_to(nlB.n2p(k), DOWN, buff=0.15) for k in range(0, 41, 6)])
        with self.say("Disegno il tempo su due righe, una per autobus, da zero a quaranta minuti."):
            self.play(Create(nlA), Create(nlB), FadeIn(la), FadeIn(lb), FadeIn(nums))
        dA = VGroup(*[Dot(nlA.n2p(k), radius=0.1, color=COL_GIV) for k in (0, 12, 24, 36)])
        dB = VGroup(*[Dot(nlB.n2p(k), radius=0.1, color=COL_ANG2) for k in (0, 18, 36)])
        tA = VGroup(*[M(str(k), 26, COL_GIV).next_to(nlA.n2p(k), UP, buff=0.15) for k in (12, 24, 36)])
        tB = VGroup(*[M(str(k), 26, COL_ANG2).next_to(nlB.n2p(k), UP, buff=0.15) for k in (18, 36)])
        with self.say("Il primo autobus passa a dodici, ventiquattro, trentasei minuti: sono i multipli di dodici."):
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dA], lag_ratio=0.35), FadeIn(tA), run_time=2.0)
        with self.say("Il secondo passa a diciotto e trentasei: i multipli di diciotto."):
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dB], lag_ratio=0.35), FadeIn(tB), run_time=1.6)
        meet = DashedLine(nlA.n2p(36) + UP * 0.5, nlB.n2p(36) + DOWN * 0.1, color=COL_RES, stroke_width=3)
        with self.say("Il primo multiplo comune è trentasei. Ripartono insieme dopo trentasei minuti, cioè alle sette e trentasei."):
            self.play(Create(meet))
            self.play(Flash(nlA.n2p(36), color=COL_RES), Flash(nlB.n2p(36), color=COL_RES))
        self.wipe()

        fac = VGroup(M(r"12 = 2^2\cdot 3", 44), M(r"18 = 2\cdot 3^2", 44),
                     M(r"\text{mcm}(12,18) = 2^2\cdot 3^2 = 36", 46, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(P(0, 1.0))
        rule = T("mcm: tutti i fattori, comuni e non comuni, con l'esponente più grande", 26, COL_ANG).move_to(P(0, -1.2))
        with self.say("Con i numeri primi è più veloce. Dodici è due alla seconda per tre; diciotto è due per tre alla seconda."):
            self.play(Write(fac[0]))
            self.play(Write(fac[1]))
        with self.say("Per il minimo comune multiplo prendo tutti i fattori, comuni e non comuni, con l'esponente più grande: due alla seconda per tre alla seconda, trentasei."):
            self.play(Write(fac[2]))
            self.play(FadeIn(rule, shift=UP * 0.2))
        self.wipe()

        # GCD: 48 pens and 72 pencils into equal cases
        q = VGroup(T("48 penne e 72 matite in astucci tutti uguali:", 28),
                   T("quanti astucci, al massimo?", 28)).arrange(DOWN, buff=0.12).move_to(P(0, 2.8))
        pens = VGroup(*[Dot(radius=0.07, color=COL_GIV) for _ in range(PENS)]).arrange_in_grid(6, 8, buff=0.12).move_to(P(-3.8, 0.4))
        pencils = VGroup(*[Dot(radius=0.07, color=COL_ANG) for _ in range(PENCILS)]).arrange_in_grid(8, 9, buff=0.12).move_to(P(-0.6, 0.4))
        lp = T("48 penne", 24, COL_GIV).next_to(pens, DOWN, buff=0.2)
        lm = T("72 matite", 24, COL_ANG).next_to(pencils, DOWN, buff=0.2)
        with self.say("Adesso il problema opposto. Una maestra ha quarantotto penne e settantadue matite, e vuole preparare astucci tutti uguali, usando tutto. Quanti astucci, al massimo?"):
            self.play(FadeIn(q))
            self.play(FadeIn(pens, lag_ratio=0.01), FadeIn(pencils, lag_ratio=0.01), FadeIn(lp), FadeIn(lm), run_time=1.6)
        fac2 = VGroup(M(r"48 = 2^4\cdot 3", 40), M(r"72 = 2^3\cdot 3^2", 40),
                      M(r"\text{MCD} = 2^3\cdot 3 = 24", 42, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P(4.3, 0.6))
        with self.say("Qui dobbiamo dividere in parti uguali, le più grandi possibili: serve il massimo comune divisore. Prendo solo i fattori comuni, con l'esponente più piccolo: due alla terza per tre, ventiquattro."):
            self.play(Write(fac2[0]), Write(fac2[1]))
            self.play(Write(fac2[2]))
        # 24 cases: 4 rows x 6 columns, each with 2 pens and 3 pencils
        cases = VGroup()
        tgt_p, tgt_m = VGroup(), VGroup()
        for i in range(GCD):
            r, c = divmod(i, 6)
            ctr = P(-5.6 + c * 1.05, 1.3 - r * 0.85)
            box = RoundedRectangle(width=0.9, height=0.7, corner_radius=0.08, color=GRAY_B, stroke_width=1.5).move_to(ctr)
            cases.add(box)
            for k in range(2):
                tgt_p.add(Dot(ctr + P(-0.25 + 0.2 * k, 0.15), radius=0.07, color=COL_GIV))
            for k in range(3):
                tgt_m.add(Dot(ctr + P(-0.2 + 0.2 * k, -0.15), radius=0.07, color=COL_ANG))
        with self.say("Guarda: ventiquattro astucci, e in ognuno due penne e tre matite. Non avanza niente."):
            self.play(FadeOut(lp), FadeOut(lm), FadeOut(q), FadeIn(cases, lag_ratio=0.03), run_time=1.2)
            self.play(Transform(pens, tgt_p), Transform(pencils, tgt_m), run_time=2.4)
        res = M(r"48 : 24 = 2 \qquad 72 : 24 = 3", 38, COL_RES).next_to(fac2, DOWN, buff=0.45)
        with self.say("Infatti quarantotto diviso ventiquattro fa due, e settantadue diviso ventiquattro fa tre."):
            self.play(Write(res))
        self.wipe()
        tip = VGroup(T("Si ripete insieme  →  mcm", 36, COL_GIV),
                     T("Si divide in parti uguali  →  MCD", 36, COL_ANG)).arrange(DOWN, buff=0.6)
        with self.say("Il trucco per non sbagliare: se qualcosa si ripete e cerchi quando succede insieme, usi il minimo comune multiplo. Se devi dividere in parti uguali, usi il massimo comune divisore."):
            self.play(FadeIn(tip[0], shift=UP * 0.2))
            self.play(FadeIn(tip[1], shift=UP * 0.2))
        self.end()


class V1_P3_Frazioni(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 1, "Numeri e frazioni", 3, "Le frazioni"

    def construct(self):
        self.title_card()
        C = P(-4.4, 0.3)
        R = 1.8
        secs, _ = pie(C, R, [1] * 4, [COL_ANG, COL_ANG, COL_ANG, GRAY_D])
        edges = VGroup(Circle(radius=R, color=WHITE, stroke_width=3).move_to(C),
                       *[Line(C, C + R * unit(90 - 90 * k), color=WHITE, stroke_width=3) for k in range(4)])
        f34 = M(r"\frac{3}{4}", 72, COL_ANG).move_to(P(-1.5, 0.8))
        with self.say("Una frazione è una parte di un intero. Taglio una pizza in quattro fette uguali e ne prendo tre: tre quarti."):
            self.play(FadeIn(secs), Create(edges), run_time=1.4)
            self.play(Write(f34))
        num = T("numeratore: le parti che prendo", 26, COL_ANG).next_to(f34, RIGHT, buff=0.4).shift(UP * 0.4)
        den = T("denominatore: le parti uguali del tutto", 26, GRAY_B).next_to(f34, RIGHT, buff=0.4).shift(DOWN * 0.4)
        with self.say("Il numero sotto, il denominatore, dice in quante parti uguali taglio. Il numero sopra, il numeratore, quante ne prendo."):
            self.play(FadeIn(den))
            self.play(FadeIn(num))
        secs12, _ = pie(C, R, [1] * 12, [COL_ANG] * 9 + [GRAY_D] * 3)
        edges12 = VGroup(*[Line(C, C + R * unit(90 - 30 * k), color=WHITE, stroke_width=1.5) for k in range(12)])
        f912 = M(r"\frac{3}{4} = \frac{9}{12}", 64).move_to(P(1.0, -1.5))
        with self.say("Adesso taglio ogni fetta in tre. Le fette diventano dodici e le mie diventano nove, ma la pizza che mangio è la stessa: tre quarti è uguale a nove dodicesimi."):
            self.play(FadeIn(edges12), ReplacementTransform(secs, secs12), run_time=1.6)
            self.play(Write(f912))
        with self.say("Le frazioni equivalenti si ottengono moltiplicando numeratore e denominatore per lo stesso numero. Qui, per tre."):
            self.play(Indicate(f912))
        self.wipe()

        # common denominator with bars
        L = 7.2
        x0 = -4.2

        def bar(y, parts, filled, col):
            w = L / parts
            g = VGroup(*[Rectangle(width=w, height=0.55, color=WHITE, stroke_width=2)
                         .set_fill(col if k < filled else GRAY_E, 0.8 if k < filled else 0.3)
                         .move_to(P(x0 + w * (k + 0.5), y)) for k in range(parts)])
            return g
        b1 = bar(1.6, 4, 3, COL_ANG)
        b2 = bar(0.4, 6, 1, COL_GIV)
        e1 = M(r"\frac34", 44, COL_ANG).next_to(b1, LEFT, buff=0.3)
        e2 = M(r"\frac16", 44, COL_GIV).next_to(b2, LEFT, buff=0.3)
        with self.say("Come si sommano tre quarti e un sesto? Le fette sono di grandezza diversa: non posso sommarle così."):
            self.play(FadeIn(b1), FadeIn(e1))
            self.play(FadeIn(b2), FadeIn(e2))
        b1n = bar(1.6, 12, 9, COL_ANG)
        b2n = bar(0.4, 12, 2, COL_GIV)
        e1n = M(r"\frac{9}{12}", 44, COL_ANG).move_to(e1)
        e2n = M(r"\frac{2}{12}", 44, COL_GIV).move_to(e2)
        with self.say("Taglio tutte e due le strisce in dodicesimi, perché dodici è il minimo comune multiplo di quattro e sei. Tre quarti diventano nove dodicesimi, un sesto diventa due dodicesimi."):
            self.play(ReplacementTransform(b1, b1n), ReplacementTransform(e1, e1n), run_time=1.4)
            self.play(ReplacementTransform(b2, b2n), ReplacementTransform(e2, e2n), run_time=1.4)
        tot = VGroup(*[Rectangle(width=L / 12, height=0.55, color=WHITE, stroke_width=2)
                       .set_fill(COL_ANG if k < 9 else (COL_GIV if k < 11 else GRAY_E), 0.8 if k < 11 else 0.3)
                       .move_to(P(x0 + L / 12 * (k + 0.5), -1.0)) for k in range(12)])
        et = M(r"\frac{11}{12}", 44, COL_RES).next_to(tot, LEFT, buff=0.3)
        sumeq = M(r"\frac34+\frac16=\frac{9}{12}+\frac{2}{12}=\frac{11}{12}", 44, COL_RES).move_to(P(0, -2.1))
        with self.say("Adesso sì: nove più due fa undici. La somma è undici dodicesimi."):
            self.play(TransformFromCopy(VGroup(b1n[:9], b2n[:2]), tot[:11]), FadeIn(tot[11:]), run_time=1.6)
            self.play(Write(et), Write(sumeq))
        self.wipe()

        # exercise F1
        e = VGroup(M(r"\left(\frac34+\frac16\right)\cdot\frac{6}{11}-\frac13", 50),
                   M(r"=\frac{11}{12}\cdot\frac{6}{11}-\frac13", 50),
                   M(r"=\frac{\cancel{11}\,^{1}}{\cancel{12}\,_{2}}\cdot\frac{\cancel{6}\,^{1}}{\cancel{11}\,_{1}}-\frac13", 50),
                   M(r"=\frac12-\frac13=\frac{3-2}{6}=\frac16", 50, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(P(-2.4, 0.45))
        with self.say("Ora l'esercizio F uno del file. Prima la parentesi: abbiamo appena visto che fa undici dodicesimi."):
            self.play(Write(e[0]))
            self.play(Write(e[1]))
        with self.say("Poi la moltiplicazione. Prima di moltiplicare semplifico in croce: undici con undici, sei con dodici. Resta un mezzo."):
            self.play(Write(e[2]))
        with self.say("Infine la sottrazione: un mezzo meno un terzo. Denominatore comune sei: tre sesti meno due sesti, un sesto."):
            self.play(Write(e[3]))
            self.play(Circumscribe(e[3], color=COL_RES))
        order = VGroup(T("Ordine:", 30, COL_ANG, weight=BOLD), T("1. parentesi", 28, COL_ANG), T("2. per e diviso", 28, COL_ANG),
                       T("3. più e meno", 28, COL_ANG)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(P(4.3, 0.3))
        with self.say("Ricorda l'ordine: prima le parentesi, poi moltiplicazioni e divisioni, e solo alla fine addizioni e sottrazioni."):
            self.play(FadeIn(order, shift=UP * 0.2))
        self.end()


class V1_P4_Potenze(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 1, "Numeri e frazioni", 4, "Le potenze"

    def construct(self):
        self.title_card()
        d = VGroup(M(r"2^3", 72, COL_ANG), M(r"= 2\cdot 2\cdot 2", 60), M(r"= 8", 60, COL_RES)).arrange(RIGHT, buff=0.3).move_to(P(0, 2.2))
        lab = VGroup(T("base", 24, COL_ANG), T("esponente", 24, COL_AUX))
        with self.say("Una potenza è una moltiplicazione ripetuta. Due alla terza vuol dire due per due per due: otto."):
            self.play(Write(d[0]))
            self.play(Write(d[1]))
            self.play(Write(d[2]))
        lab[0].next_to(d[0], DOWN, buff=0.25).shift(LEFT * 0.2)
        lab[1].next_to(d[0], UP, buff=0.15).shift(RIGHT * 0.3)
        with self.say("Il numero grande è la base; il numero piccolo in alto, l'esponente, dice quante volte la moltiplico."):
            self.play(FadeIn(lab))
        # doubling squares
        sq = [VGroup(*[Square(0.4, color=COL_ANG, stroke_width=2).set_fill(COL_ANG, 0.4) for _ in range(n)]).arrange(RIGHT, buff=0.08)
              for n in (1, 2, 4, 8)]
        for k, g in enumerate(sq):
            g.move_to(P(-3.2 + 0.0, 0.6 - 0.72 * k), aligned_edge=LEFT)
        tags = VGroup(*[M(t, 32).next_to(sq[k], LEFT, buff=0.3) for k, t in enumerate([r"2^0=1", r"2^1=2", r"2^2=4", r"2^3=8"])])
        with self.say("Ogni volta che l'esponente cresce di uno, il risultato raddoppia: uno, due, quattro, otto."):
            for k in range(4):
                self.play(FadeIn(sq[k], lag_ratio=0.1), FadeIn(tags[k]), run_time=0.8)
        self.wipe()

        # product rule by counting factors
        a = MS(r"2^3", r"\cdot", r"2^4", fs=56).move_to(P(0, 2.0))
        b = MS(r"(2\cdot2\cdot2)", r"\cdot", r"(2\cdot2\cdot2\cdot2)", fs=50).move_to(P(0, 0.9))
        c = MS(r"2^7", fs=60, col=COL_RES).move_to(P(0, -0.2))
        with self.say("Perché le regole delle potenze funzionano? Basta contare. Due alla terza per due alla quarta: scrivo tutti i fattori."):
            self.play(Write(a))
            self.play(TransformFromCopy(a, b), run_time=1.4)
        with self.say("Tre due più quattro due fanno sette due in fila: due alla settima. Con la stessa base, gli esponenti si sommano."):
            self.play(TransformFromCopy(b, c), run_time=1.2)
            self.play(FadeIn(M(r"a^m\cdot a^n = a^{m+n}", 44, COL_ANG).move_to(P(0, -1.4))))
        self.wipe()
        q1 = M(r"2^5 : 2^3 = \frac{2\cdot2\cdot2\cdot2\cdot2}{2\cdot2\cdot2}", 50).move_to(P(0, 2.0))
        with self.say("Nella divisione i due in comune si semplificano: ne restano due. Due alla quinta diviso due alla terza fa due alla seconda: gli esponenti si sottraggono."):
            self.play(Write(q1))
            q2 = M(r"= 2^{5-3} = 2^2 = 4", 50, COL_RES).next_to(q1, DOWN, buff=0.4)
            self.play(Write(q2))
        q3 = M(r"(3^2)^3 = 3^2\cdot3^2\cdot3^2 = 3^{2+2+2} = 3^6", 48).next_to(q1, DOWN, buff=1.4)
        with self.say("E la potenza di una potenza? Tre alla seconda, il tutto alla terza, vuol dire tre alla seconda scritto tre volte: gli esponenti si moltiplicano, tre alla sesta."):
            self.play(Write(q3))
        self.wipe()

        # a^0 = 1 by the halving staircase
        rows = VGroup(*[M(s, 48) for s in (r"2^4 = 16", r"2^3 = 8", r"2^2 = 4", r"2^1 = 2", r"2^0 = \;?")]).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(P(-2.5, 0.4))
        arrows = VGroup(*[M(r":2", 30, COL_AUX).next_to(rows[k], RIGHT, buff=0.6).shift(DOWN * 0.38) for k in range(4)])
        with self.say("Quanto fa due alla zero? Guarda la scala: ogni volta che scendo di un gradino divido per due."):
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:4]], lag_ratio=0.3), run_time=1.6)
            self.play(FadeIn(arrows[:3]))
        one = M(r"2^0 = 1", 48, COL_RES).move_to(rows[4], aligned_edge=LEFT)
        with self.say("Due diviso due fa uno. Quindi due alla zero fa uno. Vale per ogni base diversa da zero."):
            self.play(FadeIn(rows[4]), FadeIn(arrows[3]))
            self.play(ReplacementTransform(rows[4], one))
            self.play(Circumscribe(one, color=COL_RES))
        self.wipe()

        sg = VGroup(M(r"(-2)^1=-2", 44), M(r"(-2)^2=+4", 44), M(r"(-2)^3=-8", 44), M(r"(-2)^4=+16", 44)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P(-3.0, 0.6))
        with self.say("Con la base negativa il segno si alterna: meno per meno fa più. Esponente pari: positivo. Esponente dispari: negativo."):
            self.play(LaggedStart(*[FadeIn(s) for s in sg], lag_ratio=0.4), run_time=2.0)
        trap = VGroup(T("Trappola!", 32, COL_ERR), M(r"-2^4 = -(2^4) = -16", 46, COL_ERR),
                      M(r"(-2)^4 = +16", 46, COL_RES)).arrange(DOWN, buff=0.35).move_to(P(3.2, 0.6))
        with self.say("Attenzione a questa trappola: meno due alla quarta, senza parentesi, vuol dire meno di due alla quarta: meno sedici. Con le parentesi, invece, fa più sedici."):
            self.play(FadeIn(trap[0]))
            self.play(Write(trap[1]))
            self.play(Write(trap[2]))
        self.end()


class V1_P5_Radici(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 1, "Numeri e frazioni", 5, "Radici e numeri periodici"

    def construct(self):
        self.title_card()
        g = unit_squares(12, 12, 0.22, P(-5.6, -1.9), COL_GIV, 0.3, 0.8)
        ar = M(r"144", 44, COL_GIV).move_to(g)
        side = M(r"12", 38, COL_ANG).next_to(g, DOWN, buff=0.15)
        with self.say("La radice quadrata è l'operazione inversa della potenza alla seconda. Immagina un quadrato fatto di centoquarantaquattro quadretti."):
            self.play(FadeIn(g, lag_ratio=0.002), run_time=1.6)
            self.play(FadeIn(ar))
        eqs = VGroup(M(r"\sqrt{144} = 12", 50, COL_RES), M(r"\text{perch\'e}\ 12^2 = 144", 40),
                     M(r"\sqrt{\frac{9}{25}} = \frac35", 46), M(r"\sqrt{0{,}49} = 0{,}7", 46)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(P(2.6, 0.4))
        with self.say("Quanto è lungo il lato? Dodici, perché dodici per dodici fa centoquarantaquattro. La radice di centoquarantaquattro è dodici."):
            self.play(Write(side))
            self.play(Write(eqs[0]), Write(eqs[1]))
        with self.say("Con le frazioni si fa la radice sopra e sotto: radice di nove venticinquesimi è tre quinti. E radice di zero virgola quarantanove è zero virgola sette."):
            self.play(Write(eqs[2]))
            self.play(Write(eqs[3]))
        self.wipe()

        s = 0.3
        o = P(-6.0, -2.0)
        g49 = unit_squares(7, 7, s, o, COL_GIV, 0.4)
        extra = Square(s, color=COL_ANG, stroke_width=1.2).set_fill(COL_ANG, 0.7).move_to(o + P(7.5 * s, 0.5 * s))
        g64 = Square(8 * s, color=COL_ERR, stroke_width=2).move_to(o + P(4 * s, 4 * s))
        with self.say("E radice di cinquanta? Cinquanta non è un quadrato perfetto. Sette per sette fa quarantanove: ci manca un solo quadretto."):
            self.play(FadeIn(g49, lag_ratio=0.01), run_time=1.2)
            self.play(FadeIn(extra, scale=1.5))
        with self.say("Otto per otto invece fa sessantaquattro, troppo. Quindi radice di cinquanta è tra sette e otto, molto vicino a sette."):
            self.play(Create(g64))
        ineq = VGroup(M(r"7^2 = 49 < 50 < 64 = 8^2", 44), M(r"7 < \sqrt{50} < 8", 48, COL_RES), M(r"\sqrt{50}\approx 7{,}07", 44, COL_ANG)).arrange(DOWN, buff=0.35).move_to(P(2.8, 0.4))
        with self.say("Con la calcolatrice: circa sette virgola zero sette."):
            self.play(Write(ineq[0]))
            self.play(Write(ineq[1]))
            self.play(Write(ineq[2]))
        self.wipe()

        # repeating decimals
        dv = VGroup(M(r"1 : 3 = 0{,}333\ldots", 52), M(r"\text{resto } 1,\ 1,\ 1,\ \ldots", 38, COL_ANG)).arrange(DOWN, buff=0.3).move_to(P(0, 1.2))
        with self.say("Adesso i numeri decimali periodici. Se divido uno per tre, il resto è sempre uno, e la cifra tre si ripete all'infinito: zero virgola tre periodico."):
            self.play(Write(dv[0]))
            self.play(FadeIn(dv[1]))
        self.play(FadeOut(dv), run_time=0.4)
        rules = VGroup(M(r"0{,}\overline{3} = \frac39 = \frac13", 44),
                       M(r"0{,}\overline{45} = \frac{45}{99} = \frac{5}{11}", 44),
                       M(r"1{,}2\overline{5} = \frac{125-12}{90} = \frac{113}{90}", 44)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(P(-2.6, 0.4))
        with self.say("Per tornare alla frazione c'è una regola. Il periodo va al numeratore, e al denominatore metto tanti nove quante sono le cifre del periodo."):
            self.play(Write(rules[0]))
            self.play(Write(rules[1]))
        note = VGroup(T("sotto: un 9 per ogni cifra", 26, COL_ANG), T("del periodo e uno 0 per ogni", 26, COL_ANG),
                      T("cifra dell'antiperiodo", 26, COL_ANG)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(P(3.6, -0.6))
        with self.say("Se dopo la virgola c'è una parte che non si ripete, l'antiperiodo: sopra tutto il numero senza virgola meno la parte che non si ripete, sotto un nove per ogni cifra del periodo e uno zero per ogni cifra dell'antiperiodo."):
            self.play(Write(rules[2]))
            self.play(FadeIn(note))
        self.end()


class V1_P6_Esercizi(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 1, "Numeri e frazioni", 6, "Riepilogo ed esercizi"

    def construct(self):
        self.header()
        items = [(r"a\cdot(b+c) = a\cdot b + a\cdot c", COL_GIV),
                 (r"\text{mcm: tutti i fattori, esponente maggiore}", COL_GIV),
                 (r"\text{MCD: fattori comuni, esponente minore}", COL_ANG),
                 (r"a^m\cdot a^n = a^{m+n}\qquad a^m:a^n=a^{m-n}\qquad (a^m)^n=a^{m\cdot n}", COL_AUX),
                 (r"a^0 = 1\qquad \sqrt{144} = 12", COL_RES)]
        col = lines_column(items, 38, 0.4).move_to(P(0, 0.4))
        with self.say("Ricapitoliamo. La proprietà distributiva. Il minimo comune multiplo e il massimo comune divisore. Le regole delle potenze, che si capiscono contando i fattori. E la radice come lato di un quadrato."):
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in col], lag_ratio=0.5), run_time=4)
        self.wait(0.6)
        self.wipe(keep_header=False)
        self.exercises([("N1", COL_GIV), ("N2", COL_GIV), ("F1", COL_ANG), ("F2", COL_ANG), ("F3", COL_ANG), ("F4", COL_ANG), ("F5", COL_ERR)],
                       "Adesso tocca a te. Nel file degli esercizi fai le sezioni uno e due: gli esercizi N uno e N due, e da F uno a F cinque. Parti da quelli con una stella.",
                       ["• Scrivi tutti i passaggi sul quaderno", "• Parti dagli esercizi con una stella", "• Poi controlla con il file delle soluzioni"])


if __name__ == "__main__":
    from fractions import Fraction as Fr
    from math import gcd, sqrt
    ok = True

    def check(name, got, want):
        global ok
        good = got == want if not isinstance(want, float) else abs(got - want) < 1e-9
        ok &= good
        print(("OK  " if good else "BAD ") + f"{name}: {got} (expected {want})")
    check("7*13", 7 * 13, 91)
    check("70+21", 7 * 10 + 7 * 3, 91)
    check("lcm 12 18", 12 * 18 // gcd(12, 18), 36)
    check("gcd 48 72", gcd(PENS, PENCILS), GCD)
    check("pens per case", PENS // GCD, 2)
    check("pencils per case", PENCILS // GCD, 3)
    check("3/4 = 9/12", Fr(3, 4), Fr(9, 12))
    check("3/4+1/6", Fr(3, 4) + Fr(1, 6), Fr(11, 12))
    check("F1", (Fr(3, 4) + Fr(1, 6)) * Fr(6, 11) - Fr(1, 3), Fr(1, 6))
    check("2^3*2^4", 2**3 * 2**4, 2**7)
    check("2^5:2^3", 2**5 // 2**3, 4)
    check("(3^2)^3", (3**2) ** 3, 3**6)
    check("-2^4", -(2**4), -16)
    check("(-2)^4", (-2) ** 4, 16)
    check("sqrt 144", sqrt(144), 12.0)
    check("sqrt 50 ~", round(sqrt(50), 2), 7.07)
    check("0.(45)", Fr(45, 99), Fr(5, 11))
    check("1.2(5)", Fr(113, 90), Fr(125 - 12, 90))
    print("ALL OK" if ok else "SOME CHECKS FAILED")
