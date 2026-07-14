#!/usr/bin/env python3
"""Validate Rainmeter skin .ini files.

Phase A: syntax — every .ini must parse as valid INI (no duplicate sections/keys,
no malformed lines).

Phase B: reference integrity — for each skin entry point (a top-level .ini with a
[Rainmeter] section), resolve its @Include chain and check that every #Var#,
[Section:Property], literal MeasureName=, and @Include reference resolves.

Deliberately out of scope: Calc formula evaluation, dynamic/computed variable
values, and any check beyond static reference resolution.
"""

import configparser
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESOURCES_DIR = os.path.join(ROOT, "@Resources")

EXCLUDE_DIRS = {".git", ".worktrees"}

BUILTIN_VARS = {
    "@",
    "CURRENTPATH",
    "CURRENTFILE",
    "ROOTCONFIG",
    "CURRENTCONFIG",
    "CURRENTSECTION",
    "SKINSPATH",
    "PROGRAMPATH",
    "SCREENAREAWIDTH",
    "SCREENAREAHEIGHT",
}

VAR_RE = re.compile(r"#([A-Za-z0-9_@]+)#")
SECTION_REF_RE = re.compile(r"\[([A-Za-z0-9_]+):[A-Za-z0-9_]+\]")
MEASURE_NAME_KEY_RE = re.compile(r"^MeasureName\d*$")


def find_ini_files():
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for name in filenames:
            if name.lower().endswith(".ini"):
                files.append(os.path.join(dirpath, name))
    return sorted(files)


def make_parser(strict):
    cp = configparser.ConfigParser(
        interpolation=None,
        strict=strict,
        comment_prefixes=(";",),
        delimiters=("=",),
    )
    cp.optionxform = str
    return cp


def resolve_include_path(raw_value):
    """Resolve a Rainmeter '#@#relative/path' include value to an absolute path."""
    relative = raw_value.strip().strip('"').replace("#@#", "")
    return os.path.normpath(os.path.join(RESOURCES_DIR, relative))


def resolve_chain(entry_file):
    """Depth-first resolve entry_file's @Include chain. Returns (ordered_files, errors)."""
    order = []
    visited = set()
    errors = []

    def visit(path):
        if path in visited:
            return
        visited.add(path)
        if not os.path.isfile(path):
            errors.append((entry_file, "Variables", "@Include", f"included file not found: {path}"))
            return
        cp = make_parser(strict=False)
        try:
            cp.read(path, encoding="utf-8")
        except configparser.Error:
            return  # already reported in Phase A
        if cp.has_section("Variables"):
            for key, val in cp["Variables"].items():
                if key.lower().startswith("@include"):
                    visit(resolve_include_path(val))
        order.append(path)

    visit(entry_file)
    return order, errors


def check_references(entry_file):
    errors = []
    order, include_errors = resolve_chain(entry_file)
    errors.extend(include_errors)

    merged = make_parser(strict=False)
    merged.read(order, encoding="utf-8")

    defined_sections = set(merged.sections())
    defined_vars = set(BUILTIN_VARS)
    if merged.has_section("Variables"):
        defined_vars.update(merged["Variables"].keys())

    for section in merged.sections():
        for key, val in merged[section].items():
            if val is None:
                continue
            stripped = val.strip().strip('"')

            for token in VAR_RE.findall(val):
                if token not in defined_vars:
                    errors.append((entry_file, section, key, f"undefined variable #{token}#"))

            for ref_section in SECTION_REF_RE.findall(val):
                if ref_section not in defined_sections:
                    errors.append((entry_file, section, key, f"reference to undefined section [{ref_section}]"))

            if MEASURE_NAME_KEY_RE.match(key) and "#" not in stripped:
                if stripped and stripped not in defined_sections:
                    errors.append((entry_file, section, key, f"MeasureName references undefined section [{stripped}]"))

    return errors


def main():
    ini_files = find_ini_files()
    if not ini_files:
        print("No .ini files found.")
        return 1

    syntax_errors = []
    parsed_ok = []
    for path in ini_files:
        cp = make_parser(strict=True)
        try:
            cp.read(path, encoding="utf-8")
            parsed_ok.append(path)
        except configparser.Error as exc:
            syntax_errors.append((path, str(exc).splitlines()[0]))

    reference_errors = []
    entry_points = []
    for path in parsed_ok:
        cp = make_parser(strict=False)
        cp.read(path, encoding="utf-8")
        if cp.has_section("Rainmeter"):
            entry_points.append(path)

    for entry in entry_points:
        reference_errors.extend(check_references(entry))

    def rel(p):
        return os.path.relpath(p, ROOT)

    if syntax_errors:
        print(f"Phase A — syntax: {len(syntax_errors)} error(s)")
        for path, message in syntax_errors:
            print(f"  {rel(path)}: {message}")
    else:
        print(f"Phase A — syntax: {len(ini_files)} file(s) parsed OK")

    if reference_errors:
        print(f"Phase B — references: {len(reference_errors)} error(s)")
        for entry, section, key, message in reference_errors:
            print(f"  {rel(entry)} [{section}] {key}: {message}")
    else:
        print(f"Phase B — references: {len(entry_points)} entry point(s) checked, 0 error(s)")

    return 1 if (syntax_errors or reference_errors) else 0


if __name__ == "__main__":
    sys.exit(main())
