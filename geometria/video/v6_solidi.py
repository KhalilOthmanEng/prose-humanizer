"""
Video 6 · Geometria solida
==========================
Scenes (render each with  manim -qh v6_solidi.py <Scene>):
  V6_P1_Parallelepipedo  the box: 3 pairs of faces, the net, lateral surface as one band, volume as unit cubes, diagonal
  V6_P2_Stanza           painting a room (exercise V4): walls, ceiling, door and window, litres, cans rounded up
  V6_P3_PrismaPiramide   prism V = Sb h; a pyramid fills a third of the prism; the composite solid of X2
  V6_P4_Rotazione        cylinder and cone from turning a rectangle and a triangle; the unrolled label
  V6_P5_Capacita         1 dm3 = 1 litre = 1000 cm3; the aquarium; weight = volume x specific weight
  V6_P6_Esercizi         summary and the matching exercises
"""
from comune import *

BOX = (5, 3, 4)            # a, b, c of exercise V1


class V6_P1_Parallelepipedo(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 6, "Geometria solida", 1, "Il parallelepipedo"

    def construct(self):
        self.video_card("parallelepipedo · prisma · piramide · cilindro · cono",
                        "Ciao! In questo ultimo video passiamo dal piano allo spazio: superfici e volumi dei solidi, con tanti problemi pratici.")
        self.header()
        a, b, c = BOX
        p = box_pts(P(-5.2, -1.6), a, b, c, s=0.55, ang=35, k=0.5)
        box = box_mob(p)
        dims = VGroup(M("a=5", 30).next_to(seg(p["A"], p["B"]), DOWN, buff=0.1),
                      M("b=3", 30).next_to(seg(p["B"], p["F"]), RIGHT, buff=0.05).shift(DOWN * 0.1),
                      M("c=4", 30).next_to(seg(p["A"], p["D"]), LEFT, buff=0.1))
        with self.say("Ecco un parallelepipedo rettangolo, come una scatola da scarpe: base cinque per tre e altezza quattro."):
            self.play(Create(box), run_time=1.6)
            self.play(FadeIn(dims))
        # six faces as polygons (front/back blue, top/bottom yellow, left/right green)
        faces = {
            "bottom": (["A", "B", "F", "E"], COL_ANG), "front": (["A", "B", "C", "D"], COL_GIV),
            "top": (["D", "C", "G", "H"], COL_ANG), "back": (["E", "F", "G", "H"], COL_GIV),
            "left": (["E", "A", "D", "H"], COL_RES), "right": (["B", "F", "G", "C"], COL_RES)}
        polys = {k: poly(*[p[n] for n in v], col=WHITE, fill=col, op=0.45, w=2) for k, (v, col) in faces.items()}
        with self.say("Ha sei facce, a coppie uguali: davanti e dietro, sopra e sotto, destra e sinistra."):
            self.play(FadeOut(box), *[FadeIn(polys[k]) for k in ("back", "bottom", "left")], run_time=0.6)
            self.play(*[FadeIn(polys[k]) for k in ("front", "right", "top")], run_time=0.8)
        # the net: unit 0.34, origin at the bottom left of the bottom face
        u = 0.34
        o = P(0.6, -2.5)

        def R(x0, y0, w, h):
            return [o + P(x0 * u, y0 * u), o + P((x0 + w) * u, y0 * u), o + P((x0 + w) * u, (y0 + h) * u), o + P(x0 * u, (y0 + h) * u)]
        net = {"bottom": R(0, 0, a, b), "front": R(0, b, a, c), "top": R(0, b + c, a, b), "back": R(0, 2 * b + c, a, c),
               "left": R(-b, b, b, c), "right": R(a, b, b, c)}
        targets = {k: poly(*net[k], col=WHITE, fill=faces[k][1], op=0.45, w=2) for k in net}
        with self.say("Se apro la scatola e la stendo sul tavolo ottengo lo sviluppo: sei rettangoli. La superficie totale è la somma delle loro aree."):
            self.play(*[TransformFromCopy(polys[k], targets[k]) for k in net], run_time=2.6)
        st = VGroup(M(r"S_t = 2(ab + bc + ac)", 38), M(r"= 2(15 + 12 + 20) = 94", 38, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(P(4.9, 0.9))
        with self.say("Due facce di cinque per tre, due di tre per quattro e due di cinque per quattro: la superficie totale è novantaquattro centimetri quadrati."):
            self.play(Write(st))
        self.wipe()

        # lateral surface as one band
        band = VGroup()
        widths = [(a, COL_GIV), (b, COL_RES), (a, COL_GIV), (b, COL_RES)]
        x = -5.6
        for w, col in widths:
            band.add(Rectangle(width=w * 0.42, height=c * 0.42, color=WHITE, stroke_width=2).set_fill(col, 0.45).move_to(P(x + w * 0.21, 0.8), aligned_edge=ORIGIN))
            x += w * 0.42
        br = Brace(band, DOWN, buff=0.1)
        brl = M(r"2p = 2(a+b) = 16", 34).next_to(br, DOWN, buff=0.1)
        hl = M("c = 4", 32).next_to(band, LEFT, buff=0.15)
        with self.say("Le quattro facce laterali, messe una accanto all'altra, formano un'unica striscia. È lunga quanto il perimetro di base, sedici, e alta quanto il solido, quattro."):
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.3) for r in band], lag_ratio=0.3), run_time=1.6)
            self.play(GrowFromCenter(br), FadeIn(brl), FadeIn(hl))
        sl = VGroup(M(r"S_\ell = 2p\cdot h = 16\cdot 4 = 64", 40, COL_GIV), M(r"S_t = S_\ell + 2S_b = 64 + 30 = 94", 40, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P(2.9, -1.9))
        with self.say("Superficie laterale: perimetro di base per altezza, sessantaquattro. Aggiungo le due basi, trenta, e ritrovo novantaquattro. Due modi, stesso risultato: è un ottimo controllo."):
            self.play(Write(sl[0]))
            self.play(Write(sl[1]))
        self.wipe()

        # volume with unit cubes
        s = 0.6
        o = P(-6.0, -1.9)
        layers = []
        for z in range(c):
            layer = VGroup()
            for d in reversed(range(b)):
                for x in range(a):
                    q = box_pts(o, x, d, z, s=s, ang=35, k=0.5)["A"]
                    origin = o + P(x * s, z * s) + 0.5 * s * d * unit(35)
                    layer.add(small_cube(origin, s=s, col=COL_GIV if z % 2 == 0 else COL_ANG))
            layers.append(layer)
        cnt = VGroup(M(r"\text{1 strato} = 5\cdot 3 = 15", 38), M(r"4\ \text{strati} = 15\cdot 4 = 60", 38, COL_RES),
                     M(r"V = a\cdot b\cdot c = 60\ \text{cm}^3", 42, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P(3.2, 0.9))
        with self.say("Il volume è quanti cubetti da un centimetro cubo riempiono la scatola. Sul fondo ci stanno cinque per tre, quindici cubetti."):
            self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.3) for k in layers[0]], lag_ratio=0.05), run_time=1.8)
            self.play(Write(cnt[0]))
        with self.say("Poi aggiungo un altro strato, e un altro, fino all'altezza quattro. Quattro strati da quindici: sessanta centimetri cubi."):
            for z in range(1, c):
                self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.3) for k in layers[z]], lag_ratio=0.02), run_time=1.0)
            self.play(Write(cnt[1]))
            self.play(Write(cnt[2]))
        self.wipe()

        # the diagonal: Pythagoras twice
        p = box_pts(P(-5.2, -1.8), a, b, c, s=0.6, ang=35, k=0.5)
        box = box_mob(p, fill=GRAY_D, op=0.15)
        dbase = Line(p["A"], p["F"], color=COL_ANG, stroke_width=4)
        dspace = Line(p["A"], p["G"], color=COL_ERR, stroke_width=5)
        up = DashedLine(p["F"], p["G"], color=COL_ERR)
        with self.say("Infine la diagonale, che attraversa la scatola da un angolo a quello opposto. Serve Pitagora due volte."):
            self.play(Create(box))
        d1 = M(r"d_{\text{base}} = \sqrt{5^2 + 3^2} = \sqrt{34}", 38, COL_ANG).move_to(P(3.0, 1.6))
        d2 = M(r"d = \sqrt{34 + 4^2} = \sqrt{50} \approx 7{,}07", 38, COL_ERR).move_to(P(3.0, 0.6))
        d3 = M(r"d = \sqrt{a^2 + b^2 + c^2}", 42, COL_RES).move_to(P(3.0, -0.6))
        with self.say("Prima la diagonale del fondo: radice di cinque al quadrato più tre al quadrato."):
            self.play(Create(dbase))
            self.play(Write(d1))
        with self.say("Poi un altro triangolo rettangolo, in piedi: la diagonale del fondo e l'altezza quattro. Radice di cinquanta, circa sette virgola zero sette."):
            self.play(Create(up), Create(dspace))
            self.play(Write(d2))
        with self.say("In una sola formula: radice di a al quadrato più b al quadrato più c al quadrato."):
            self.play(Write(d3))
        self.end()


class V6_P2_Stanza(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 6, "Geometria solida", 2, "Dipingere una stanza"

    def construct(self):
        self.title_card()
        q = VGroup(T("Stanza 5 m × 4 m, alta 2,8 m.", 28), T("Dipingo pareti e soffitto, non porta e finestra.", 28),
                   T("1 litro copre 8 m²; barattoli da 2,5 l a 24 €.", 28)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(P(2.8, 2.4))
        p = box_pts(P(-5.8, -1.4), 5, 4, 2.8, s=0.55, ang=35, k=0.5)
        room = box_mob(p, fill=COL_WOOD, op=0.15)
        with self.say("Un problema come quello del tuo quaderno. Una stanza è lunga cinque metri, larga quattro e alta due virgola otto. Bisogna dipingere le quattro pareti e il soffitto, ma non la porta e la finestra."):
            self.play(Create(room), FadeIn(q, lag_ratio=0.3), run_time=2.0)
        self.play(FadeOut(room), run_time=0.4)
        # walls as one band 18 x 2.8, scale 0.4
        k = 0.4
        x0, y0 = -6.6, -1.7
        band = VGroup()
        x = x0
        for w in (5, 4, 5, 4):
            band.add(Rectangle(width=w * k, height=2.8 * k, color=WHITE, stroke_width=2).set_fill(COL_GIV, 0.3).move_to(P(x + w * k / 2, y0 + 1.4 * k)))
            x += w * k
        door = Rectangle(width=0.9 * k, height=2.1 * k, color=WHITE, stroke_width=1.5).set_fill(COL_WOOD, 0.9).move_to(P(x0 + 1.2 * k, y0 + 1.05 * k))
        win = Rectangle(width=1.2 * k, height=1.0 * k, color=WHITE, stroke_width=1.5).set_fill(COL_ANG, 0.8).move_to(P(x0 + 7.0 * k, y0 + 1.6 * k))
        ceil = Rectangle(width=5 * k, height=4 * k, color=WHITE, stroke_width=2).set_fill(COL_RES, 0.3).move_to(P(x0 + 2.5 * k, y0 + 2.8 * k + 2 * k))
        with self.say("Srotolo le quattro pareti: una striscia lunga come il perimetro, diciotto metri, e alta due virgola otto."):
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in band], lag_ratio=0.25), run_time=1.6)
        c1 = VGroup(M(r"\text{pareti} = 2(5+4)\cdot 2{,}8 = 50{,}4\ \text{m}^2", 34),
                    M(r"\text{soffitto} = 5\cdot 4 = 20\ \text{m}^2", 34),
                    M(r"\text{porta} = 0{,}9\cdot 2{,}1 = 1{,}89\ \text{m}^2", 34),
                    M(r"\text{finestra} = 1{,}2\cdot 1 = 1{,}2\ \text{m}^2", 34),
                    M(r"50{,}4 + 20 - 1{,}89 - 1{,}2 = 67{,}31\ \text{m}^2", 34, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        c1.align_to(P(1.2, 0), LEFT).align_to(P(0, 1.55), UP)
        with self.say("Le pareti fanno diciotto per due virgola otto, cinquanta virgola quattro metri quadrati. Il soffitto, cinque per quattro, venti."):
            self.play(Write(c1[0]))
            self.play(FadeIn(ceil, shift=DOWN * 0.3), Write(c1[1]))
        with self.say("Tolgo la porta, uno virgola ottantanove, e la finestra, uno virgola due. Restano sessantasette virgola trentuno metri quadrati."):
            self.play(FadeIn(door), Write(c1[2]))
            self.play(FadeIn(win), Write(c1[3]))
            self.play(Write(c1[4]))
        self.wipe()
        l1 = VGroup(M(r"67{,}31 : 8 \approx 8{,}41\ \text{litri}", 42), M(r"8{,}41 : 2{,}5 \approx 3{,}37\ \text{barattoli}", 42)).arrange(DOWN, buff=0.35).move_to(P(0, 2.0))
        with self.say("Quanti litri? Sessantasette virgola trentuno diviso otto: circa otto virgola quarantuno litri. Diviso due virgola cinque: tre virgola trentasette barattoli."):
            self.play(Write(l1[0]))
            self.play(Write(l1[1]))
        cans = VGroup()
        for i in range(4):
            body = Rectangle(width=0.9, height=1.3, color=WHITE, stroke_width=2).move_to(P(-5.4 + 1.3 * i, -0.4))
            fill_h = 1.3 * min(1.0, max(0.0, 3.37 - i))
            paint = Rectangle(width=0.9, height=max(fill_h, 0.001), color=COL_GIV, stroke_width=0).set_fill(COL_GIV, 0.8).move_to(body.get_bottom(), aligned_edge=DOWN)
            cans.add(VGroup(paint, body))
        with self.say("Ma i barattoli non si comprano a pezzi. Con tre non basta la pittura: bisogna arrotondare per eccesso e comprarne quattro."):
            self.play(LaggedStart(*[FadeIn(cn) for cn in cans], lag_ratio=0.3), run_time=1.4)
        l2 = VGroup(M(r"4\cdot 24 = 96\ \text{euro}", 42, COL_RES), M(r"10 - 8{,}41 \approx 1{,}59\ \text{litri avanzano}", 38, COL_ANG)).arrange(DOWN, buff=0.3).move_to(P(2.6, -0.4))
        with self.say("Si spendono quattro per ventiquattro, novantasei euro, e avanzano circa uno virgola cinquantanove litri."):
            self.play(Write(l2[0]))
            self.play(Write(l2[1]))
        self.end()


class V6_P3_PrismaPiramide(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 6, "Geometria solida", 3, "Prisma e piramide"

    def construct(self):
        self.title_card()
        # right prism with a right triangle base 9, 12, height 10 (scale 0.2)
        k = 0.2
        A0 = P(-5.4, -1.8)
        B0 = A0 + P(9 * k, 0)
        C0 = A0 + P(0, 0) + 0.5 * 12 * k * unit(35)
        h = P(0, 10 * k)
        base = poly(A0, B0, C0, col=WHITE, fill=COL_ANG, op=0.6, w=2)
        with self.say("Un prisma retto ha due basi uguali e parallele e le facce laterali rettangolari. Questo ha per base un triangolo rettangolo con i cateti di nove e dodici."):
            self.play(DrawBorderThenFill(base))
        slices = VGroup(*[poly(A0 + h * t, B0 + h * t, C0 + h * t, col=WHITE, fill=COL_ANG, op=0.25, w=1) for t in np.linspace(0.1, 1, 10)])
        with self.say("Il volume si capisce impilando tante basi una sopra l'altra, fino all'altezza dieci: volume uguale area di base per altezza."):
            self.play(LaggedStart(*[FadeIn(sl, shift=UP * 0.2) for sl in slices], lag_ratio=0.15), run_time=2.0)
            self.play(Create(VGroup(seg(A0, A0 + h), seg(B0, B0 + h), DashedLine(C0, C0 + h, color=WHITE))))
        calc = VGroup(M(r"i = \sqrt{9^2 + 12^2} = 15", 36), M(r"S_b = \frac{9\cdot 12}{2} = 54", 36), M(r"S_\ell = 2p\cdot h = 36\cdot 10 = 360", 36),
                      M(r"S_t = 360 + 2\cdot 54 = 468", 36, COL_RES), M(r"V = S_b\cdot h = 54\cdot 10 = 540", 38, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(P(2.6, 0.4))
        with self.say("Per le superfici serve il perimetro di base, e quindi l'ipotenusa: quindici. Superficie laterale: trentasei per dieci, trecentosessanta. Totale: quattrocentosessantotto. Volume: cinquantaquattro per dieci, cinquecentoquaranta."):
            self.play(LaggedStart(*[Write(x) for x in calc], lag_ratio=0.5), run_time=4.0)
        self.wipe()

        # a pyramid is one third of the prism with the same base and height
        s = 0.5
        pb = box_pts(P(0.8, -1.9), 4, 4, 4, s=s, ang=35, k=0.5)
        prism = box_mob(pb, fill=GRAY_D, op=0.1)
        py = box_pts(P(-5.4, -1.9), 4, 4, 0, s=s, ang=35, k=0.5)
        apex = (py["A"] + py["F"]) / 2 + P(0, 4 * s)
        pyr = VGroup(DashedLine(py["E"], apex, color=WHITE, stroke_width=1.5), DashedLine(py["E"], py["F"], color=WHITE, stroke_width=1.5),
                     DashedLine(py["E"], py["A"], color=WHITE, stroke_width=1.5),
                     poly(py["A"], py["B"], apex, col=WHITE, fill=COL_GIV, op=0.45, w=2), poly(py["B"], py["F"], apex, col=WHITE, fill=COL_GIV, op=0.6, w=2))
        with self.say("Adesso una piramide e un prisma con la stessa base e la stessa altezza. Riempio la piramide d'acqua e la verso nel prisma."):
            self.play(Create(pyr), Create(prism), run_time=1.6)

        def water(level):
            w = box_pts(P(0.8, -1.9), 4, 4, level, s=s, ang=35, k=0.5)
            return VGroup(poly(w["A"], w["B"], w["C"], w["D"], col=COL_GIV, fill=COL_GIV, op=0.5, w=0),
                          poly(w["D"], w["C"], w["G"], w["H"], col=COL_GIV, fill=COL_GIV, op=0.35, w=0),
                          poly(w["B"], w["F"], w["G"], w["C"], col=COL_GIV, fill=COL_GIV, op=0.6, w=0))
        wat = water(0.01)
        self.add(wat)
        with self.say("Una volta, due volte, tre volte: il prisma è pieno. La piramide contiene esattamente un terzo del prisma."):
            for i in range(1, 4):
                arr = CurvedArrow(apex + P(0.2, 0.2), pb["H"] + P(0.3, 0.4), color=COL_GIV, angle=-PI / 3)
                self.play(Create(arr), run_time=0.5)
                self.play(Transform(wat, water(4 * i / 3)), FadeOut(arr), run_time=1.0)
        f = M(r"V_{\text{piramide}} = \frac{S_b\cdot h}{3}", 50, COL_RES).move_to(P(-2.0, 2.4))
        with self.say("Per questo il volume della piramide è area di base per altezza, diviso tre."):
            self.play(Write(f))
        self.wipe()

        # composite solid of X2: a cube of edge 6 with a pyramid of height 4
        s = 0.42
        cb = box_pts(P(-5.0, -2.0), 6, 6, 6, s=s, ang=35, k=0.5)
        cube = box_mob(cb, fill=COL_ANG, op=0.2)
        top_c = (cb["D"] + cb["G"]) / 2
        tip = top_c + P(0, 4 * s)
        mid_front = (cb["D"] + cb["C"]) / 2
        roof = VGroup(poly(cb["D"], cb["C"], tip, col=WHITE, fill=COL_GIV, op=0.45, w=2), poly(cb["C"], cb["G"], tip, col=WHITE, fill=COL_GIV, op=0.6, w=2))
        apo = Line(tip, mid_front, color=COL_ERR, stroke_width=4)
        hgt = DashedLine(tip, top_c, color=WHITE)
        with self.say("Il quesito X due della simulazione: un cubo di spigolo sei con sopra una piramide alta quattro."):
            self.play(Create(cube), Create(roof), run_time=1.6)
        ap = VGroup(M(r"a = \sqrt{4^2 + 3^2} = 5", 38, COL_ERR), M(r"S = 5\cdot 36 + \frac{24\cdot 5}{2} = 240", 38),
                    M(r"V = 6^3 + \frac{36\cdot 4}{3} = 216 + 48 = 264", 38, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(P(2.6, 0.6))
        with self.say("L'apotema della piramide è l'ipotenusa di un triangolo con l'altezza quattro e metà spigolo, tre: cinque."):
            self.play(Create(hgt), Create(apo))
            self.play(Write(ap[0]))
        with self.say("Nella superficie contano solo cinque facce del cubo, perché quella di sopra è coperta, più le facce della piramide: duecentoquaranta. Il volume è la somma dei due volumi: duecentosessantaquattro."):
            self.play(Write(ap[1]))
            self.play(Write(ap[2]))
        self.end()


class V6_P4_Rotazione(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 6, "Geometria solida", 4, "Cilindro e cono"

    def construct(self):
        self.title_card()
        s = 0.28
        ax_x = -3.8
        yb = -1.5
        r, h = 4 * s, 10 * s
        axis = DashedLine(P(ax_x, yb - 0.4), P(ax_x, yb + h + 0.5), color=COL_ERR)
        phi = ValueTracker(0)

        def rect():
            c = np.cos(phi.get_value())
            return Polygon(P(ax_x, yb), P(ax_x + r * c, yb), P(ax_x + r * c, yb + h), P(ax_x, yb + h), color=COL_ANG, stroke_width=3).set_fill(COL_ANG, 0.5)
        rm = always_redraw(rect)
        with self.say("Un rettangolo di lati quattro e dieci gira attorno al lato di dieci, come una porta attorno ai cardini."):
            self.play(Create(axis), FadeIn(rm))
        ghosts = VGroup(*[Polygon(P(ax_x, yb), P(ax_x + r * np.cos(a), yb), P(ax_x + r * np.cos(a), yb + h), P(ax_x, yb + h),
                                  color=COL_ANG, stroke_width=1, stroke_opacity=0.4) for a in np.linspace(0, 2 * PI, 13)])
        with self.say("Facendo un giro completo descrive un cilindro. Il lato che gira diventa l'altezza, l'altro lato il raggio."):
            self.play(phi.animate.set_value(2 * PI), FadeIn(ghosts), run_time=3.2, rate_func=linear)
        cyl = VGroup(Ellipse(width=2 * r, height=0.5, color=COL_GIV, stroke_width=3).move_to(P(ax_x, yb + h)),
                     Line(P(ax_x - r, yb), P(ax_x - r, yb + h), color=COL_GIV, stroke_width=3),
                     Line(P(ax_x + r, yb), P(ax_x + r, yb + h), color=COL_GIV, stroke_width=3),
                     Arc(radius=1, start_angle=PI, angle=PI, color=COL_GIV, stroke_width=3).stretch(r, 0).stretch(0.25, 1).move_to(P(ax_x, yb - 0.125)),
                     DashedVMobject(Arc(radius=1, start_angle=0, angle=PI, color=COL_GIV, stroke_width=2).stretch(r, 0).stretch(0.25, 1).move_to(P(ax_x, yb + 0.125)), num_dashes=12))
        with self.say("Ecco il cilindro, con raggio quattro e altezza dieci."):
            self.play(FadeOut(ghosts), FadeOut(rm), Create(cyl), run_time=1.4)
        # the label unrolled
        lab = Rectangle(width=2 * PI * r * 0.55, height=h, color=WHITE, stroke_width=2).set_fill(COL_GIV, 0.35).move_to(P(1.2, yb + h / 2))
        bw = Brace(lab, DOWN, buff=0.08)
        with self.say("Se srotolo l'etichetta del cilindro ottengo un rettangolo: la base è la circonferenza, due pi greco r, l'altezza è h."):
            self.play(TransformFromCopy(cyl[1], lab), run_time=1.6)
            self.play(GrowFromCenter(bw), FadeIn(M(r"2\pi r", 32).next_to(bw, DOWN, buff=0.08)), FadeIn(M("h", 32).next_to(lab, LEFT, buff=0.1)))
        f = VGroup(M(r"S_\ell = 2\pi r h = 80\pi \approx 251{,}2", 34, COL_GIV), M(r"S_t = S_\ell + 2\pi r^2 = 112\pi \approx 351{,}68", 34),
                   M(r"V = \pi r^2 h = 160\pi \approx 502{,}4", 36, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        f.align_to(P(-0.2, 0), LEFT).align_to(P(0, 3.3), UP)
        with self.say("Superficie laterale due pi greco r h, ottanta pi greco. Aggiungo i due cerchi di base: centododici pi greco. Volume: area di base per altezza, centosessanta pi greco, circa cinquecentodue virgola quattro."):
            self.play(LaggedStart(*[Write(x) for x in f], lag_ratio=0.5), run_time=3.2)
        self.wipe()

        # cone
        rr, hh = 8 * 0.34, 6 * 0.34
        axx, y0 = -3.7, -1.4
        axis = DashedLine(P(axx, y0 - 0.4), P(axx, y0 + hh + 0.5), color=COL_ERR)
        phi2 = ValueTracker(0)
        tri = always_redraw(lambda: Polygon(P(axx, y0), P(axx + rr * np.cos(phi2.get_value()), y0), P(axx, y0 + hh), color=COL_ANG, stroke_width=3).set_fill(COL_ANG, 0.5))
        with self.say("Ora un triangolo rettangolo con i cateti sei e otto gira attorno al cateto di sei."):
            self.play(Create(axis), FadeIn(tri))
        with self.say("Descrive un cono. Il cateto sull'asse è l'altezza, sei; l'altro cateto è il raggio, otto; l'ipotenusa è l'apotema."):
            self.play(phi2.animate.set_value(2 * PI), run_time=3.0, rate_func=linear)
        cone = VGroup(Line(P(axx - rr, y0), P(axx, y0 + hh), color=COL_GIV, stroke_width=3), Line(P(axx + rr, y0), P(axx, y0 + hh), color=COL_GIV, stroke_width=3),
                      Arc(radius=1, start_angle=PI, angle=PI, color=COL_GIV, stroke_width=3).stretch(rr, 0).stretch(0.3, 1).move_to(P(axx, y0 - 0.15)),
                      DashedVMobject(Arc(radius=1, start_angle=0, angle=PI, color=COL_GIV, stroke_width=2).stretch(rr, 0).stretch(0.3, 1).move_to(P(axx, y0 + 0.15)), num_dashes=14))
        self.play(FadeOut(tri), Create(cone))
        g = VGroup(M(r"a = \sqrt{8^2 + 6^2} = 10", 36, COL_ERR), M(r"S_\ell = \pi r a = 80\pi \approx 251{,}2", 34),
                   M(r"S_t = 80\pi + 64\pi = 144\pi \approx 452{,}16", 34), M(r"V = \frac{\pi r^2 h}{3} = 128\pi \approx 401{,}92", 36, COL_RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(P(3.2, 0.7))
        with self.say("Apotema: radice di sessantaquattro più trentasei, dieci. Superficie laterale pi greco r per apotema, ottanta pi greco; totale centoquarantaquattro pi greco."):
            self.play(Write(g[0]))
            self.play(Write(g[1]))
            self.play(Write(g[2]))
        with self.say("E il volume, come per la piramide, è un terzo del cilindro con la stessa base e la stessa altezza: centoventotto pi greco."):
            self.play(Write(g[3]))
        trap = T("Il cateto sull'asse è l'altezza, l'altro è il raggio.", 26, COL_ERR).move_to(P(3.0, -1.5))
        with self.say("Attenzione: il cateto attorno a cui il triangolo gira è sempre l'altezza del cono."):
            self.play(FadeIn(trap))
        self.end()


class V6_P5_Capacita(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 6, "Geometria solida", 5, "Capacità e peso"

    def construct(self):
        self.title_card()
        p = box_pts(P(-5.4, -1.8), 10, 10, 10, s=0.26, ang=35, k=0.5)
        cube = box_mob(p, fill=COL_GIV, op=0.25)
        grid = VGroup(*[Line(p["A"] + P(i * 0.26, 0), p["D"] + P(i * 0.26, 0), color=COL_GIV, stroke_width=0.6) for i in range(1, 10)],
                      *[Line(p["A"] + P(0, i * 0.26), p["B"] + P(0, i * 0.26), color=COL_GIV, stroke_width=0.6) for i in range(1, 10)])
        eq = VGroup(M(r"1\ \text{dm}^3 = 10\cdot10\cdot10\ \text{cm}^3 = 1000\ \text{cm}^3", 38), M(r"1\ \text{dm}^3 = 1\ \text{litro}", 44, COL_RES),
                    M(r"1\ \text{litro d'acqua pesa}\ 1\ \text{kg}", 38, COL_ANG)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(P(2.6, 1.2))
        with self.say("Un cubo di dieci centimetri di spigolo, cioè un decimetro, contiene mille cubetti da un centimetro cubo."):
            self.play(Create(cube), Create(grid), run_time=1.6)
            self.play(Write(eq[0]))
        with self.say("Un decimetro cubo è esattamente un litro. E un litro d'acqua pesa un chilogrammo."):
            self.play(Write(eq[1]))
            self.play(Write(eq[2]))
        self.wipe()
        s = 0.045
        pa = box_pts(P(-5.6, -1.6), 80, 35, 45, s=s, ang=35, k=0.5)
        tank = box_mob(pa, fill=GRAY_D, op=0.08)
        pw = box_pts(P(-5.6, -1.6), 80, 35, 40, s=s, ang=35, k=0.5)
        water = VGroup(poly(pw["A"], pw["B"], pw["C"], pw["D"], col=COL_GIV, fill=COL_GIV, op=0.45, w=0),
                       poly(pw["D"], pw["C"], pw["G"], pw["H"], col=COL_GIV, fill=COL_GIV, op=0.3, w=0),
                       poly(pw["B"], pw["F"], pw["G"], pw["C"], col=COL_GIV, fill=COL_GIV, op=0.55, w=0))
        with self.say("Un acquario lungo ottanta centimetri, largo trentacinque e alto quarantacinque, riempito fino a cinque centimetri dal bordo."):
            self.play(Create(tank))
            self.play(FadeIn(water, shift=UP * 0.3))
        c = VGroup(M(r"\text{acqua alta } 45 - 5 = 40\ \text{cm}", 36), M(r"V = 80\cdot 35\cdot 40 = 112\,000\ \text{cm}^3", 36),
                   M(r"= 112\ \text{dm}^3 = 112\ \text{litri}", 38, COL_RES), M(r"\text{peso} = 112\ \text{kg}", 38, COL_ANG)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(P(2.9, 0.6))
        with self.say("L'acqua è alta quaranta centimetri, non quarantacinque. Volume: ottanta per trentacinque per quaranta, centododicimila centimetri cubi."):
            self.play(Write(c[0]))
            self.play(Write(c[1]))
        with self.say("Divido per mille: centododici decimetri cubi, cioè centododici litri. E pesano centododici chilogrammi."):
            self.play(Write(c[2]))
            self.play(Write(c[3]))
        self.wipe()
        f = VGroup(M(r"P = V\cdot p_s", 56, COL_RES), M(r"V = 20\cdot 10\cdot 5 = 1000\ \text{cm}^3", 40),
                   M(r"P = 1000\cdot 0{,}6 = 600\ \text{g}", 44, COL_ANG)).arrange(DOWN, buff=0.4).move_to(P(0, 0.6))
        with self.say("Per gli altri materiali si usa il peso specifico: il peso è volume per peso specifico. Un blocco di legno di venti per dieci per cinque centimetri, con peso specifico zero virgola sei grammi al centimetro cubo, pesa seicento grammi."):
            self.play(Write(f[0]))
            self.play(Write(f[1]))
            self.play(Write(f[2]))
        self.end()


class V6_P6_Esercizi(LessonScene):
    VIDEO, VTITLE, PART, TITLE = 6, "Geometria solida", 6, "Riepilogo ed esercizi"

    def construct(self):
        self.header()
        items = [(r"S_\ell = 2p\cdot h \qquad S_t = S_\ell + 2S_b", COL_GIV),
                 (r"\text{prisma, cilindro: } V = S_b\cdot h", COL_ANG),
                 (r"\text{piramide, cono: } V = \frac{S_b\cdot h}{3}", COL_RES),
                 (r"1\ \text{dm}^3 = 1\ \text{litro} \qquad P = V\cdot p_s", COL_ERR)]
        col = lines_column(items, 40, 0.45).move_to(P(0, 0.4))
        with self.say("Ricapitoliamo. La superficie laterale è perimetro di base per altezza. Prisma e cilindro: volume uguale base per altezza. Piramide e cono: un terzo. E un decimetro cubo è un litro."):
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in col], lag_ratio=0.5), run_time=4)
        self.wait(0.6)
        self.wipe(keep_header=False)
        self.exercises([("V1", COL_GIV), ("V2", COL_GIV), ("V3", COL_ANG), ("V4", COL_ANG), ("V5", COL_ANG), ("V6", COL_ANG), ("V7", COL_ERR), ("X2", COL_ERR)],
                       "Adesso tocca a te. Nel file degli esercizi fai la sezione dieci, da V uno a V sette, e il quesito X due della simulazione. Con questo hai visto tutto il programma dell'esame!",
                       ["• Disegna sempre il solido", "• Controlla le superfici in due modi", "• Controlla con il file delle soluzioni"])


if __name__ == "__main__":
    from math import sqrt, pi
    ok = True

    def check(name, got, want, tol=1e-9):
        global ok
        good = abs(got - want) < tol
        ok &= good
        print(("OK  " if good else "BAD ") + f"{name}: {got} (expected {want})")
    a, b, c = BOX
    check("St", 2 * (a * b + b * c + a * c), 94)
    check("Sl", 2 * (a + b) * c, 64)
    check("V", a * b * c, 60)
    check("diag", round(sqrt(a * a + b * b + c * c), 2), 7.07)
    walls = 2 * (5 + 4) * 2.8
    check("walls", walls, 50.4)
    area = walls + 20 - 0.9 * 2.1 - 1.2
    check("paint area", round(area, 2), 67.31)
    check("litres", round(area / 8, 2), 8.41)
    check("cans", round(area / 8 / 2.5, 2), 3.37)
    check("leftover", round(10 - area / 8, 2), 1.59)
    check("prism hyp", sqrt(81 + 144), 15)
    check("prism Sl", 36 * 10, 360)
    check("prism St", 360 + 108, 468)
    check("prism V", 54 * 10, 540)
    check("X2 apothem", sqrt(16 + 9), 5)
    check("X2 S", 5 * 36 + 24 * 5 / 2, 240)
    check("X2 V", 216 + 36 * 4 / 3, 264)
    check("cyl V", round(160 * 3.14, 1), 502.4)
    check("cyl St", round(112 * 3.14, 2), 351.68)
    check("cone a", sqrt(64 + 36), 10)
    check("cone V", round(128 * 3.14, 2), 401.92)
    check("cone St", round(144 * 3.14, 2), 452.16)
    check("aquarium", 80 * 35 * 40, 112000)
    check("wood", 1000 * 0.6, 600)
    print("ALL OK" if ok else "SOME CHECKS FAILED")
