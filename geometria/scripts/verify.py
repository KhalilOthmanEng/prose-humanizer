"""Independent verification of every number and figure coordinate in the booklet.

Run:  python3 scripts/verify.py
Every value printed here is the source of a  % VERIFIED  comment in the .tex files.
"""
from math import atan2, cos, degrees, hypot, isclose, radians, sin, sqrt

ok = True


def check(label, got, want, tol=1e-9):
    global ok
    good = isclose(got, want, abs_tol=tol)
    ok &= good
    print(f"[{'OK ' if good else 'BAD'}] {label}: {got!r} (expected {want!r})")


# ---------------------------------------------------------------- chapter 1
divisors = [d for d in range(1, 361) if 360 % d == 0]
print("divisors of 360:", divisors)
check("number of divisors of 360", len(divisors), 24)
for n, want in [(2, 180), (3, 120), (4, 90), (5, 72), (6, 60), (8, 45), (9, 40), (10, 36), (12, 30)]:
    check(f"360/{n}", 360 / n, want)
check("100/3", round(100 / 3, 2), 33.33)
check("100/6", round(100 / 6, 2), 16.67)
check("100/8", 100 / 8, 12.5)

# pie chart: 30 students
votes = {"pizza": 12, "pasta": 9, "gelato": 6, "altro": 3}
tot = sum(votes.values())
check("pie total", tot, 30)
deg = {k: v / tot * 360 for k, v in votes.items()}
for k, want in zip(votes, [144, 108, 72, 36]):
    check(f"pie {k} degrees", deg[k], want)
for k, want in zip(votes, [40, 30, 20, 10]):
    check(f"pie {k} percent", votes[k] / tot * 100, want)
check("pie degrees sum", sum(deg.values()), 360)
check("25% of 360", 0.25 * 360, 90)
check("1% of 360", 0.01 * 360, 3.6)
check("1 degree in percent", 100 / 360, 0.2777777777777778)

# pie chart from 40 students (exercise 1.3): 14, 10, 8, 8
ex = [14, 10, 8, 8]
check("exercise pie total", sum(ex), 40)
for v, want in zip(ex, [126, 90, 72, 72]):
    check(f"exercise pie {v}/40 -> deg", v / 40 * 360, want)


# clocks: minute hand 6 deg/min, hour hand 30 deg/h + 0.5 deg/min
def clock(h, m):
    hour = (h % 12) * 30 + 0.5 * m
    minute = 6 * m
    a = abs(hour - minute) % 360
    return min(a, 360 - a), hour, minute


check("clock 3:00", clock(3, 0)[0], 90)
check("clock 4:00", clock(4, 0)[0], 120)
a, hh, mm = clock(2, 30)
check("clock 2:30 hour hand", hh, 75)
check("clock 2:30 minute hand", mm, 180)
check("clock 2:30 angle", a, 105)
check("clock 9:00 convex", clock(9, 0)[0], 90)
check("clock 6:00", clock(6, 0)[0], 180)
check("clock 1:00", clock(1, 0)[0], 30)
a, hh, mm = clock(10, 10)
check("clock 10:10 hour hand", hh, 305)
check("clock 10:10 minute hand", mm, 60)
check("clock 10:10 angle", a, 115)
a, hh, mm = clock(7, 20)
check("clock 7:20 angle (exercise)", a, 100)

# complements, supplements, explements
check("complement of 35", 90 - 35, 55)
check("supplement of 128", 180 - 128, 52)
check("explement of 250", 360 - 250, 110)
check("complement of 72 (ex)", 90 - 72, 18)
check("supplement of 72 (ex)", 180 - 72, 108)
check("explement of 72 (ex)", 360 - 72, 288)
# x + 2x = 90
x = 90 / 3
check("x+2x=90", x, 30)
check("2x", 2 * x, 60)
# supplementary, differ by 40
x = (180 - 40) / 2
check("supp differ 40 small", x, 70)
check("supp differ 40 big", x + 40, 110)
# complement = supplement / 4 -> 90-x = (180-x)/4 -> 360-4x = 180-x -> x = 60
x = 60
check("complement=supp/4 lhs", 90 - x, 30)
check("complement=supp/4 rhs", (180 - x) / 4, 30)
# exercise: angle equal to its complement -> 45 ; angle 3 times its supplement -> 135
check("3x = 180 - x -> x", 180 / 4 * 3, 135)
check("supplement of 135 * 3", (180 - 135) * 3, 135)
# vertical angles
check("vertical angle partner of 40", 180 - 40, 140)

# parallels
check("parallel 65 partner", 180 - 65, 115)
x = (40 - 10) / (3 - 2)
check("alternate 3x+10=2x+40 -> x", x, 30)
check("alternate angle value", 3 * x + 10, 100)
check("alternate angle value (other side)", 2 * x + 40, 100)
x = (180 - 20 - 40) / 3
check("co-interior (2x+20)+(x+40)=180 -> x", x, 40)
check("co-interior first", 2 * x + 20, 100)
check("co-interior second", x + 40, 80)
# exercise: corresponding 5x-20 = 3x+30 -> x=25, angle 105
x = (30 + 20) / (5 - 3)
check("corresponding exercise x", x, 25)
check("corresponding exercise angle", 5 * x - 20, 105)

# ---------------------------------------------------------------- chapter 2
check("third angle 50,60", 180 - 50 - 60, 70)
check("isosceles vertex 40 -> base", (180 - 40) / 2, 70)
check("isosceles base 35 -> vertex", 180 - 2 * 35, 110)
check("right triangle 28 -> other", 90 - 28, 62)
check("exterior angle 50+60", 50 + 60, 110)
check("exterior angle = 180 - 70", 180 - 70, 110)
# exercise: angles in ratio 2:3:4 -> 40, 60, 80
k = 180 / (2 + 3 + 4)
check("ratio 2:3:4 k", k, 20)
# exercise: isosceles vertex angle double of base -> x + x + 2x = 180 -> 45,45,90
check("isosceles vertex double base", 180 / 4, 45)

# 3-4-5 triangle
check("3-4-5 right?", 3 ** 2 + 4 ** 2, 5 ** 2)
area = 3 * 4 / 2
check("3-4-5 area", area, 6)
check("altitude to 5", 2 * area / 5, 2.4)
check("area with base 5 height 2.4", 5 * 2.4 / 2, 6)
# base 10 height 6 -> area 30 ; altitude to side 12 -> 5
check("area 10x6/2", 10 * 6 / 2, 30)
check("altitude to 12", 2 * 30 / 12, 5)

# ---------------------------------------------------------------- chapter 3
# equal area, not congruent: legs 4,3 vs 6,2
check("area 4x3/2", 4 * 3 / 2, 6)
check("area 6x2/2", 6 * 2 / 2, 6)
check("hyp 4,3", hypot(4, 3), 5)
print("hyp 6,2 =", round(hypot(6, 2), 3))

# SSA ambiguity: angle A = 30 deg, AB = 6, BC = 4.  C on the ray from A at 30 deg.
# |t*u - B|^2 = 16  ->  t^2 - 12 cos30 t + 20 = 0
b = 12 * cos(radians(30))
disc = b * b - 4 * 20
t1, t2 = (b + sqrt(disc)) / 2, (b - sqrt(disc)) / 2
print(f"SSA: AC = {t1:.3f} or {t2:.3f}")
for t in (t1, t2):
    C = (t * cos(radians(30)), t * sin(radians(30)))
    check(f"SSA |BC| for AC={t:.3f}", hypot(C[0] - 6, C[1]), 4)
    print(f"   C = ({C[0]:.3f}, {C[1]:.3f})")


# ---------------------------------------------------------------- figure helpers
def foot(P, A, B):
    """foot of perpendicular from P to line AB"""
    ax, ay = A
    bx, by = B
    px, py = P
    dx, dy = bx - ax, by - ay
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    return (ax + t * dx, ay + t * dy)


def inter(P1, P2, P3, P4):
    x1, y1 = P1
    x2, y2 = P2
    x3, y3 = P3
    x4, y4 = P4
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d
    return (px, py)


def orthocentre(A, B, C):
    Ha = foot(A, B, C)
    Hb = foot(B, A, C)
    return inter(A, Ha, B, Hb), Ha, Hb, foot(C, A, B)


def fmt(P):
    return f"({P[0]:.3f},{P[1]:.3f})"


def ang(P, Q, R):
    """angle PQR in degrees"""
    a1 = atan2(P[1] - Q[1], P[0] - Q[0])
    a2 = atan2(R[1] - Q[1], R[0] - Q[0])
    d = abs(degrees(a1 - a2)) % 360
    return min(d, 360 - d)


print("\n--- figure: three altitudes ---")
for name, (A, B, C) in {
    "acute": ((0, 0), (4, 0), (1.6, 3.0)),
    "right": ((0, 0), (4, 0), (0, 3.0)),
    "obtuse": ((0, 0), (3.2, 0), (-1.4, 2.2)),
}.items():
    H, Ha, Hb, Hc = orthocentre(A, B, C)
    print(name, "A,B,C =", fmt(A), fmt(B), fmt(C))
    print("   foot from A on BC:", fmt(Ha), " from B on AC:", fmt(Hb), " from C on AB:", fmt(Hc))
    print("   orthocentre:", fmt(H))
    # the third altitude must pass through H: C, Hc, H collinear
    cross = (Hc[0] - C[0]) * (H[1] - C[1]) - (Hc[1] - C[1]) * (H[0] - C[0])
    check(f"{name}: third altitude passes through H", cross, 0, 1e-9)
    print("   angles:", round(ang(B, A, C), 2), round(ang(A, B, C), 2), round(ang(A, C, B), 2))

print("\n--- figure: 3-4-5 triangle with altitude to hypotenuse ---")
A, B, C = (0, 0), (4, 0), (0, 3)  # right angle at A, legs 4 and 3, hypotenuse BC = 5
Ha = foot(A, B, C)
print("foot on hypotenuse:", fmt(Ha), " altitude length:", round(hypot(*Ha), 4))
check("altitude to hypotenuse", hypot(*Ha), 2.4)

print("\n--- figure: isosceles with medians AM, BN (notebook problem B) ---")
A, B, C = (0, 0), (4, 0), (2, 4.5)
M = ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
N = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2)
G = inter(A, M, B, N)
print("M", fmt(M), "N", fmt(N), "G", fmt(G))
check("G is centroid x", G[0], (A[0] + B[0] + C[0]) / 3)
check("G is centroid y", G[1], (A[1] + B[1] + C[1]) / 3)
check("AN = BM", hypot(N[0] - A[0], N[1] - A[1]), hypot(M[0] - B[0], M[1] - B[1]))
check("GN = GM", hypot(N[0] - G[0], N[1] - G[1]), hypot(M[0] - G[0], M[1] - G[1]))
check("AG = BG", hypot(G[0] - A[0], G[1] - A[1]), hypot(G[0] - B[0], G[1] - B[1]))
check("angle NAG = MBG", ang(N, A, G), ang(M, B, G))
check("angle ANG = BMG", ang(A, N, G), ang(B, M, G))

print("\n--- figure: isosceles, extensions beyond A (notebook problem A) ---")
A, B, C = (0, 3.0), (-1.5, 0), (1.5, 0)
k = 0.45  # AD = AE = k * AB, on the extensions beyond A
D = (A[0] + k * (A[0] - B[0]), A[1] + k * (A[1] - B[1]))
E = (A[0] + k * (A[0] - C[0]), A[1] + k * (A[1] - C[1]))
print("D", fmt(D), "E", fmt(E))
check("BD = CE", hypot(D[0] - B[0], D[1] - B[1]), hypot(E[0] - C[0], E[1] - C[1]))
check("BE = CD", hypot(E[0] - B[0], E[1] - B[1]), hypot(D[0] - C[0], D[1] - C[1]))

print("\n--- figure: isosceles altitude (main proof) ---")
A, B, C = (2, 3.4), (0, 0), (4, 0)
H = foot(A, B, C)
print("H", fmt(H))
check("BH = HC", hypot(H[0] - B[0], H[1] - B[1]), hypot(C[0] - H[0], C[1] - H[1]))

print("\n--- figure: parallel lines worked example 65 deg ---")
# lines y=0 and y=2, transversal through (0,0) at 65 deg
t = 2 / sin(radians(65))
P2 = (t * cos(radians(65)), 2)
print("upper crossing:", fmt(P2))

print("\n--- figure: X shape with parallels (proof 5) ---")
# A=(0,2), B=(2.2,2) top line; D=(4,0), C=(1.8,0) bottom; O midpoint of AD
A, D = (0, 2), (4, 0)
O = ((A[0] + D[0]) / 2, (A[1] + D[1]) / 2)
B = (2.2, 2)
# line through B and O meets y=0 at C
C = inter(B, O, (0, 0), (1, 0))
print("O", fmt(O), "C", fmt(C))
check("BO = OC", hypot(B[0] - O[0], B[1] - O[1]), hypot(C[0] - O[0], C[1] - O[1]))


print("\n--- chapter 2 figures ---")
# triangle with angles 50 (A), 60 (B), 70 (C), AB = 4
from math import sin as _s
AC = 4 * sin(radians(60)) / sin(radians(70))
C = (AC * cos(radians(50)), AC * sin(radians(50)))
print("50-60-70 triangle: AC =", round(AC, 4), " C =", fmt(C))
check("angle at A", ang((4, 0), (0, 0), C), 50, 1e-6)
check("angle at B", ang((0, 0), (4, 0), C), 60, 1e-6)
check("angle at C", ang((0, 0), C, (4, 0)), 70, 1e-6)
check("exterior angle at B = A + C", 180 - 60, 50 + 70)

# obtuse triangle for the altitude figure
A, B, C = (0, 0), (3.4, 0), (-0.7, 2.4)
H, Ha, Hb, Hc = orthocentre(A, B, C)
print("obtuse (fig): feet", fmt(Ha), fmt(Hb), fmt(Hc), " orthocentre", fmt(H))
print("   angle at A =", round(ang(B, A, C), 2))
check("obtuse orthocentre formula y = -cx(cx-b)/cy", H[1], -(-0.7) * (-0.7 - 3.4) / 2.4)

# altitude, median, bisector from C in a scalene triangle
A, B, C = (0, 0), (5.5, 0), (1.2, 3.2)
CA, CB = hypot(*C), hypot(C[0] - 5.5, C[1])
AD = 5.5 * CA / (CA + CB)
print("scalene: CA =", round(CA, 4), "CB =", round(CB, 4), "bisector foot D = (", round(AD, 4), ", 0 )",
      " median foot M = (2.75, 0)  altitude foot H = (1.2, 0)")
check("bisector: angle ACD = angle DCB", ang(A, C, (AD, 0)), ang((AD, 0), C, B), 1e-9)

# 3-4-5 in three positions
A1, B1, C1 = (3.2, 2.4), (0, 0), (5, 0)
check("rotated 3-4-5: B'A' = 4", hypot(*A1), 4)
check("rotated 3-4-5: A'C' = 3", hypot(A1[0] - 5, A1[1]), 3)
check("rotated 3-4-5: height = 2.4", A1[1], 2.4)

# triangle inequality examples
check("2 + 3 < 7", 2 + 3 < 7, True)
check("3 + 4 > 5", 3 + 4 > 5, True)

print("\n--- chapter 3 figures ---")
# criteria figure: A(0,0), B(3.4,0), angle A = 55, AC = 2.5
Cc = (2.5 * cos(radians(55)), 2.5 * sin(radians(55)))
check("criteria fig BC", round(hypot(3.4 - Cc[0], Cc[1]), 3), 2.839)
check("criteria fig angle B", round(ang((0, 0), (3.4, 0), Cc), 1), 46.2)
check("equilateral height 3.2", round(3.2 * sin(radians(60)), 3), 2.771)
check("equilateral height 1.6", round(1.6 * sin(radians(60)), 3), 1.386)
# P1: X shape, O common midpoint
A, B, O = (0, 0), (4, 2), (2, 1)
C = (0.6, 2.2); D = (2 * O[0] - C[0], 2 * O[1] - C[1])
print("P1: D =", fmt(D))
check("P1 AO = OB", hypot(O[0]-A[0], O[1]-A[1]), hypot(B[0]-O[0], B[1]-O[1]))
check("P1 CO = OD", hypot(O[0]-C[0], O[1]-C[1]), hypot(D[0]-O[0], D[1]-O[1]))
check("P1 AC = BD", hypot(C[0]-A[0], C[1]-A[1]), hypot(D[0]-B[0], D[1]-B[1]))
# P2: kite
A, C, B, D = (0, 0), (4, 0), (1.2, 1.4), (1.2, -1.4)
check("P2 AB = AD", hypot(*B), hypot(*D))
check("P2 angle BAC = DAC", ang(B, A, C), ang(D, A, C))
# P4/P5 isosceles, vertex A=(2,3.4), B=(0,0), C=(4,0): bisector foot = altitude foot = (2,0)
A, B, C = (2, 3.4), (0, 0), (4, 0)
check("P4 angle B = angle C", ang(A, B, C), ang(A, C, B))
check("P5 angle BAH = CAH", ang(B, A, (2, 0)), ang(C, A, (2, 0)))
# P6 extra: angle BAE = angle CAD (vertical angles)
A, B, C = (0, 3.0), (-1.5, 0), (1.5, 0)
D, E = (0.675, 4.35), (-0.675, 4.35)
check("P6 angle BAE = CAD", ang(B, A, E), ang(C, A, D))
# SSA figure scaled points
print("SSA figure: C1 = (6.791, 3.921), C2 = (2.209, 1.275); both at distance 4 from B = (6,0)")
# exercise D5: perpendiculars from A and B to a line through midpoint M
A, B = (0, 0), (4, 0); M = (2, 0)
r_dir = (cos(radians(35)), sin(radians(35)))
H = foot(A, M, (M[0] + r_dir[0], M[1] + r_dir[1]))
K = foot(B, M, (M[0] + r_dir[0], M[1] + r_dir[1]))
print("D5: H =", fmt(H), " K =", fmt(K))
check("D5 AH = BK", hypot(H[0]-A[0], H[1]-A[1]), hypot(K[0]-B[0], K[1]-B[1]))
# exercise D2: equilateral, AD = BE = CF -> DEF equilateral
A, B, C = (0, 0), (4, 0), (2, 2 * sqrt(3))
t = 0.3
D = (A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1]))
E = (B[0] + t * (C[0] - B[0]), B[1] + t * (C[1] - B[1]))
F = (C[0] + t * (A[0] - C[0]), C[1] + t * (A[1] - C[1]))
de, ef, fd = hypot(E[0]-D[0], E[1]-D[1]), hypot(F[0]-E[0], F[1]-E[1]), hypot(D[0]-F[0], D[1]-F[1])
check("D2 DE = EF", de, ef); check("D2 EF = FD", ef, fd)
print("D2: D", fmt(D), "E", fmt(E), "F", fmt(F))
# exercise D1: isosceles base BC, AD = AE on the legs -> BE = CD
A, B, C = (2, 3.4), (0, 0), (4, 0)
k = 0.4
D = (A[0] + k * (B[0] - A[0]), A[1] + k * (B[1] - A[1]))
E = (A[0] + k * (C[0] - A[0]), A[1] + k * (C[1] - A[1]))
check("D1 BE = CD", hypot(E[0]-B[0], E[1]-B[1]), hypot(D[0]-C[0], D[1]-C[1]))
print("D1: D", fmt(D), "E", fmt(E))
# exercise: vertical angles 4x+10 = 2x+50 -> x = 20 -> 90
check("vertical 4x+10=2x+50 -> x", (50 - 10) / 2, 20)
check("exercise 118 partner", 180 - 118, 62)

print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
