"""Python AST validation for generated Manim scene code.

Two layers, no execution and no Manim install required:

1. Security policy (ported from Math-To-Manim, math_to_manim/tools/ast_validation.py):
   parse the source and flag forbidden imports (os, sys, subprocess, ...) and
   forbidden calls (eval, exec, open, subprocess.run, ...). Generated scene
   code should never touch the filesystem, network, or shell.

2. Manim anti-pattern linter (added for this skill): statically detect the
   crash patterns enumerated in SKILL.md PART I before a single frame renders:
     - VGroup(*self.mobjects)            -> RULE 1
     - math/underscore inside Text(...)  -> RULE 2
     - raw Unicode math inside MathTex   -> RULE 2
     - stroke_dasharray=                 -> RULE 7
     - interpolate_color("#hex", ...)    -> RULE 8
     - obj.always_redraw(...)            -> RULE 10
     - np.trapz(...)                     -> RULE 11

This is the engine behind the §7.4 validate-then-render gate. Use it through
gate.py, or call validate_scene_source(source) directly.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Literal


Severity = Literal["error", "warning"]

# Unicode characters that crash LaTeX inside MathTex/Tex (use macros instead).
_UNICODE_MATH = set(
    "\u0391\u0392\u0393\u0394\u0395\u0396\u0397\u0398\u0399\u039a\u039b\u039c"
    "\u039d\u039e\u039f\u03a0\u03a1\u03a3\u03a4\u03a5\u03a6\u03a7\u03a8\u03a9"
    "\u03b1\u03b2\u03b3\u03b4\u03b5\u03b6\u03b7\u03b8\u03b9\u03ba\u03bb\u03bc"
    "\u03bd\u03be\u03bf\u03c0\u03c1\u03c2\u03c3\u03c4\u03c5\u03c6\u03c7\u03c8"
    "\u03c9\u2192\u2190\u2191\u2193\u2194\u21d2\u21d0\u21d4\u2211\u220f\u222b"
    "\u221a\u221e\u2202\u2207\u2248\u2260\u2264\u2265\u00b1\u00d7\u00f7\u22c5"
)
_MATH_TEXT_CLASSES = {"MathTex", "Tex"}


@dataclass(frozen=True)
class ValidationIssue:
    severity: Severity
    code: str
    message: str
    lineno: int = 0
    col_offset: int = 0


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    issues: tuple[ValidationIssue, ...] = ()
    tree: ast.Module | None = field(default=None, repr=False, compare=False)

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return tuple(i for i in self.issues if i.severity == "error")

    @property
    def warnings(self) -> tuple[ValidationIssue, ...]:
        return tuple(i for i in self.issues if i.severity == "warning")

    def report(self) -> str:
        if not self.issues:
            return "OK: no issues."
        lines = []
        for i in self.issues:
            mark = "ERROR" if i.severity == "error" else "warn "
            loc = f"L{i.lineno}" if i.lineno else "-"
            lines.append(f"  [{mark}] {loc} {i.code}: {i.message}")
        head = "FAIL" if not self.ok else "PASS (warnings only)"
        return f"{head}\n" + "\n".join(lines)


@dataclass(frozen=True)
class PythonAstPolicy:
    """Policy knobs. Dangerous roots are errors; merely-unusual imports warn.

    This deviates intentionally from the upstream M2M policy, which errored on
    any import outside an allowlist. For a personal engineering skill that
    legitimately reaches for scipy, pandas, etc., a hard allowlist blocks too
    much; the safety-critical roots remain errors.
    """

    forbidden_import_roots: tuple[str, ...] = (
        "builtins", "importlib", "os", "pathlib", "runpy",
        "shutil", "socket", "subprocess", "sys",
    )
    expected_import_roots: tuple[str, ...] = (
        "manim", "numpy", "math", "itertools", "functools",
        "dataclasses", "collections", "typing", "random",
    )
    forbidden_call_names: tuple[str, ...] = (
        "__import__", "breakpoint", "compile", "eval", "exec", "input", "open",
        "os.popen", "os.system", "subprocess.Popen", "subprocess.call",
        "subprocess.check_call", "subprocess.check_output", "subprocess.run",
    )
    max_source_bytes: int = 1_000_000
    max_ast_nodes: int = 50_000


DEFAULT_POLICY = PythonAstPolicy()


def validate_scene_source(
    source: str,
    *,
    filename: str = "<generated>",
    policy: PythonAstPolicy = DEFAULT_POLICY,
) -> ValidationResult:
    """Parse and validate a generated Manim scene without executing it."""

    issues: list[ValidationIssue] = []
    if len(source.encode("utf-8")) > policy.max_source_bytes:
        issues.append(ValidationIssue(
            "error", "source-too-large",
            f"Source exceeds {policy.max_source_bytes} bytes"))
        return ValidationResult(False, tuple(issues), None)

    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError as exc:
        issues.append(ValidationIssue(
            "error", "syntax-error", exc.msg,
            lineno=exc.lineno or 0, col_offset=exc.offset or 0))
        return ValidationResult(False, tuple(issues), None)

    node_count = 0
    for node in ast.walk(tree):
        node_count += 1
        if node_count > policy.max_ast_nodes:
            issues.append(ValidationIssue(
                "error", "ast-too-large",
                f"AST exceeds {policy.max_ast_nodes} nodes"))
            break

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            issues.extend(_check_import(node, policy))
        elif isinstance(node, ast.Call):
            issues.extend(_check_call(node, policy))
        elif isinstance(node, ast.keyword):
            if node.arg == "stroke_dasharray":
                issues.append(ValidationIssue(
                    "error", "manim-stroke-dasharray",
                    "stroke_dasharray is not a Manim parameter (RULE 7); use "
                    "DashedLine or DashedVMobject",
                    lineno=getattr(node.value, "lineno", 0)))

    ok = not any(i.severity == "error" for i in issues)
    return ValidationResult(ok, tuple(issues), tree)


def _check_import(node, policy):
    out = []
    roots = _import_roots(node)
    for root in roots:
        if root in policy.forbidden_import_roots:
            out.append(ValidationIssue(
                "error", "forbidden-import",
                f"Import root '{root}' is not allowed in scene code",
                lineno=getattr(node, "lineno", 0)))
        elif root and root not in policy.expected_import_roots:
            out.append(ValidationIssue(
                "warning", "unexpected-import",
                f"Import root '{root}' is unusual for a scene; confirm it is needed",
                lineno=getattr(node, "lineno", 0)))
    return out


def _check_call(node: ast.Call, policy: PythonAstPolicy):
    out = []
    name = _call_name(node.func)
    line = getattr(node, "lineno", 0)

    if name in policy.forbidden_call_names:
        out.append(ValidationIssue(
            "error", "forbidden-call",
            f"Call to '{name}' is not allowed in scene code", lineno=line))

    # RULE 1: VGroup(*self.mobjects)
    if name == "VGroup":
        for arg in node.args:
            if isinstance(arg, ast.Starred):
                tgt = arg.value
                if isinstance(tgt, ast.Attribute) and tgt.attr == "mobjects":
                    out.append(ValidationIssue(
                        "error", "manim-vgroup-mobjects",
                        "VGroup(*self.mobjects) crashes on the Camera (RULE 1); "
                        "use the clear_scene() helper", lineno=line))

    # RULE 10: obj.always_redraw(...) used as a method
    if isinstance(node.func, ast.Attribute) and node.func.attr == "always_redraw":
        out.append(ValidationIssue(
            "error", "manim-always-redraw-method",
            "always_redraw is a module-level function, not a method (RULE 10); "
            "use always_redraw(lambda: ...)", lineno=line))

    # RULE 11: np.trapz
    if isinstance(node.func, ast.Attribute) and node.func.attr == "trapz":
        out.append(ValidationIssue(
            "error", "manim-np-trapz",
            "np.trapz was removed in NumPy 2.0 (RULE 11); use np.trapezoid",
            lineno=line))

    # RULE 8: interpolate_color with a hex string literal
    if name == "interpolate_color":
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str) \
                    and arg.value.startswith("#"):
                out.append(ValidationIssue(
                    "warning", "manim-interpolate-hex",
                    "interpolate_color needs ManimColor, not a hex string (RULE 8)",
                    lineno=line))
                break

    # RULE 2: Text(...) carrying math, and MathTex/Tex carrying raw Unicode
    if name == "Text":
        s = _first_str_arg(node)
        if s is not None and any(ch in s for ch in ("$", "\\", "_", "^")):
            out.append(ValidationIssue(
                "warning", "manim-text-math",
                "Text() should hold plain prose only (RULE 2); math, $, \\, _, ^ "
                "belong in MathTex", lineno=line))
    if name in _MATH_TEXT_CLASSES:
        s = _first_str_arg(node)
        if s is not None and any(ch in _UNICODE_MATH for ch in s):
            out.append(ValidationIssue(
                "error", "manim-unicode-math",
                f"{name} contains raw Unicode math that crashes LaTeX (RULE 2); "
                "use macros like \\alpha, \\to", lineno=line))
    return out


def _first_str_arg(node: ast.Call) -> str | None:
    for arg in node.args:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            return arg.value
        return None
    return None


def _import_roots(node) -> tuple[str, ...]:
    if isinstance(node, ast.Import):
        return tuple(alias.name.split(".", 1)[0] for alias in node.names)
    if node.module is None:
        return ("",)
    return (node.module.split(".", 1)[0],)


def _call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _call_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return None
