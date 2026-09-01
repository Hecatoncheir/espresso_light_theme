# Espresso Light Theme

[![Version](https://img.shields.io/jetbrains/plugin/v/12317.svg)](https://plugins.jetbrains.com/plugin/12317-espresso-light-theme)
[![Downloads](https://img.shields.io/jetbrains/plugin/d/12317.svg)](https://plugins.jetbrains.com/plugin/12317-espresso-light-theme)
[![Rating](https://img.shields.io/jetbrains/plugin/r/rating/12317.svg)](https://plugins.jetbrains.com/plugin/12317-espresso-light-theme/reviews)
[![License: MIT](https://img.shields.io/badge/license-MIT-informational.svg)](LICENSE)

<!-- Plugin description -->
A warm light theme for IntelliJ IDEA and the other JetBrains IDEs: cream surfaces, a pink accent and a soft green syntax family.

The plugin ships a UI theme together with a matching editor colour scheme, including dedicated highlighting for Dart, Go, JavaScript, CSS and SASS, HTML and XML, YAML, Bash and `.gitignore`.

![Editor](https://github.com/hecatoncheir/espresso_light_theme/raw/master/docs/screenshots/editor.png)

![Debug](https://github.com/hecatoncheir/espresso_light_theme/raw/master/docs/screenshots/debug_window.png)
<!-- Plugin description end -->

## Install

From the IDE: **Settings → Plugins → Marketplace**, search for *Espresso Light Theme*, install and pick it under **Settings → Appearance & Behavior → Appearance → Theme**.

Or install it [from JetBrains Marketplace](https://plugins.jetbrains.com/plugin/12317-espresso-light-theme).

## Screenshots

[The full gallery lives in PREVIEW.md](PREVIEW.md) — editor, debugger, completion, popups, menus, search, settings and per-language syntax.

### Editor
![Editor](https://github.com/hecatoncheir/espresso_light_theme/raw/master/docs/screenshots/editor.png)

### Debug
![Debug](https://github.com/hecatoncheir/espresso_light_theme/raw/master/docs/screenshots/debug_window.png)

## Bracket pair highlighting

The scheme also colours the eleven `*_ATTR` keys used by
[HighlightBracketPair](https://github.com/Rasarts/HighlightBracketPair) — `BRACE_ATTR`, `BRACKET_ATTR`, `PARENTHESIS_ATTR`,
`CUSP_BRACKETS_ATTR`, `DOUBLE_QUOTE_ATTR` and their `_LINE_ATTR` counterparts —
so brace pairs and the lines between them pick up the theme instead of falling
back to the platform defaults.

The patched build this was tuned against is kept in the repository root as
[`HighlightBracketPair-1.1.2_ShowBracesInGutterWithVerticalLines.jar.jar`](HighlightBracketPair-1.1.2_ShowBracesInGutterWithVerticalLines.jar.jar); it is a fork adding braces in the gutter with vertical lines.
Install it via **Settings → Plugins → ⚙ → Install Plugin from Disk**. The theme
works fine without it — those keys are simply unused.

![Bracket pair highlighting](https://github.com/hecatoncheir/espresso_light_theme/raw/master/docs/screenshots/brace_highlight.gif)

## Build from source

Requires JDK 11 or newer; the Gradle wrapper handles everything else.

```bash
./gradlew buildPlugin
```

The installable archive lands in `build/distributions`. To try it in a sandbox IDE:

```bash
./gradlew runIde
```

Theme sources live in `src/main/resources/themes`: `espresso_light.theme.json` holds the UI colours (with a named palette at the top of the file) and `espresso_light.xml` the editor colour scheme.

## License

[MIT](LICENSE) © Vitaliy Vostrikov
