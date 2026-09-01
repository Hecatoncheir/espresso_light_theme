#!/usr/bin/env python3
"""Structural checks for the Espresso Light theme descriptors.

These exist because every one of them corresponds to a bug that actually shipped:
a five-digit hex that the platform silently discarded, a menu whose selected row
was painted in the same colour as an unselected one, and syntax colours sitting
at 1.13:1 against their own background.

Run: python3 tools/check_theme.py
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEME = ROOT / "src/main/resources/themes/espresso_light.theme.json"
SCHEME = ROOT / "src/main/resources/themes/espresso_light.xml"

HEX = re.compile(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\Z")
SCHEME_HEX = re.compile(r"[0-9a-fA-F]{1,6}\Z")

# Anything below this against its own background is unreadable rather than subtle.
# The theme deliberately keeps a light yellow-green family around 1.7:1, so the
# floor sits under that: this catches regressions, not style choices.
MIN_SCHEME_CONTRAST = 1.5

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def luminance(value: str) -> float:
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    value = value.rjust(6, "0")[:6]
    channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def check_theme_json() -> None:
    data = json.loads(THEME.read_text())
    palette = data.get("colors", {})

    for name, value in palette.items():
        if not HEX.match(value):
            fail(f"palette: {name} is not a valid colour: {value}")

    def resolve(value):
        """A ui value is a literal colour, a palette name, or something else entirely."""
        if not isinstance(value, str):
            return None
        if value.startswith("#"):
            return value if HEX.match(value) else False
        return palette.get(value)

    def walk(node, path=""):
        if isinstance(node, dict):
            for key, value in node.items():
                walk(value, f"{path}.{key}")
            return
        if not isinstance(node, str):
            return
        if node.startswith("#") and not HEX.match(node):
            fail(f"ui{path}: invalid colour {node}")
        elif not node.startswith("#") and node in palette:
            pass  # resolved palette reference
        elif not node.startswith("#") and re.fullmatch(r"[a-zA-Z][a-zA-Z0-9]*", node):
            # Looks like a palette reference but is not one. Insets ("3,6,3,0")
            # and booleans never reach here.
            fail(f"ui{path}: unknown colour name {node!r}")

    walk(data["ui"])

    ui = data["ui"]

    def value_of(component: str, key: str):
        return resolve(ui.get(component, {}).get(key))

    # A selected row that matches an unselected one has no selected state at all.
    for component in ("MenuItem", "Menu", "List", "Table", "Tree", "CompletionPopup"):
        node = ui.get(component, {})
        base = resolve(node.get("background"))
        selected = resolve(node.get("selectionBackground"))
        if base and selected and base.lower() == selected.lower():
            fail(f"ui.{component}: selectionBackground equals background ({base})")
        fg = resolve(node.get("foreground"))
        sel_fg = resolve(node.get("selectionForeground"))
        if base and selected and fg and sel_fg and fg.lower() == sel_fg.lower() and base.lower() == selected.lower():
            fail(f"ui.{component}: selected state is identical to the normal state")

    # Focused selection must read at least as strongly as unfocused selection.
    for component in ("List", "Table"):
        node = ui.get(component, {})
        surface = resolve(node.get("background")) or resolve(ui["*"]["background"])
        active = resolve(node.get("selectionBackground"))
        inactive = resolve(node.get("selectionInactiveBackground"))
        if surface and active and inactive:
            if contrast(active, surface) < contrast(inactive, surface):
                fail(
                    f"ui.{component}: focused selection ({active}) is weaker against the "
                    f"background than the unfocused one ({inactive})"
                )

    # Borders that match what they separate are not borders.
    borders = ui.get("Borders", {})
    border = resolve(borders.get("color"))
    star_bg = resolve(ui["*"]["background"])
    if border and star_bg and border.lower() == star_bg.lower():
        fail(f"ui.Borders.color equals the default background ({border})")

    # An underline the colour of the tab it underlines marks nothing.
    for component, under, base in (
        ("EditorTabs", "underlineColor", "underlinedTabBackground"),
        ("ToolWindow.HeaderTab", "underlineColor", "underlinedTabBackground"),
    ):
        node = ui
        for part in component.split("."):
            node = node.get(part, {})
        a, b = resolve(node.get(under)), resolve(node.get(base))
        if a and b and a.lower() == b.lower():
            fail(f"ui.{component}: {under} equals {base} ({a})")


def check_editor_scheme() -> None:
    root = ET.parse(SCHEME).getroot()
    default_bg = "ffffff"

    for option in root.find("colors").findall("option"):
        value = option.get("value")
        if value and not SCHEME_HEX.match(value):
            fail(f"scheme colors: {option.get('name')} has invalid value {value}")

    for option in root.find("attributes").findall("option"):
        name = option.get("name")
        attrs = {c.get("name"): c.get("value") for c in option.find("value").findall("option")}
        for key, value in attrs.items():
            if key.endswith(("COLOR", "FOREGROUND", "BACKGROUND")) and value and not SCHEME_HEX.match(value):
                fail(f"scheme {name}: {key} has invalid value {value}")

        fg = attrs.get("FOREGROUND")
        if not fg or not SCHEME_HEX.match(fg):
            continue
        bg = attrs.get("BACKGROUND") or default_bg
        if not SCHEME_HEX.match(bg):
            continue
        if fg.lower() == bg.lower():
            fail(f"scheme {name}: foreground and background are the same colour ({fg})")
            continue
        ratio = contrast(fg, bg)
        if ratio < MIN_SCHEME_CONTRAST:
            fail(f"scheme {name}: {ratio:.2f}:1 is below the {MIN_SCHEME_CONTRAST}:1 floor (#{fg} on #{bg})")


def main() -> int:
    check_theme_json()
    check_editor_scheme()
    if errors:
        print(f"{len(errors)} problem(s) found:\n")
        for error in errors:
            print(f"  {error}")
        return 1
    print("theme descriptors OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
