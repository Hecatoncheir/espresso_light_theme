<!-- Keep a Changelog guide -> https://keepachangelog.com -->

# Espresso Light Theme

## [Unreleased]

## [1.4.2] - 2026-09-01

Released together: 1.4.1 was prepared but never published, so everything below
ships in this version.

### Added
- New UI coverage (IDEA 2022.3 and newer): `MainToolbar`, `MainMenu`, `RunWidget`, `Tag`, `Counter`, `OnePixelDivider`, `TableHeader` and `DefaultTabs`. The theme described 38 components and now describes 46; on any recent IDE those surfaces previously fell back to platform defaults. Key names come from the platform's own `expUI_light.theme.json`.
- `tools/check_theme.py`, run in CI: it rejects invalid colour values, palette names that resolve to nothing, a selection painted in its own background colour, a tab underline the colour of its tab, borders the colour of the background, a focused selection weaker than an unfocused one, and any editor-scheme colour below 1.5:1.
- `2019.1.4` in the plugin verifier list — the oldest release `pluginSinceBuild` claims, and until now never actually tested.

### Fixed
- Focused selection was fainter than unfocused selection in lists and tables: `List` read 1.11:1 focused against 1.24:1 unfocused, `Table` 1.03:1 against 1.24:1. Focused selection is now the deeper cream the menus use, unfocused the lighter one.
- Selected labels in lists and tables were hard to read at 3.21:1 and 2.72:1; they now sit at 5.02:1.
- Unfocused tree selection was pure white on a `#f5f5f5` tree.
- Menu separators were white on a cream menu.

### Changed
- Migrated from the Gradle IntelliJ Plugin 1.8.0 to the IntelliJ Platform Gradle Plugin 2.18.1, which is the maintained one. The old plugin only worked on Gradle 7: it breaks on Gradle 8 (`ArchivePublishArtifact`) and on Gradle 9 (`JavaPluginConvention`).
- Gradle 7.5.1 to 9.7.1, and the build now targets IntelliJ Platform 2025.2.6 instead of 2021.3.3. CI runs on Java 21, which build 252 requires.
- `buildSearchableOptions` is off: a colour theme has no searchable settings, and building them starts a full IDE.
- Plugin signing is now skipped by the platform plugin itself when no certificate is configured, so the local `onlyIf` guard added in 1.4.1 is gone.
- Dropped Qodana. It analyses source code, and this project has none.

### Removed
- `pluginUntilBuild` and `platformPlugins` properties, both unused: `until-build` is now unset directly in the build script, and the theme depends on no plugins.

## [1.4.0] - 2026-08-31

### Added
- Plugin icon drawn in the theme's own palette, plus a `pluginIcon_dark.svg` variant for dark IDE themes.
- Named colour palette in `espresso_light.theme.json` — 26 semantic names covering 178 of the 197 colour references in the `ui` section.
- GitHub Actions workflow building and verifying the plugin on every push and pull request.

### Changed
- Dropped the `until-build` constraint. The theme was pinned to 2022.2 and would not install on anything newer.
- Unified the yellow-green syntax family on `#b8d270`.
- Replaced colours inherited from the project templates: `#0000ff` in TODOs, `#008000` in typos and invalid escapes, four `#ff0000`, and the Darcula orange and grey used throughout the `.gitignore` highlighting.
- Dropped the Kotlin Gradle plugin — this project has no sources to compile.

### Fixed
- The plugin icon was named `pluginicon.svg`; the platform only looks for `pluginIcon.svg`, so no icon was ever shown.
- `EditorTabs.borderColor` was `#FFFFF` — five hex digits, silently discarded by the colour parser.
- Menu item selection was invisible: `MenuItem.background` and `selectionBackground` were both `#d8e8f2`, and both foregrounds `#325a7d`.
- Search matches were invisible: `SearchMatch` painted white on a near-white list background.
- The active editor tab and tool window tab drew a white underline on a white tab.
- Panel borders were the same colour as the panel background.
- Keywords were left uncoloured in every language except Java and Dart. `DEFAULT_KEYWORD` was blank, which shadows the parent scheme rather than inheriting from it; sixteen further blank overrides were removed for the same reason.
- Raised the colours that were effectively unreadable, worst first: `DIFF_DELETED` at 1.13:1, `LINE_PARTIAL_COVERAGE` at 1.26:1, the white-on-colour foregrounds in the debugger execution point and matched braces, and the console and log palette.

## [1.3.2] - 2022-08-23

- Update menu colors.

## [1.3.1] - 2022-08-23

- Update completion popup colors.

## [1.3.0] - 2022-08-21

- Update menu colors.
- Update completion popup colors.

## [1.2.0] - 2021-03-17

- Fix UI colors.

## [1.1.5]

- Update GoLang package colors.

## [1.1.4] - 2020-02-06

- Update GoLang colors.

## [1.1.3] - 2019-08-27

- Update debugger tabs color.

## [1.1.2] - 2019-08-01

- Update header tabs colors, header button colors, debugger tabs colors.

## [1.1.1]

- Update scrollbar and tabs colors.

## [1.1.0]

- Update menu and title colors.

## [1.0.9]

- Enable plugin in all products.

## [1.0.8]

- Change scrollbar color.

## [1.0.7]

- Cleanup.

## [1.0.6]

- Added colors for [HighlightBracketPair](https://github.com/Rasarts/HighlightBracketPair).

## [1.0.5]

- Cleanup.

## [1.0.4]

- Update Dart constructor color.

## [1.0.2]

- Update minimum idea version to 191.0.

## [1.0.0] - 2019-03-29

- First release.
