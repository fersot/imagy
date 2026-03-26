# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-03-25

- First stable release.
- Image processing modules: compress, convert, resize, metadata, remove_bg, rename, lqip.
- Safer outputs with conflict handling to avoid overwriting files.
- Background tasks to prevent UI freezes on heavy operations.
- Improved translations and UI labels consistency.
- Settings stored in AppData for stable theme/language persistence.
- PyInstaller one-folder build with assets and dynamic imports included.

## [1.1.0] - 2026-03-26

- Batch limits per module to improve performance (100 images, remove_bg 10).
- Added core + UI test suites with pytest.
- PEP8 cleanup and naming readability improvements.
- README simplification and clearer install/use instructions.
