"""
Video 2 · Equazioni e percentuali
=================================
Scenes (render each with  manim -qh v2_equazioni.py <Scene>):
  V2_P1_Bilancia     the equation as a balance: 3x + 2 = x + 10, what you do on one side you do on the other
  V2_P2_Equazioni    exercises E1, E2, E3 step by step; impossible and undetermined equations
  V2_P3_Problemi     word problems: rectangle with perimeter 56, three consecutive numbers
  V2_P4_Proporzioni  proportions, direct proportion (graph through the origin), inverse proportion (same area)
  V2_P5_Percentuali  the 100 square grid, percentage of, reverse percentage (the shoes), +10% then -10%
  V2_P6_Esercizi     summary and the matching exercises
"""
from comune import *

FULCRUM = P(0, -1.2)
BEAM_Y = -1.2


def balance_items(nx, n1, x_start):
    """boxes (value x) then unit weights, sitting on the beam from x_start to the right"""
    boxes, ws = VGroup(), VGroup()
    x = x_start
    for _ in range(nx):
        b = Square(0.6, color=COL_GIV, stroke_width=3).set_fill(COL_GIV, 0.45).move_to(P(x + 0.3, BEAM_Y + 0.35))
        boxes.add(VGroup(b, M("x", 30).move_to(b)))
        x += 0.7
    for j in range(n1):
        c, r = j % 5, j // 5
        w = Circle(0.2, color=COL_ANG, stroke_width=2).set_fill(COL_ANG, 0.6).move_to(P(x + 0.25 + 0.44 * c, BEAM_Y + 0.25 + 0.44 * r))
        ws.add(VGroup(w, M("1", 22, BG).move_to(w)))
    return boxes, ws


class V2_P1_Bilancia(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 2, "Equazioni e percentuali", 1, "L'equazione è una bilancia"

    def construct(self):
        self.video_card("equazioni · proporzioni · percentuali",
                        "Ciao! In questo video impariamo a risolvere le equazioni, a usare le proporzioni e a calcolare le percentuali, anche quelle degli sconti.")
        self.header()
        beam = Rectangle(width=10.6, height=0.12, color=WHITE, stroke_width=2).set_fill(GRAY_B, 1).move_to(P(0, BEAM_Y - 0.06))
        base = Polygon(FULCRUM + DOWN * 0.12, P(-0.55, -2.25), P(0.55, -2.25), color=WHITE, stroke_width=2).set_fill(GRAY_D, 1)
        lb, lw = balance_items(3, 2, -5.0)
        rb, rw = balance_items(1, 10, 0.6)
        eq = MS(r"3x", r"+2", r"=", r"x", r"+10", fs=60).move_to(P(0, 2.4))
        with self.say("Un'equazione è come una bilancia in equilibrio. Il segno uguale dice che i due piatti pesano lo stesso."):
            self.play(FadeIn(base), FadeIn(beam))
            self.play(FadeIn(lb, lag_ratio=0.2), FadeIn(lw, lag_ratio=0.2), FadeIn(rb), FadeIn(rw, lag_ratio=0.1), run_time=2.0)
        with self.say("Ogni scatola blu pesa x, un numero che non conosciamo. Ogni pallina gialla pesa uno. A sinistra: tre x più due. A destra: x più dieci."):
            self.play(Write(eq), run_time=1.6)
        # wrong move: remove only on one side
        scale_all = VGroup(beam, lb, lw, rb, rw)
        with self.say("Cosa succede se tolgo due palline solo da una parte? La bilancia si inclina: non è più in equilibrio. Non si fa!"):
            self.play(rw[8:].animate.shift(UP * 1.2).set_opacity(0.2), run_time=0.8)
            self.play(Rotate(VGroup(beam, lb, lw, rb, rw[:8]), angle=8 * DEGREES, about_point=FULCRUM), run_time=1.0)
            cross = Cross(eq, stroke_color=COL_ERR, stroke_width=5)
            self.play(Create(cross))
        with self.say("La regola d'oro: quello che fai da una parte, lo devi fare anche dall'altra."):
            self.play(Rotate(VGroup(beam, lb, lw, rb, rw[:8]), angle=-8 * DEGREES, about_point=FULCRUM), FadeOut(cross), run_time=1.0)
            self.play(rw[8:].animate.shift(DOWN * 1.2).set_opacity(1), run_time=0.8)
        eq2 = MS(r"2x", r"+2", r"=", r"10", fs=60).move_to(eq)
        with self.say("Primo passo: tolgo una scatola da tutte e due le parti. Resta: due x più due uguale dieci."):
            self.play(FadeOut(lb[2], shift=UP), FadeOut(rb[0], shift=UP), run_time=1.0)
            self.play(TransformMatchingTex(eq, eq2))
        eq3 = MS(r"2x", r"=", r"8", fs=60).move_to(eq)
        with self.say("Secondo passo: tolgo due palline da tutte e due le parti. Resta: due x uguale otto."):
            self.play(FadeOut(lw, shift=UP), FadeOut(rw[:2], shift=UP), run_time=1.0)
            self.play(*[rw[2 + k].animate.move_to(P(0.85 + 0.44 * (k % 4), BEAM_Y + 0.25 + 0.44 * (k // 4))) for k in range(8)],
                      TransformMatchingTex(eq2, eq3))
        eq4 = MS(r"x", r"=", r"4", fs=64, col=COL_RES).move_to(eq)
        with self.say("Terzo passo: se due scatole pesano come otto palline, una scatola pesa come quattro palline. Divido tutte e due le parti per due: x uguale quattro."):
            self.play(FadeOut(lb[1], shift=UP), FadeOut(rw[6:], shift=UP), run_time=1.0)
            self.play(TransformMatchingTex(eq3, eq4))
            self.play(Circumscribe(eq4, color=COL_RES))
        chk = M(r"3\cdot 4 + 2 = 14 \qquad 4 + 10 = 14 \ \checkmark", 44, COL_RES).move_to(P(0, 1.3))
        with self.say("Verifica: metto quattro al posto di x. A sinistra tre per quattro più due, quattordici. A destra quattro più dieci, quattordici. Giusto!"):
            self.play(Write(chk))
        self.wipe()
        rule = VGroup(MS(r"3x", r"+2", r"=", r"x", r"+10", fs=52),
                      MS(r"3x", r"-x", r"=", r"10", r"-2", fs=52),
                      MS(r"2x", r"=", r"8", fs=52), MS(r"x", r"=", r"4", fs=52, col=COL_RES)).arrange(DOWN, buff=0.35).move_to(P(-2.4, 0.3))
        rule[1][1].set_color(COL_AUX)
        rule[1][4].set_color(COL_AUX)
        txt = VGroup(T("Togliere x da tutte e due le parti", 26), T("è come «spostarlo» cambiando segno:", 26),
                     T("+x a destra diventa −x a sinistra.", 26, COL_AUX)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(P(3.3, 0.4))
        with self.say("Sul quaderno scriviamo la stessa cosa più in fretta. Togliere x da tutte e due le parti è come spostarlo dall'altra parte cambiando il segno. Più x a destra diventa meno x a sinistra."):
            self.play(Write(rule[0]))
            self.play(TransformFromCopy(rule[0], rule[1]), FadeIn(txt, lag_ratio=0.3), run_time=1.6)
            self.play(Write(rule[2]))
            self.play(Write(rule[3]))
        self.end()


class V2_P2_Equazioni(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 2, "Equazioni e percentuali", 2, "Risolvere le equazioni"

    def construct(self):
        self.title_card()
        e1 = VGroup(M(r"3x-7=2x+5", 50), M(r"3x-2x=5+7", 50), M(r"x=12", 54, COL_RES),
                    M(r"\text{verifica: } 3\cdot12-7=29,\quad 2\cdot12+5=29\ \checkmark", 38, COL_RES)).arrange(DOWN, buff=0.35).move_to(P(0, 0.6))
        with self.say("Esercizio E uno: tre x meno sette uguale due x più cinque. Porto le x a sinistra e i numeri a destra, cambiando il segno a chi passa dall'altra parte."):
            self.play(Write(e1[0]))
            self.play(Write(e1[1]))
        with self.say("Tre x meno due x fa x; cinque più sette fa dodici. X uguale dodici. E la verifica: tutte e due le parti fanno ventinove."):
            self.play(Write(e1[2]))
            self.play(Write(e1[3]))
        self.wipe()

        e2 = VGroup(M(r"2(x+3)-3(x-1)=5-2x", 50),
                    M(r"2x+6\;\;-3x+3=5-2x", 50),
                    M(r"-x+9=5-2x", 50),
                    M(r"-x+2x=5-9", 50),
                    M(r"x=-4", 54, COL_RES)).arrange(DOWN, buff=0.3).move_to(P(-1.3, 0.4))
        with self.say("Esercizio E due, con le parentesi. Prima tolgo le parentesi moltiplicando."):
            self.play(Write(e2[0]))
            self.play(Write(e2[1]))
        trap = VGroup(T("Trappola!", 30, COL_ERR), M(r"-3(x-1) = -3x\,\mathbf{+}\,3", 42, COL_ERR),
                      T("il meno cambia tutti i segni", 24, COL_ERR)).arrange(DOWN, buff=0.25).move_to(P(4.2, 1.2))
        with self.say("Attenzione al meno davanti alla seconda parentesi: cambia tutti i segni dentro. Meno tre per meno uno fa più tre."):
            self.play(FadeIn(trap, lag_ratio=0.3))
        with self.say("Poi sommo i termini simili, porto le x a sinistra e i numeri a destra. X uguale meno quattro."):
            self.play(Write(e2[2]))
            self.play(Write(e2[3]))
            self.play(Write(e2[4]))
        self.wipe()

        e3 = VGroup(M(r"\frac{x-1}{2}+\frac{x}{3}=2+\frac{x+1}{6}", 52),
                    M(r"\cdot 6:\quad 3(x-1)+2x=12+(x+1)", 46),
                    M(r"3x-3+2x=x+13", 46), M(r"4x=16", 46), M(r"x=4", 54, COL_RES)).arrange(DOWN, buff=0.3).move_to(P(0, 0.3))
        with self.say("Esercizio E tre, con le frazioni. Il trucco è moltiplicare tutto per il minimo comune multiplo dei denominatori, che è sei. Così le frazioni spariscono."):
            self.play(Write(e3[0]))
            self.play(Write(e3[1]))
        with self.say("Anche il due va moltiplicato per sei, e diventa dodici. Poi si risolve come prima: quattro x uguale sedici, x uguale quattro."):
            self.play(Write(e3[2]))
            self.play(Write(e3[3]))
            self.play(Write(e3[4]))
        self.wipe()

        imp = VGroup(M(r"3x+1=3x+5", 46), M(r"0x=4", 46, COL_ERR), T("impossibile", 30, COL_ERR)).arrange(DOWN, buff=0.3).move_to(P(-3.2, 0.5))
        ind = VGroup(M(r"2(x+1)=2x+2", 46), M(r"0x=0", 46, COL_ANG), T("indeterminata", 30, COL_ANG)).arrange(DOWN, buff=0.3).move_to(P(3.2, 0.5))
        with self.say("Due casi speciali. Se alla fine resta zero x uguale quattro, nessun numero va bene, perché zero per qualsiasi cosa fa zero: l'equazione è impossibile."):
            self.play(Write(imp))
        with self.say("Se invece resta zero x uguale zero, ogni numero va bene: l'equazione è indeterminata."):
            self.play(Write(ind))
        self.end()


class V2_P3_Problemi(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 2, "Equazioni e percentuali", 3, "Problemi con le equazioni"

    def construct(self):
        self.title_card()
        q = VGroup(T("Il perimetro di un rettangolo è 56 cm.", 28), T("La base supera l'altezza di 8 cm.", 28)).arrange(DOWN, buff=0.12).move_to(P(0, 2.7))
        with self.say("Un problema: il perimetro di un rettangolo è cinquantasei centimetri e la base supera l'altezza di otto centimetri. Trova base, altezza e area."):
            self.play(FadeIn(q))
        s = 0.2
        rect = Rectangle(width=18 * s, height=10 * s, color=WHITE, stroke_width=3).set_fill(COL_GIV, 0.2).move_to(P(-3.2, 0.7))
        lh = M("x", 40, COL_ANG).next_to(rect, LEFT, buff=0.2)
        lbase = M("x+8", 40, COL_ANG).next_to(rect, DOWN, buff=0.2)
        with self.say("Primo passo: scelgo l'incognita. Chiamo x l'altezza; allora la base è x più otto."):
            self.play(Create(rect))
            self.play(Write(lh), Write(lbase))
        steps = VGroup(M(r"2\,(x + x + 8) = 56", 46), M(r"4x + 16 = 56", 46), M(r"4x = 40", 46), M(r"x = 10", 50, COL_RES)).arrange(DOWN, buff=0.3).move_to(P(3.0, 0.4))
        with self.say("Secondo passo: scrivo l'equazione. Il perimetro è due volte base più altezza, e deve fare cinquantasei."):
            self.play(Write(steps[0]))
        with self.say("Risolvo: quattro x più sedici uguale cinquantasei, quattro x uguale quaranta, x uguale dieci."):
            self.play(Write(steps[1]))
            self.play(Write(steps[2]))
            self.play(Write(steps[3]))
        res = VGroup(M(r"h = 10\ \text{cm} \qquad b = 18\ \text{cm}", 40, COL_RES), M(r"A = 10\cdot18 = 180\ \text{cm}^2", 40, COL_RES)).arrange(DOWN, buff=0.2)
        res.move_to(P(-3.2, -1.55))
        with self.say("Terzo passo: rispondo alla domanda. Altezza dieci centimetri, base diciotto, area centottanta centimetri quadrati. E controllo: due per ventotto fa proprio cinquantasei."):
            self.play(ReplacementTransform(lh, M("10", 40, COL_RES).move_to(lh)), ReplacementTransform(lbase, M("18", 40, COL_RES).move_to(lbase)))
            self.play(FadeIn(res))
        self.wipe()
        q2 = T("La somma di tre numeri consecutivi è 84.", 30).move_to(P(0, 2.4))
        st2 = VGroup(M(r"n + (n+1) + (n+2) = 84", 48), M(r"3n + 3 = 84", 48), M(r"n = 27", 50, COL_RES),
                     M(r"27,\ 28,\ 29", 54, COL_RES)).arrange(DOWN, buff=0.35).move_to(P(0, -0.1))
        with self.say("Un altro: la somma di tre numeri consecutivi è ottantaquattro. Se il primo è n, gli altri due sono n più uno e n più due."):
            self.play(FadeIn(q2))
            self.play(Write(st2[0]))
        with self.say("Tre n più tre uguale ottantaquattro, quindi n uguale ventisette. I numeri sono ventisette, ventotto e ventinove."):
            self.play(Write(st2[1]))
            self.play(Write(st2[2]))
            self.play(Write(st2[3]))
        self.end()


class V2_P4_Proporzioni(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 2, "Equazioni e percentuali", 4, "Proporzioni"

    def construct(self):
        self.title_card()
        pr = VGroup(M(r"6 : x = 9 : 12", 56),
                    M(r"9\cdot x = 6\cdot 12", 50),
                    M(r"x = \frac{72}{9} = 8", 52, COL_RES)).arrange(DOWN, buff=0.4).move_to(P(-2.6, 0.5))
        lab = VGroup(T("estremi: 6 e 12", 28, COL_GIV), T("medi: x e 9", 28, COL_ANG),
                     T("prodotto dei medi = prodotto degli estremi", 26, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(P(3.3, 0.8))
        with self.say("Una proporzione dice che due rapporti sono uguali: sei sta a x come nove sta a dodici."):
            self.play(Write(pr[0]))
        with self.say("I termini esterni si chiamano estremi, quelli in mezzo medi. La proprietà fondamentale: il prodotto dei medi è uguale al prodotto degli estremi."):
            self.play(FadeIn(lab, lag_ratio=0.4), run_time=1.6)
            self.play(Write(pr[1]))
        with self.say("Quindi nove x uguale settantadue, e x uguale otto."):
            self.play(Write(pr[2]))
        self.wipe()

        ax = Axes(x_range=[0, 24, 4], y_range=[0, 100, 20], x_length=6, y_length=4, tips=False,
                  axis_config={"color": GRAY_B, "stroke_width": 2, "include_numbers": True, "font_size": 22}).move_to(P(-2.8, 0.1))
        xl = T("km", 22, GRAY_B).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = T("minuti", 22, GRAY_B).next_to(ax.y_axis, UP, buff=0.1)
        with self.say("Un atleta corre a velocità costante: dodici chilometri in quarantotto minuti. In quanto tempo ne fa venti?"):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
        line = ax.plot(lambda k: 4 * k, x_range=[0, 24], color=COL_GIV, stroke_width=4)
        d1 = Dot(ax.c2p(12, 48), color=COL_GIV)
        d2 = Dot(ax.c2p(20, 80), color=COL_RES)
        with self.say("Se il tempo e la distanza crescono insieme, nello stesso rapporto, sono direttamente proporzionali. Il grafico è una retta che passa per l'origine."):
            self.play(FadeIn(d1))
            self.play(Create(line), run_time=1.6)
        dl = VGroup(DashedLine(ax.c2p(20, 0), ax.c2p(20, 80), color=COL_RES), DashedLine(ax.c2p(0, 80), ax.c2p(20, 80), color=COL_RES))
        eqs = VGroup(M(r"12 : 48 = 20 : x", 42), M(r"x = \frac{48\cdot 20}{12} = 80", 42, COL_RES),
                     M(r"\frac{48}{12} = 4\ \text{min/km}", 40, COL_ANG)).arrange(DOWN, buff=0.35).move_to(P(3.8, 0.6))
        with self.say("La proporzione: dodici sta a quarantotto come venti sta a x. X uguale ottanta minuti. Il rapporto è costante: quattro minuti per ogni chilometro."):
            self.play(Write(eqs[0]))
            self.play(Create(dl), FadeIn(d2), Write(eqs[1]))
            self.play(Write(eqs[2]))
        self.wipe()

        # inverse proportion: same area
        s = 0.28
        o = P(-4.2, -2.0)
        r1 = Rectangle(width=6 * s, height=10 * s, color=COL_ANG2, stroke_width=3).set_fill(COL_ANG2, 0.35)
        r1.move_to(o, aligned_edge=DL)
        l1w = M(r"6\ \text{operai}", 30).next_to(r1, DOWN, buff=0.12)
        l1h = M(r"10\ \text{giorni}", 30).next_to(r1, LEFT, buff=0.12)
        with self.say("Adesso un caso diverso. Sei operai costruiscono un muro in dieci giorni. Quanti giorni servono a quattro operai?"):
            self.play(DrawBorderThenFill(r1), FadeIn(l1w), FadeIn(l1h))
        area = M(r"6\cdot 10 = 60", 40, COL_ANG).move_to(P(3.2, 1.8))
        with self.say("Qui, meno operai vuol dire più giorni. Resta costante il lavoro totale: sei per dieci, sessanta giornate di lavoro. È l'area del rettangolo."):
            self.play(Write(area))
        r2 = Rectangle(width=4 * s, height=15 * s, color=COL_RES, stroke_width=3).set_fill(COL_RES, 0.35).move_to(o, aligned_edge=DL)
        l2w = M("4", 30).next_to(r2, DOWN, buff=0.12)
        l2h = M("15", 30).next_to(r2, LEFT, buff=0.12)
        area2 = M(r"4\cdot x = 60 \ \Rightarrow\ x = 15", 42, COL_RES).next_to(area, DOWN, buff=0.4)
        with self.say("Con quattro operai il rettangolo diventa più stretto e più alto, ma l'area resta sessanta: quattro per x uguale sessanta, x uguale quindici giorni."):
            self.play(ReplacementTransform(r1, r2), ReplacementTransform(l1w, l2w), ReplacementTransform(l1h, l2h), run_time=2.0)
            self.play(Write(area2))
        kinds = VGroup(T("diretta: il rapporto è costante", 28, COL_GIV), T("inversa: il prodotto è costante", 28, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(area2, DOWN, buff=0.6)
        with self.say("Questa è la proporzionalità inversa: il prodotto è costante. Nella diretta, invece, è costante il rapporto."):
            self.play(FadeIn(kinds, lag_ratio=0.4))
        wrong = M(r"6 : 10 = 4 : x \ \Rightarrow\ x \approx 6{,}7\ ?", 36, COL_ERR).next_to(kinds, DOWN, buff=0.35)
        wrong.shift(LEFT * max(0, wrong.get_right()[0] - 6.7))
        with self.say("Attenzione: se usi la proporzione diretta ottieni meno giorni con meno operai. È assurdo! Chiediti sempre: se una cresce, l'altra cresce o cala?"):
            self.play(Write(wrong))
            self.play(Create(Cross(wrong, stroke_color=COL_ERR, stroke_width=4)))
        self.end()


class V2_P5_Percentuali(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 2, "Equazioni e percentuali", 5, "Percentuali e sconti"

    def construct(self):
        self.title_card()
        g = unit_squares(10, 10, 0.34, P(-6.0, -1.9), GRAY_D, 0.25, 1)
        with self.say("Per cento vuol dire su cento. Prendi un quadrato diviso in cento quadretti."):
            self.play(FadeIn(g, lag_ratio=0.005), run_time=1.4)
        f15 = VGroup(*[g[k] for k in range(15)])
        p = M(r"15\% = \frac{15}{100}", 50, COL_ANG).move_to(P(2.6, 2.0))
        with self.say("Quindici per cento vuol dire quindici quadretti su cento."):
            self.play(f15.animate.set_fill(COL_ANG, 0.8), run_time=1.2)
            self.play(Write(p))
        c = VGroup(M(r"15\%\ \text{di}\ 240 = \frac{15}{100}\cdot 240 = 36", 42),
                   M(r"\frac{18}{72}\cdot 100 = 25\%", 42),
                   M(r"30\%\ \text{di}\ x = 45 \Rightarrow x = \frac{45\cdot100}{30} = 150", 38)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(P(2.4, 0.0))
        with self.say("Il quindici per cento di duecentoquaranta: duecentoquaranta per quindici centesimi, trentasei."):
            self.play(Write(c[0]))
        with self.say("Diciotto su settantadue, quanto per cento? Diciotto diviso settantadue per cento: venticinque per cento, un quarto."):
            self.play(Write(c[1]))
        with self.say("E se il trenta per cento di un numero è quarantacinque? Il numero è quarantacinque per cento diviso trenta: centocinquanta."):
            self.play(Write(c[2]))
        self.wipe()

        # the shoes: reverse percentage with a bar model
        q = VGroup(T("Scarpe scontate del 20%: costano 170 €.", 30), T("Quanto costavano prima?", 30)).arrange(DOWN, buff=0.12).move_to(P(0, 2.95))
        with self.say("Adesso il problema delle scarpe del tuo quaderno. Dopo uno sconto del venti per cento costano centosettanta euro. Quanto costavano prima?"):
            self.play(FadeIn(q))
        W = 9.0
        parts = VGroup(*[Rectangle(width=W / 5, height=0.8, color=WHITE, stroke_width=2).set_fill(COL_GIV, 0.45).move_to(P(-4.5 + W / 10 + k * W / 5, 0.7)) for k in range(5)])
        tags = VGroup(*[M(r"20\%", 30).move_to(parts[k]) for k in range(5)])
        full = BraceLabel(parts, r"100\% = \ ?", UP, font_size=34)
        with self.say("Il prezzo iniziale è il cento per cento. Lo divido in cinque parti da venti per cento."):
            self.play(FadeIn(parts, lag_ratio=0.2), FadeIn(tags, lag_ratio=0.2), run_time=1.4)
        with self.say("Lo sconto toglie una parte. Restano quattro parti, cioè l'ottanta per cento, e valgono centosettanta euro."):
            self.play(parts[4].animate.set_fill(COL_ERR, 0.6), run_time=0.8)
            b80 = BraceLabel(VGroup(*parts[:4]), r"80\% = 170\ \text{euro}", DOWN, font_size=34)
            self.play(FadeIn(b80))
        one = M(r"20\% = 170 : 4 = 42{,}50\ \text{euro}", 42, COL_ANG).move_to(P(0, -1.2))
        tot = M(r"100\% = 42{,}50\cdot 5 = 212{,}50\ \text{euro}", 46, COL_RES).move_to(P(0, -2.0))
        with self.say("Una parte vale centosettanta diviso quattro: quarantadue euro e cinquanta. Il prezzo iniziale è cinque parti: duecentododici euro e cinquanta."):
            self.play(Write(one))
            self.play(Write(tot))
            self.play(FadeIn(full))
        self.wipe()
        wrong = VGroup(T("Trappola!", 32, COL_ERR), M(r"170 + 20\%\ \text{di}\ 170 = 204\ \text{euro}", 42, COL_ERR),
                       T("Il 20% si calcola sul prezzo iniziale, non su quello scontato.", 26, COL_ERR)).arrange(DOWN, buff=0.3).move_to(P(0, 1.6))
        with self.say("Attenzione: molti fanno centosettanta più il venti per cento di centosettanta, e trovano duecentoquattro. È sbagliato, perché lo sconto era il venti per cento del prezzo iniziale, non di quello scontato."):
            self.play(FadeIn(wrong, lag_ratio=0.3))
        seq = VGroup(M(r"80", 48), M(r"\xrightarrow{+10\%}", 40, COL_RES), M(r"88", 48), M(r"\xrightarrow{-10\%}", 40, COL_ERR), M(r"79{,}20", 48, COL_ANG)).arrange(RIGHT, buff=0.3).move_to(P(0, -0.8))
        with self.say("Per lo stesso motivo, se un prezzo di ottanta euro aumenta del dieci per cento e poi cala del dieci per cento, non torna a ottanta: diventa ottantotto e poi settantanove e venti. Il secondo dieci per cento si calcola su un numero più grande."):
            self.play(FadeIn(seq, lag_ratio=0.3), run_time=2.0)
        self.end()


class V2_P6_Esercizi(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 2, "Equazioni e percentuali", 6, "Riepilogo ed esercizi"

    def construct(self):
        self.header()
        items = [(r"\text{Equazione: stessa operazione da tutte e due le parti}", COL_GIV),
                 (r"\text{Si sposta un termine cambiando segno}", COL_AUX),
                 (r"a:b=c:d\ \Rightarrow\ a\cdot d = b\cdot c", COL_ANG),
                 (r"\text{diretta: } \tfrac{y}{x}=k \qquad \text{inversa: } x\cdot y = k", COL_RES),
                 (r"p\%\ \text{di}\ N = \tfrac{p}{100}\cdot N", COL_ANG2)]
        col = lines_column(items, 38, 0.4).move_to(P(0, 0.4))
        with self.say("Ricapitoliamo. L'equazione è una bilancia: stessa operazione da tutte e due le parti. Nelle proporzioni, prodotto dei medi uguale prodotto degli estremi. Diretta: rapporto costante; inversa: prodotto costante. E la percentuale si calcola sempre sull'intero giusto."):
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in col], lag_ratio=0.5), run_time=4)
        self.wait(0.6)
        self.wipe(keep_header=False)
        self.exercises([("E1", COL_GIV), ("E2", COL_GIV), ("E3", COL_GIV), ("E4", COL_ERR), ("P1", COL_ANG), ("P2", COL_ANG),
                        ("P3", COL_ANG), ("P4", COL_ANG), ("P5", COL_ERR), ("X1", COL_ERR)],
                       "Adesso tocca a te. Nel file degli esercizi fai le sezioni tre e quattro: da E uno a E quattro e da P uno a P cinque. Quando ti senti pronta, prova anche il quesito X uno della simulazione d'esame.",
                       ["• Fai sempre la verifica delle equazioni", "• Chiediti: diretta o inversa?", "• Controlla con il file delle soluzioni"])


if __name__ == "__main__":
    from fractions import Fraction as Fr
    ok = True

    def check(name, got, want):
        global ok
        good = abs(float(got) - float(want)) < 1e-9
        ok &= good
        print(("OK  " if good else "BAD ") + f"{name}: {got} (expected {want})")
    x = 4
    check("balance", 3 * x + 2, x + 10)
    check("E1", 3 * 12 - 7, 2 * 12 + 5)
    x = -4
    check("E2", 2 * (x + 3) - 3 * (x - 1), 5 - 2 * x)
    x = Fr(4)
    check("E3", (x - 1) / 2 + x / 3, 2 + (x + 1) / 6)
    check("rect", 2 * (10 + 18), 56)
    check("rect area", 10 * 18, 180)
    check("consecutive", 27 + 28 + 29, 84)
    check("P1", Fr(6 * 12, 9), 8)
    check("athlete", Fr(48 * 20, 12), 80)
    check("workers", Fr(60, 4), 15)
    check("wrong direct", round(10 * 4 / 6, 1), 6.7)
    check("15% of 240", Fr(15, 100) * 240, 36)
    check("18/72", Fr(18, 72) * 100, 25)
    check("30% -> 45", Fr(4500, 30), 150)
    check("shoes part", Fr(170, 4), Fr(85, 2))
    check("shoes", Fr(170, 4) * 5, Fr(425, 2))
    check("shoes wrong", 170 * 1.2, 204)
    check("80 +10%", 80 * 1.1, 88)
    check("88 -10%", 88 * 0.9, 79.2)
    print("ALL OK" if ok else "SOME CHECKS FAILED")
