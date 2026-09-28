"""Independent check of every number in the worksheets (esercizi.tex / soluzioni.tex).

Run:  python3 verifica.py      Exact arithmetic with Fraction wherever possible.
Each block is labelled with the exercise id used in contenuto.tex.
"""
from fractions import Fraction as F
from math import gcd, isclose, pi, sqrt

ok = True


def check(label, got, want, tol=1e-9):
    global ok
    if isinstance(got, F) or isinstance(want, F):
        good = F(got) == F(want)
    elif isinstance(got, (bool, str)) or isinstance(want, (bool, str)):
        good = got == want
    else:
        good = isclose(got, want, abs_tol=tol)
    ok &= good
    print(f"[{'OK ' if good else 'BAD'}] {label}: {got} (expected {want})")


def lcm(a, b):
    return a * b // gcd(a, b)


# ── N  numeri naturali ────────────────────────────────────────────────
check("N1 distributiva", 7 * (10 + 3), 7 * 10 + 7 * 3)
check("N1 invariantiva", F(36, 4), F(36 // 2, 4 // 2))
check("N2 mcm(12,18)", lcm(12, 18), 36)
check("N2 MCD(48,72)", gcd(48, 72), 24)
check("N2 penne per astuccio", 48 // 24, 2)
check("N2 matite per astuccio", 72 // 24, 3)

# ── F  frazioni e potenze ─────────────────────────────────────────────
f1 = (F(3, 4) + F(1, 6)) * F(6, 11) - F(1, 3)
check("F1 3/4+1/6", F(3, 4) + F(1, 6), F(11, 12))
check("F1 risultato", f1, F(1, 6))
check("F2a 2^3*2^4:2^5", F(2**3 * 2**4, 2**5), 4)
check("F2b (3^2)^3:3^4", F((3**2) ** 3, 3**4), 9)
check("F2c (2/5)^3*(5/2)^3", F(2, 5) ** 3 * F(5, 2) ** 3, 1)
check("F2d (-2)^3", (-2) ** 3, -8)
check("F2d (-2)^4", (-2) ** 4, 16)
check("F2d -2^4", -(2**4), -16)
check("F2d (-1/3)^2", F(-1, 3) ** 2, F(1, 9))
f3 = (F(5, 3) ** 4 / F(5, 3) ** 2) * F(9, 25) + F(1, 2) ** 2
check("F3 risultato", f3, F(5, 4))
check("F4 0,(3)", F(3, 9), F(1, 3))
check("F4 1,2(5)", F(125 - 12, 90), F(113, 90))
check("F4 1,2(5) decimale", float(F(113, 90)), 1.2555555555555555)
check("F4 0,(45)", F(45, 99), F(5, 11))
check("F4 sqrt(9/25)", F(3, 5) ** 2, F(9, 25))
check("F4 sqrt(0,49)", 0.7**2, 0.49)
check("F4 7^2 < 50 < 8^2", 49 < 50 < 64, True)
inner = (1 - F(1, 4)) * (1 + F(1, 3)) - F(1, 2) ** 2
check("F5 parentesi quadra", inner, F(3, 4))
check("F5 : (3/4)^2", inner / F(3, 4) ** 2, F(4, 3))
check("F5 graffa", inner / F(3, 4) ** 2 + F(-2, 3) ** 2, F(16, 9))
f5 = (inner / F(3, 4) ** 2 + F(-2, 3) ** 2) * F(9, 16) - F(-1, 2) ** 3
check("F5 risultato", f5, F(9, 8))

# ── E  equazioni ──────────────────────────────────────────────────────
check("E1a x=12", 3 * 12 - 7, 2 * 12 + 5)
check("E1b x=7", 4 * (7 - 2), 2 * 7 + 6)
x = -4
check("E2 x=-4 LHS=RHS", 2 * (x + 3) - 3 * (x - 1), 5 - 2 * x)
check("E2 value", 5 - 2 * x, 13)
x = F(4)
check("E3 x=4", (x - 1) / 2 + x / 3, 2 + (x + 1) / 6)
check("E3 value", (x - 1) / 2 + x / 3, F(17, 6))
h = F(56 - 16, 4)
check("E4a altezza", h, 10)
check("E4a base", h + 8, 18)
check("E4a perimetro", 2 * (h + h + 8), 56)
check("E4a area", h * (h + 8), 180)
check("E4b consecutivi", 27 + 28 + 29, 84)

# ── P  proporzioni e percentuali ──────────────────────────────────────
check("P1a 6:x=9:12", F(6 * 12, 9), 8)
check("P1b x:5=14:10", F(5 * 14, 10), 7)
check("P1c (x+2):x=5:3 -> x=3", F(3 + 2, 3), F(5, 3))
check("P2a 15% di 240", F(15, 100) * 240, 36)
check("P2b 18 su 72", F(18, 72) * 100, 25)
check("P2c 30% di x = 45", F(45 * 100, 30), 150)
check("P3 prezzo iniziale", F(170 * 100, 80), F(425, 2))
check("P3 = 212,50", float(F(170 * 100, 80)), 212.5)
check("P3 controllo sconto", 212.5 * 0.8, 170)
check("P3b +10%", 80 * 1.1, 88)
check("P3b -10%", 88 * 0.9, 79.2)
check("P4 10 ore", 1.5 / 4 * 10, 3.75)
check("P4 60%", 3.75 * 0.60, 2.25)
check("P4 costo", 2.25 * 0.28, 0.63)
check("P5a 20 km", F(48 * 20, 12), 80)
check("P5a costante min/km", F(48, 12), 4)
check("P5b 4 operai", F(6 * 10, 4), 15)
check("P5b costante", 6 * 10, 60)

# ── S  statistica e probabilità ───────────────────────────────────────
voti = [6, 7, 5, 8, 7, 9, 7, 6]
check("S1 somma", sum(voti), 55)
check("S1 media", F(sum(voti), len(voti)), F(55, 8))
check("S1 media decimale", 55 / 8, 6.875)
s = sorted(voti)
check("S1 mediana", F(s[3] + s[4], 2), 7)
check("S1 moda", max(set(voti), key=voti.count), 7)
check("S1 campo", max(voti) - min(voti), 4)
libri = {"gialli": 96, "fantasy": 60, "storici": 48, "biografie": 36}
check("S2 totale", sum(libri.values()), 240)
for k, want_pct, want_deg in [("gialli", 40, 144), ("fantasy", 25, 90), ("storici", 20, 72), ("biografie", 15, 54)]:
    check(f"S2 {k} %", F(libri[k] * 100, 240), want_pct)
    check(f"S2 {k} gradi", F(libri[k] * 360, 240), want_deg)
check("S3 ottimo gradi", 360 - 150 - 120, 90)
for d, want in [(150, 30), (120, 24), (90, 18)]:
    check(f"S3 {d} gradi -> alunni", F(d * 72, 360), want)
check("S3 somma alunni", 30 + 24 + 18, 72)
check("S4 pari", F(3, 6), F(1, 2))
check("S4 >4", F(2, 6), F(1, 3))
check("S4 >4 %", round(100 / 3, 1), 33.3)
urna = {"rosse": 5, "blu": 3, "verdi": 2}
check("S5 totale", sum(urna.values()), 10)
check("S5 rossa", F(5, 10), F(1, 2))
check("S5 non blu", 1 - F(3, 10), F(7, 10))
check("S5 rossa o verde", F(5 + 2, 10), F(7, 10))
somma7 = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 7)
check("S5 casi somma 7", somma7, 6)
check("S5 P(somma 7)", F(somma7, 36), F(1, 6))
check("S5 P(doppio)", F(6, 36), F(1, 6))
check("S5 P(somma > 10)", F(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b > 10), 36), F(1, 12))

# ── C  piano cartesiano ───────────────────────────────────────────────
check("C1 base", 7 - 1, 6)
check("C1 altezza", 5 - 1, 4)
check("C1 perimetro", 2 * (6 + 4), 20)
check("C1 area", 6 * 4, 24)
check("C1 diagonale", sqrt(6**2 + 4**2), sqrt(52))
check("C1 diagonale ~", round(sqrt(52), 2), 7.21)
A, B, C = (-2, -1), (4, -1), (1, 3)
d = lambda P, Q: sqrt((P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2)
check("C2 AB", d(A, B), 6)
check("C2 AC", d(A, C), 5)
check("C2 BC", d(B, C), 5)
check("C2 perimetro", d(A, B) + d(A, C) + d(B, C), 16)
check("C2 area", 6 * 4 / 2, 12)
for xx in [1, 2, 3, 4, 6, 12]:
    check(f"C3 y=12/x at {xx}", F(12, xx) * xx, 12)
xi = F(6, 3)
check("C4 intersezione x", xi, 2)
check("C4 intersezione y r", 2 * xi - 1, 3)
check("C4 intersezione y s", -xi + 5, 3)
check("C4 P(4,7) su r", 2 * 4 - 1, 7)
check("C4 P(4,7) su s?", -4 + 5 == 7, False)
check("C4 r asse x", F(1, 2), F(1, 2))
check("C4 area triangolo", (5 - F(1, 2)) * 3 / 2, F(27, 4))

# ── A  angoli ─────────────────────────────────────────────────────────
check("A1 complementare 38", 90 - 38, 52)
check("A1 supplementare 38", 180 - 38, 142)
check("A1 esplementare 38", 360 - 38, 322)
xa = F(15 + 25, 5 - 3)
check("A2 x", xa, 20)
check("A2 angolo", 3 * xa + 15, 75)
check("A2 altro lato", 5 * xa - 25, 75)
check("A2 supplementare", 180 - 75, 105)
check("A3 x", F(200, 5), 40)
check("A3 altro", 4 * 40 - 20, 140)
check("A3 somma", 40 + 140, 180)
check("A3 ore 4:30 lancetta ore", 4 * 30 + 30 * 0.5, 135)
check("A3 ore 4:30 angolo", 180 - 135, 45)

# ── T  triangoli ──────────────────────────────────────────────────────
check("T1a", 180 - 47 - 68, 65)
check("T1b", F(180 - 36, 2), 72)
check("T1c", 90 - 25, 65)
check("T1d angolo B", 110 - 45, 65)
check("T1d angolo C interno", 180 - 110, 70)
check("T1d somma", 45 + 65 + 70, 180)

# ── G  Pitagora, poligoni, cerchio ────────────────────────────────────
check("G1 ipotenusa 9-12", sqrt(81 + 144), 15)
check("G1 perimetro", 9 + 12 + 15, 36)
check("G1 area", 9 * 12 / 2, 54)
check("G1 altezza relativa all'ipotenusa", 9 * 12 / 15, 7.2)
check("G1b cateto 26-10", sqrt(26**2 - 10**2), 24)
check("G2 altezza", sqrt(25**2 - 24**2), 7)
check("G2 perimetro", 2 * (24 + 7), 62)
check("G2 area", 24 * 7, 168)
check("G2 diagonale quadrato 5", round(5 * sqrt(2), 2), 7.07)
check("G4 lato rombo", sqrt(8**2 + 15**2), 17)
check("G4 perimetro", 4 * 17, 68)
check("G4 area", 16 * 30 / 2, 240)
check("G4 altezza", round(240 / 17, 2), 14.12)
proj = (22 - 10) / 2
check("G5 proiezione", proj, 6)
check("G5 altezza", sqrt(10**2 - 6**2), 8)
check("G5 area", (22 + 10) * 8 / 2, 128)
check("G5 perimetro", 22 + 10 + 2 * 10, 52)
check("G5 diagonale", round(sqrt(16**2 + 8**2), 2), 17.89)
check("G6 ipotenusa", sqrt(36 + 64), 10)
check("G6 C = 10 pi (3,14)", 10 * 3.14, 31.4)
check("G6 A = 25 pi (3,14)", 25 * 3.14, 78.5)
check("G6 area esterna", 78.5 - 24, 54.5)
check("G6 arco 72", 2 * 3.14 * 5 * 72 / 360, 6.28)
check("G6 settore 72", 3.14 * 25 * 72 / 360, 15.7)
circ = 70 * 3.14
check("G3 circonferenza cm", circ, 219.8)
check("G3 giri per 1 km", round(100000 / circ, 2), 454.96)

# ── V  solidi ─────────────────────────────────────────────────────────
a, b, c = 5, 3, 4
check("V1 Sb", a * b, 15)
check("V1 2p", 2 * (a + b), 16)
check("V1 Sl", 2 * (a + b) * c, 64)
check("V1 St", 2 * (a + b) * c + 2 * a * b, 94)
check("V1 St formula 2(ab+bc+ac)", 2 * (a * b + b * c + a * c), 94)
check("V1 V", a * b * c, 60)
check("V1 diagonale", round(sqrt(a * a + b * b + c * c), 2), 7.07)
check("V2 Sl cubo 6", 4 * 36, 144)
check("V2 St cubo 6", 6 * 36, 216)
check("V2 V cubo 6", 6**3, 216)
check("V2 diagonale", round(6 * sqrt(3), 2), 10.39)
check("V2 spigolo da V=125", round(125 ** (1 / 3), 9), 5)
check("V2 St cubo 5", 6 * 25, 150)
# V3: the student's exercise n.3 (2,5 x 4 x 6)
check("V3 2p", 2 * (2.5 + 4), 13)
check("V3 Sl", 13 * 6, 78)
check("V3 Sb", 2.5 * 4, 10)
check("V3 St", 78 + 2 * 10, 98)
check("V3 St formula", 2 * (2.5 * 4 + 4 * 6 + 2.5 * 6), 98)
check("V3 V", 2.5 * 4 * 6, 60)
# V4: room 5 x 4 x 2,8, walls + ceiling, door 0,9 x 2,1, window 1,2 x 1
walls = 2 * (5 + 4) * 2.8
check("V4 pareti", walls, 50.4)
check("V4 soffitto", 5 * 4, 20)
check("V4 porta", round(0.9 * 2.1, 2), 1.89)
check("V4 finestra", 1.2 * 1, 1.2)
area = walls + 20 - 1.89 - 1.2
check("V4 superficie", round(area, 2), 67.31)
litri = area / 8
check("V4 litri", round(litri, 2), 8.41)
check("V4 barattoli (frazione)", round(litri / 2.5, 2), 3.37)
check("V4 barattoli (interi)", -(-litri // 2.5), 4)
check("V4 spesa", 4 * 24, 96)
check("V4 pittura avanzata", round(4 * 2.5 - litri, 2), 1.59)
# V5: aquarium
check("V5 volume acqua cm3", 80 * 35 * 40, 112000)
check("V5 litri", 112000 / 1000, 112)
check("V5 volume vasca", 80 * 35 * 45 / 1000, 126)
check("V5 legno volume", 20 * 10 * 5, 1000)
check("V5 legno peso g", 1000 * 0.6, 600)
# V6: right prism, base right triangle 9, 12 ; h 10
ip = sqrt(81 + 144)
check("V6 ipotenusa", ip, 15)
check("V6 2p", 9 + 12 + 15, 36)
check("V6 Sb", 9 * 12 / 2, 54)
check("V6 Sl", 36 * 10, 360)
check("V6 St", 360 + 2 * 54, 468)
check("V6 V", 54 * 10, 540)
# V7: cylinder r4 h10 ; cone from triangle 6,8 rotating around the 6 leg -> r = 8, h = 6
check("V7a Sl cil (x pi)", 2 * 4 * 10, 80)
check("V7a Sb cil (x pi)", 4 * 4, 16)
check("V7a St cil (x pi)", 80 + 2 * 16, 112)
check("V7a V cil (x pi)", 16 * 10, 160)
check("V7a V cil ~", round(160 * 3.14, 1), 502.4)
check("V7a Sl cil ~", round(80 * 3.14, 1), 251.2)
check("V7a St cil ~", round(112 * 3.14, 2), 351.68)
check("V7b apotema", sqrt(8**2 + 6**2), 10)
check("V7b Sl cono (x pi)", 8 * 10, 80)
check("V7b Sb cono (x pi)", 64, 64)
check("V7b St cono (x pi)", 80 + 64, 144)
check("V7b V cono (x pi)", F(64 * 6, 3), 128)
check("V7b V cono ~", round(128 * 3.14, 2), 401.92)
check("V7b St cono ~", round(144 * 3.14, 2), 452.16)
check("V7b Sb cono ~", round(64 * 3.14, 2), 200.96)
check("X3 tabella A", [1.5 * x + 3 for x in (0, 2, 4, 6, 8)] == [3, 6, 9, 12, 15], True)
check("X3 tabella B", [2.5 * x for x in (0, 2, 4, 6, 8)] == [0, 5, 10, 15, 20], True)
check("X2 facce cubo visibili", 5 * 36, 180)

# ── X  simulazione ────────────────────────────────────────────────────
x1 = (F(2, 3) - F(1, 4)) * F(12, 5) + (F(1, 2)) ** 2 / F(1, 4)
check("X1a espressione", x1, 2)
x = F(14, 2)
check("X1b 3(x-2)+4 = 2x+5 -> x=7", 3 * (x - 2) + 4, 2 * x + 5)
apo = sqrt(4**2 + 3**2)
check("X2 apotema piramide", apo, 5)
check("X2 Sl piramide", 24 * 5 / 2, 60)
check("X2 St solido", 5 * 36 + 60, 240)
check("X2 V cubo", 216, 216)
check("X2 V piramide", 36 * 4 / 3, 48)
check("X2 V totale", 216 + 48, 264)
check("X2 peso", round(264 * 0.8, 1), 211.2)
check("X3 18 euro", F(18 - 3, F(3, 2)), 10)
check("X3 pareggio", F(3, F(5, 2) - F(3, 2)), 3)
check("X3 tariffa A 3 km", 3 + 1.5 * 3, 7.5)
check("X3 tariffa B 3 km", 2.5 * 3, 7.5)
check("X3 tariffa A 8 km", 3 + 1.5 * 8, 15)
check("X3 tariffa B 8 km", 2.5 * 8, 20)
fr = {0: 4, 1: 9, 2: 5, 3: 2}
n = sum(fr.values())
check("X4 n", n, 20)
check("X4 media", F(sum(k * v for k, v in fr.items()), n), F(5, 4))
dati = sorted(k for k, v in fr.items() for _ in range(v))
check("X4 mediana", F(dati[9] + dati[10], 2), 1)
check("X4 moda", max(fr, key=fr.get), 1)
for k, pc, gr in [(0, 20, 72), (1, 45, 162), (2, 25, 90), (3, 10, 36)]:
    check(f"X4 {k} fratelli %", F(fr[k] * 100, n), pc)
    check(f"X4 {k} fratelli gradi", F(fr[k] * 360, n), gr)
check("X4 P(almeno 2)", F(fr[2] + fr[3], n), F(7, 20))

print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
