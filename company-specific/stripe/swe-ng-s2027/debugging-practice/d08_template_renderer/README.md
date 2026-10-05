# D08 — Mini Template Engine Regressions

**Difficulty:** Hard  
**Target:** 55 minutes

This final exercise is an original miniature template library. It intentionally
resembles the experience of debugging an unfamiliar third-party package: token
parsing, rendering, file-like includes, and a compilation cache are split across
modules.

Users report problems involving raw variables, included templates, HTML
attributes, and templates with the same filename in different directories.

## Syntax and contract

- `{{ name }}` renders an HTML-escaped variable.
- `{{{ name }}}` renders a raw, unescaped variable.
- Dotted variables such as `{{ customer.name }}` traverse dictionaries.
- `{% include "path.tpl" %}` renders another template with the **same context**.
- Missing variables render as the empty string.
- Escaping covers `&`, `<`, `>`, single quote, and double quote.
- `DictTemplateLoader` maps complete template paths to source strings.
- Parsed-template caching must not alias different complete paths.

Run `pytest -q`. Fix the library rather than special-casing test templates. Do
not replace the parser with an external dependency.

