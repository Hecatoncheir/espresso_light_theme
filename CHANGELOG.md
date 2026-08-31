<!-- Keep a Changelog guide -> https://keepachangelog.com -->

# Espresso Light Theme

## [Unreleased]

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

## [1.0] - 2019-03-29

- First release.
