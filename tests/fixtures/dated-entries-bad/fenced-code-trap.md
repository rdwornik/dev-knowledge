# Changelog

<!-- scope: meta -->

```
## 2026-05-15

### Added

- This looks like a valid entry but is inside a fenced code block
- Validator must skip it and NOT count it as a real heading
```

The file has no real dated headings outside the fenced block.
The validator must return warn/fail, not pass, since there are no real H2 date headings.
